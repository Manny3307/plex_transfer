import os
import json
from helpers.db_helpers import dbFunction
import datetime, dateutil
from ftplib import FTP_TLS
from tqdm import tqdm
from dotenv import load_dotenv
import ftplib
from pathlib import Path
from plexapi.server import PlexServer


class FTPHelpers(dbFunction):

    def __init__(self):
        global uploaded_file_names

    #Files to upload to Plex Server
    def upload_to_plex(self):
        html_str = ""
        super().__init__() #Call the constrcutor of the dbFucntion class
        ftps = FTP_TLS() #Initialize FTP object
        home_folder = self.get_conf_val("home_folder")
        print(home_folder)
        dotenv_path = Path(f'{home_folder}/conf/.env') #Load environment variable file
        load_dotenv(dotenv_path=dotenv_path)
        ftp_plex_server = os.getenv("FTP_server")
        ftp_plex_server_login = os.getenv("FTP_server_login")
        ftp_plex_server_password = os.getenv("FTP_server_password")
        try:
            ftps = ftplib.FTP(f'{ftp_plex_server}', f'{ftp_plex_server_login}', f'{ftp_plex_server_password}')
        except Exception as e:
            print(e)    
            print("Login Failed!!!")
        uploaded_file_names = []
        FTP_Path = os.getenv('FTP_server_folder_path')
        ftps.cwd(FTP_Path)
        f_names = self.get_file_names_from_database()
        base_folder_name = self.get_conf_val("base_folder")
        print("+++++++++++++++ Start uploading the files to Plex Server ++++++++++++++++++")
        if not f_names:
            html_str = f"<h3>No file(s) to upload at {datetime.datetime.now()}</h3> </br><ol>"    
        else:
            html_str = f"<h3>Following file(s) have been uploaded to Plex Server.</h3> </br><ol>"    
        try:
            for file_n in f_names:
                complete_file_path = f"{base_folder_name}/{file_n}"
                filename_without_path = file_n
                filesize = int(os.path.getsize(complete_file_path))
                TheFile = open(complete_file_path, 'rb')
                with tqdm(unit = 'blocks', unit_scale = True, leave = False, miniters = 1, desc = f'Uploading {file_n}......', total = filesize) as tqdm_instance:
                    ftps.storbinary(f'STOR {filename_without_path}', TheFile , 2048, callback = lambda sent: tqdm_instance.update(len(sent)))
                uploaded_file_names.append(filename_without_path)
                html_str += f"<li>{filename_without_path}</li>"
                self.update_isExecuted_flag_against_file_name(filename_without_path)

            html_str += "</ol>"
            
        except Exception as e:
            print(e)
            print("Upload error. Please try again")
        
        
        for file_names in uploaded_file_names:
            print(file_names)
        
        with open(f'{home_folder}/html/html_content.txt', 'w') as file_content:
            file_content.write(html_str)

        ftps.close()
        ftps = None
        print("+++++++++++++++ Above file(s) uploaded to Plex Server Successfully ++++++++++++++++++")

        print("+++++++++++++++ Start scanning the files into the Library on the Plex Server ++++++++++++++++++")
        self.update_plex_server()
        print("+++++++++++++++ Finished scanning the files successfully into the Library on the Plex Server ++++++++++++++++++")

    #Update the Plex Server after copying files to it.
    def update_plex_server(self):
        home_folder = self.get_conf_val("home_folder")
        dotenv_path = Path(f'{home_folder}/conf/.env') #Load environment variable file
        load_dotenv(dotenv_path=dotenv_path)

        Plex_server_host = os.getenv("Plex_server_host")
        Plex_server_port = os.getenv("Plex_server_port")
        Plex_server_token = os.getenv("Plex_server_token")
        try:
            baseurl = f'http://{Plex_server_host}:{Plex_server_port}'
            plex = PlexServer(baseurl, Plex_server_token)

            vids  = plex.library.section('Manny')
            vids.update()
        except Exception as e:
            print(e)
            print("Connection Failed. Please try to login into the Plex Server using the browser")
