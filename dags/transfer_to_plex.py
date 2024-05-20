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
from helpers.file_transfer_helpers import PlexHelperFunctions
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