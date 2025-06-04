from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
# from azure.storage.filedatalake import DataLakeServiceClient
from airflow.providers.microsoft.azure.sensors.wasb import WasbPrefixSensor
from airflow.providers.sftp.sensors.sftp import SFTPSensor
from datetime import datetime

default_args = {
    "owner": "Siddharth",
    "start_date": datetime(2024, 11, 8, 14, 00),
    "email_on_failure": False
}

dag = DAG(
    dag_id="dag-05",
    default_args=default_args,
    schedule_interval="@once",
    catchup=False
)

start_task = DummyOperator(
    task_id="Start",
    dag=dag
)

"""
tasks to add:
1. Sense the file in cloud bucket
2. Unzip file in landing bucket of any cloud
3. Move file to source directory of any cloud bucket
4. Process file and load it to the cloud data warehouse
5. Move file to archive bucket once processing is complete
6. compress it back to save on storage
"""

# sense_adls_file = WasbPrefixSensor(
#     container_name=CONTAINER_NAME,
#     prefix=PREFIX,
#     task_id="sense_adls_file_with_prefix"
# )

# unzip_file_task = bashOperator(
    
# )

sftp_sensor = SFTPSensor(
    task_id="file_sensor",
    sftp_conn_id="data-ingestion",
    path="/home/sftp_user/work/data/",
    file_pattern="test01.txt",
    poke_interval=60,
    timeout=60*10,
    dag=dag
    )
    


end_task = DummyOperator(
    task_id="End",
    dag=dag
)

start_task >> sftp_sensor >> end_task