from airflow.operators.empty import EmptyOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow import DAG
from datetime import datetime
import os
import glob

default_args = {
    "owner": "Siddharth",
    "start_date": datetime(2024, 11, 8, 14, 0),
    "email" : [""],
    "email_on_failure": False,
    "depends_on_past" : False,
    "email_on_retry" : False,
    "retries" : 1,
}

def check_files(ti):
    accounts_file_path = glob.glob("/opt/shared/sbdl-app/test_data/accounts/account*.csv")
    parties_file_path = glob.glob("/opt/shared/sbdl-app/test_data/parties/party*.csv")
    party_address_file_path = glob.glob("/opt/shared/sbdl-app/test_data/party_address/address*.csv")
    
    all_exists = all([accounts_file_path, parties_file_path, party_address_file_path])
    
    ti.xcom_push(key="file_status", value="Files found" if all_exists else "Files not found")

def decide_branch(ti):
    status = ti.xcom_pull(task_ids="check_files", key="file_status")
    return "submit_sbdl" if status == "Files found" else "skip_processing"
        
with DAG(
    dag_id="spark_submit_operator",
    default_args=default_args,
    schedule="@once",
    catchup=False,
) as dag:
      
    start_task = EmptyOperator(task_id="start")
    
    check_files_task = PythonOperator(
        task_id="check_files",
        python_callable=check_files,
    )
    
    branch_task = BranchPythonOperator(
        task_id="decide_branch",
        python_callable=decide_branch,
    )
    
    spark_job = SparkSubmitOperator(
        task_id="submit_sbdl",
        application="/opt/shared/sbdl-app/sbdl_main.py",
        conn_id="spark",
        application_args=["local", "22-06-2025"],
        verbose=True,
        conf={
            "spark.submit.deployMode": "client",
            "spark.driver.extraClassPath": "/opt/spark/jars/postgresql-42.6.0.jar",
        },
        jars="/opt/spark/jars/postgresql-42.6.0.jar"
    )

    skip_task = EmptyOperator(task_id="skip_processing")
    
    end_task = EmptyOperator(task_id="end", trigger_rule="none_failed_min_one_success")

    # Start >> Check if Files present in data source >> If present > Process Task > Spark-Submit operator > End, 
    # If not present > Skip spark-submit task > End 
    
    # DAG Flow
    start_task >> check_files_task >> branch_task
    branch_task >> [spark_job, skip_task] >> end_task
