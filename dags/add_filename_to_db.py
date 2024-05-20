import airflow
from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.sensors.http_sensor import HttpSensor
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import sys
sys.path.append('/home/manny/plex_transfer')
from helpers.db_helpers import dbFunction
from helpers.ftp_helpers import FTPHelpers
from helpers.file_transfer_helpers import PlexHelperFunctions
from datetime import datetime, timedelta

#Adding filenames to Postgresql Database
def add_filename_database():
    obj_db = dbFunction()
    obj_db.files_to_upload()
    print("Adding filenames to database!!!")

args_for_database_logs = {
            "owner": "Airflow",
            "start_date": airflow.utils.dates.days_ago(1),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "mannyelaine26@gmail.com",
            "retries": 1,
            "retry_delay": timedelta(seconds=1)
        }

#Adding filenames to the postgres database for the unique generated batch ID.
with DAG(dag_id="Adding_Log_to_Database", schedule_interval=timedelta(hours=3), default_args=args_for_database_logs, catchup=False) as dag:

    # Task to add the file_name to database
    adding_file_to_database_log = PythonOperator(
            task_id="adding_file_to_database_log",
            python_callable=add_filename_database
    )
    
    trigger_start_copying_to_plex_server = TriggerDagRunOperator(
            task_id="trigger_start_copying_to_plex_server",
            trigger_dag_id="Copy_Files_To_Plex",
            conf={"message": "Database Log has been added successfully!"}
    )

    '''# Define the task to monitor the file
    file_sensor_task = FileSensor(
        task_id='file_sensor_task',
        fs_conn_id='fs_default',
        poke_interval=3,
        timeout=10,  
        filepath='/media/manny/Backups/MASM', 
        dag=dag
    )'''
   
    adding_file_to_database_log >> trigger_start_copying_to_plex_server