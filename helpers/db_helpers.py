import json
from helpers.file_transfer_helpers import PlexHelperFunctions
from sqlalchemy import create_engine
import sqlalchemy as db
import datetime, dateutil
import sys, os
sys.path.append('/home/manny/plex_transfer')


#Perform the database functions to send and retrieve the data from database.
class dbFunction(PlexHelperFunctions):
    
    def __init__(self):
        global DBConnecter, UserName, Password, ServerOrEndPoint, DatabaseName, connection_string, engine
        DBConfig = open("/home/manny/plex_transfer/helpers/helper_db_config.json")
        dbconf = json.load(DBConfig)
        DBConnector = dbconf["DBConfigs"]["postgresql"]["DBConnecter"]
        UserName = dbconf["DBConfigs"]["postgresql"]["UserName"]
        Password = dbconf["DBConfigs"]["postgresql"]["Password"]
        ServerOrEndPoint = dbconf["DBConfigs"]["postgresql"]["ServerOrEndPoint"]
        DatabaseName = dbconf["DBConfigs"]["postgresql"]["DatabaseName"]
        engine = create_engine(f'{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}')

    #Insert a new file record in database
    def insert_new_file_record(self, filename):
        is_row_inserted = True
        is_executed = False
        batch_id = self.get_batch_id_from_database()
        try:
            insert_new_file_record_query = f"INSERT INTO tbl_File_Batch_info (file_name, batch_id, file_date_time, is_executed) VALUES ('{filename}','{batch_id}',CURRENT_TIMESTAMP, '{is_executed}')"
            with engine.connect() as conn:
                insert_new_file_record = conn.execute(db.text(insert_new_file_record_query))
        except Exception as error: 
            print(error)
            is_row_inserted = False
        
        return is_row_inserted

    #Get the last batch ID from the database if its older than 30 mins then create a new one.
    def get_batch_id_from_database(self):
        batch_id_result = ""
        try:
            get_batch_id_query = 'select * from tbl_File_Batch_info ORDER BY file_date_time DESC LIMIT 1'
            with engine.connect() as conn:
                batch_id_result = conn.execute(db.text(get_batch_id_query)).fetchall()
                if not batch_id_result:
                    batch_id = self.generate_batch_ID(10)
                else:
                    batch_time_in_minutes = batch_id_result[0][3]
                    batch_id = batch_id_result[0][2]
                    time_difference = self.get_minutes_difference(batch_time_in_minutes)
                    
                    if(time_difference > 30):
                        batch_id = self.generate_batch_ID(10)
        except Exception as error: 
            print(error)
        
        return batch_id

    '''
    Get the minutes based on the timestamp of last batch_id with the current timestamp 
    and get the difference.
    '''
    def get_minutes_difference(self, database_time):
        time_fmt = "%Y-%m-%d %H:%M:%S"

        rounded_current_time = str(datetime.datetime.now()).split(".")[0]
        current_timestamp = datetime.datetime.strptime(rounded_current_time, time_fmt)

        rounded_database_time = str(database_time).split(".")[0]
        database_timestamp = datetime.datetime.strptime(rounded_database_time, time_fmt)
        
        time_difference = current_timestamp - database_timestamp
        time_difference_in_minutes = divmod(time_difference.total_seconds(), 60)[0]
        return(time_difference_in_minutes)

    #Files to upload from source folder to plex server which are not present in plex server
    def files_to_upload(self):
        files_list = []
        str_file_name = ""
        base_folder_name = self.get_conf_val("base_folder")
        special_chars = ["(",")","'",","]

        file_list_without_special_chars = self.get_files()
        #get the list of the files in the base folder or source folder
        for lst in file_list_without_special_chars:
            filename = lst.split('/')[-1]
            Actual_fl_name = f'{base_folder_name}/{filename}'
            filename = self.remove_special_chars_from_file_name(str(filename))
            chars_removed_fl_name = f'{base_folder_name}/{filename}'
            os.rename(Actual_fl_name, chars_removed_fl_name)
            str_file_name_rounded = f"('{filename}'),"
            str_file_name += str_file_name_rounded
        
        str_file_name = str_file_name[:-1]
        try:
            get_batch_id_query = f"SELECT v FROM (VALUES {str_file_name}) AS vs(v) WHERE v NOT IN (SELECT file_name FROM tbl_File_Batch_info)"
            with engine.connect() as conn:
                files_to_upload = conn.execute(db.text(get_batch_id_query)).fetchall()
                if not files_to_upload:
                    print(f"Server is up to date and no files required to upload")
                else:
                    print(f"Following are the files to upload \n {files_to_upload}")
                    for fl_name in files_to_upload:
                        fl_name = ''.join(i for i in fl_name if not i in special_chars)
                        files_list.append(fl_name.split('/')[-1])

                    for file_n in files_list:
                        include_file_name = self.include_file_names(file_n)
                        if include_file_name == file_n:
                            self.insert_new_file_record(file_n)

        except Exception as error: 
            print("Connection Refused")
            print(error)

        return files_to_upload
    
    
    #Get filenames from the database which are not uploaded to Plex Server
    def get_file_names_from_database(self):
        clean_lst_from_special_chars = []
        get_batch_id_query = f"SELECT file_name FROM tbl_File_Batch_info WHERE is_executed = False"
        try:
            with engine.connect() as conn:
                get_files_to_upload = conn.execute(db.text(get_batch_id_query)).fetchall()
                
                for f in get_files_to_upload:
                    f = self.remove_special_chars_from_file_name(str(f))
                    clean_lst_from_special_chars.append(f)
                    
                
        except Exception as e:
            print(e)
            print("Could not connect to database")

        return clean_lst_from_special_chars
    
    #Update the is_executed flag against the uploaded file towards the Plex Server
    def update_isExecuted_flag_against_file_name(self, file_name):
        get_batch_id_query = f"UPDATE tbl_File_Batch_info SET is_executed = True WHERE file_name = '{file_name}'"
        try:
            with engine.connect() as conn:
                conn.execute(db.text(get_batch_id_query))
        except Exception as e:
            print(e)
            print("Error while updating the is_executed flag")