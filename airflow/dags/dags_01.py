from airflow import DAG
from airflow.operators.empty import EmptyOperator
import datetime

with DAG(
    dag_id = "test_dag",
    start_date = datetime.datetime(2024, 10, 4),
    schedule="@daily",
    ):
    EmptyOperator(task_id="task")