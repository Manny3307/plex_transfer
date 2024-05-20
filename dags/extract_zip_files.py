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

#Extract zip files to respective zip folders
def extract_zip_files_to_folder():
    print("Extracting Zip files in the zip folder!!!")
    obj_plex = PlexHelperFunctions()
    obj_plex.extract_zip_files()


args_for_extracting_zip_files = {
            "owner": "Airflow",
            "start_date": airflow.utils.dates.days_ago(1),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "mannyelaine26@gmail.com",
            "retries": 1,
            "retry_delay": timedelta(hours=1)
        }

with DAG(dag_id="Extracting_Zip_Files", schedule_interval=timedelta(hours=6), default_args=args_for_extracting_zip_files, catchup=False) as dag:

    # Task to add the file_name to database
    extracting_zip_file_to_zip_folder = PythonOperator(
            task_id="extracting_zip_file_to_zip_folder",
            python_callable=extract_zip_files_to_folder
    )

    trigger_add_to_DB = TriggerDagRunOperator(
            task_id="trigger_add_to_DB",
            trigger_dag_id="Adding_Log_to_Database",
            conf={"message": "Zip files extraction is complete!"}
    )
    
    extracting_zip_file_to_zip_folder >> trigger_add_to_DB
