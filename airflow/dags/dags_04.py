from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime

# Define default args
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024,10,30,4,25),  # The DAG will start running from one day ago
    'email_on_failure': False,
    'email_on_retry': False,
}

# Define the DAG
with DAG(
    dag_id='airflow-postgres',  # Name of the DAG
    default_args=default_args,
    description='DAG to load data from one table to another in PostgreSQL',
    schedule_interval='@once',  # No automatic schedule, it can be triggered manually
    catchup=False,  # Do not run missed schedules
) as dag:
    # 1. Start task dummy operator
    start_task = DummyOperator(task_id='Start')
    # 2. Task to load data from source_table to target_table
    pg_data_load_task = PostgresOperator(
        task_id='pg_data_load_task',  # Unique id for the task
        postgres_conn_id='postgres_dwh',  # Connection id from Airflow
        sql="""
            
            SELECT empid, fname, lname
            FROM emp;
        """,
        database='dwh',
        dag=dag# Specify the database name where the tables reside
    )
    
    # 3. End task dummy operator
    end_task = DummyOperator(task_id='End')
    

# Set the task in the DAG
start_task >> pg_data_load_task >> end_task