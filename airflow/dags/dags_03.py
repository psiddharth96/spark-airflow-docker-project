from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG(
    dag_id='test_dag_03',
    start_date=datetime(2024, 10, 10)
)

empty_task = EmptyOperator(
    task_id='start',
    dag=dag
)

bash_task = BashOperator(
    task_id = 'run_bash',
    bash_command='echo Hello Airflow!' ,
    dag=dag   
)

empty_task >> bash_task

bash_task_1 = BashOperator(
    task_id = 'bash_task_2',
    bash_command='echo this is second bash task'
)

def test_fn():
    print('hello python')

python_run_task = PythonOperator(
    task_id = 'run_python',
    python_callable=test_fn
)

empty_task >> bash_task >> bash_task_1 >> python_run_task