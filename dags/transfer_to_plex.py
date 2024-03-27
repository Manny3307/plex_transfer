import airflow
from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.sensors.http_sensor import HttpSensor
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
import sys
sys.path.append('/home/manny/plex_transfer')
from helpers.db_helpers import dbFunction
from helpers.ftp_helpers import FTPHelpers
from datetime import datetime, timedelta
from ftplib import FTP_TLS
#from tqdm import tqdm
from pathlib import Path
import os
import csv
#import requests
import json

#Copy files to Plex Server
def copy_file_to_plex_server():
    print("Copying file(s) to Plex!!!")
    obj_ftp = FTPHelpers()
    obj_ftp.upload_to_plex()

#Adding filenames to Postgresql Database
def add_filename_database():
    obj_db = dbFunction()
    obj_db.files_to_upload()
    print("Adding filenames to database!!!")

#Create and send the email to notify success or failure of the copy functions.
def create_html_content(**kwargs):
    with open('/home/manny/plex_transfer/html/html_content.txt', 'r') as file_content:
        email_content = file_content.read()

    send_email = EmailOperator(
        task_id="send_email",
        to="mannyelaine26@gmail.com",
        subject="File Upload Status",
        html_content=email_content
    )
    send_email.execute(context=kwargs)

args_for_file_sensor = {
            "owner": "Airflow",
            "start_date": airflow.utils.dates.days_ago(1),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "mannyelaine26@gmail.com",
            "retries": 1,
            "retry_delay": timedelta(seconds=1)
        }


args_for_copy_file_plex = {
            "owner": "Airflow",
            "start_date": airflow.utils.dates.days_ago(1),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "mannyelaine26@gmail.com",
            "retries": 1,
            "retry_delay": timedelta(seconds=5)
        }

#Copy files to the Plex server via FTP as per the batch.
with DAG(dag_id="Copy_Files_To_Plex", schedule_interval=timedelta(hours=12), default_args=args_for_copy_file_plex, catchup=False) as dag:
    
    copy_file_to_plex = PythonOperator(
            task_id="transferring_file_to_plex",
            python_callable=copy_file_to_plex_server
    )

    send_email = PythonOperator(
        task_id="send_email",
        python_callable=create_html_content,
        provide_context=True
    )

    copy_file_to_plex >> send_email

#Adding filenames to the postgres database for the unique generated batch ID.
with DAG(dag_id="Adding_Log_to_Database", schedule_interval=timedelta(minutes=5), default_args=args_for_file_sensor, catchup=False) as dag:

    # Task to add the file_name to database
    adding_file_to_database_log = PythonOperator(
            task_id="adding_file_to_database_log",
            python_callable=add_filename_database
    )
    
    # Define the task to monitor the file
    file_sensor_task = FileSensor(
        task_id='file_sensor_task',
        fs_conn_id='fs_default',
        poke_interval=3,
        timeout=10,  
        filepath='/media/manny/Backups/MASM', 
        dag=dag
    )
   
    file_sensor_task >> adding_file_to_database_log