
import os, sys
import json
from sqlalchemy import create_engine
import sqlalchemy as db
import datetime, dateutil
sys.path.append(os.path.abspath("/mnt/d/flex_transfer/helpers/"))
from helpers.file_transfer_helpers import PlexHelperFunctions
from helpers.db_helpers import dbFunction


obj_plex = PlexHelperFunctions()
obj_db = dbFunction()

DBConfig = open("../conf/db_conf.json")
dbconf = json.load(DBConfig)
DBConnector = dbconf["DBConfigs"]["postgresql"]["DBConnecter"]
UserName = dbconf["DBConfigs"]["postgresql"]["UserName"]
Password = dbconf["DBConfigs"]["postgresql"]["Password"]
ServerOrEndPoint = dbconf["DBConfigs"]["postgresql"]["ServerOrEndPoint"]
DatabaseName = dbconf["DBConfigs"]["postgresql"]["DatabaseName"]
engine = create_engine(f'{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}')
batch_id = ""


#Get the last batch ID from the database if its older than 30 mins then create a new one.
def get_batch_id_from_database():
    
    try:
        get_batch_id_query = 'select * from tbl_File_Batch_info ORDER BY file_date_time DESC LIMIT 1'
        with engine.connect() as conn:
            result = conn.execute(db.text(get_batch_id_query)).fetchall()
            
            if not result:
                batch_id = obj_plex.generate_batch_ID(10)
            else:
                batch_time_in_minutes = result[0][3]
                batch_id = result[0][2]
                time_difference = get_minutes_difference(batch_time_in_minutes)
            
                if(time_difference > 30):
                    batch_id = obj_plex.generate_batch_ID(10)
            
    except Exception as error: 
        print("Connection Refused")
        print(error)
    
    return batch_id
    

'''
Get the minutes based on the timestamp of last batch_id with the current timestamp 
and get the difference.
'''
def get_minutes_difference(database_time):
    time_fmt = "%Y-%m-%d %H:%M:%S"

    rounded_current_time = str(datetime.datetime.now()).split(".")[0]
    current_timestamp = datetime.datetime.strptime(rounded_current_time, time_fmt)

    rounded_database_time = str(database_time).split(".")[0]
    database_timestamp = datetime.datetime.strptime(rounded_database_time, time_fmt)
    
    time_difference = current_timestamp - database_timestamp
    time_difference_in_minutes = divmod(time_difference.total_seconds(), 60)[0]
    return(time_difference_in_minutes)


def insert_new_file_record(filename):
    batch_id = get_batch_id_from_database()
    try:
        insert_new_file_record_query = f"INSERT INTO tbl_File_Batch_info (file_name, batch_id, file_date_time, is_executed) VALUES ('{filename}','{batch_id}',CURRENT_TIMESTAMP, FALSE)"
        with engine.connect() as conn:
            insert_new_file_record = conn.execute(db.text(insert_new_file_record_query))
    except Exception as error: 
        print("Connection Refused")
        print(error)

#print(get_batch_id_from_database())

#insert_new_file_record('test5')
str_file_name = ""
obj_plex = PlexHelperFunctions()
llist = obj_plex.get_files()
for lst in llist:
    filename = lst.split('/')[-1]
    str_file_name_rounded = f"('{filename}'),"
    str_file_name += str_file_name_rounded


str_file_name += "('test1'),"
str_file_name += "('test2'),"
str_file_name += "('test3'),"
str_file_name += "('test4'),"

str_file_name = str_file_name[:-1]
#print(str_file_name)


'''

#filename_lst[-1] = str(filename_lst[-1]).split(',')[0]
filename_lst[-1] = str(filename_lst[-1])[:-1]
#print(filename_lst[-1])
#print(filename_lst)

for fl in filename_lst:
    str_file_name += fl

#print(str_file_name)
'''
'''try:
    get_batch_id_query = f"SELECT v FROM (VALUES {str_file_name} ) AS vs(v) WHERE v NOT IN (SELECT file_name FROM tbl_File_Batch_info)"
    with engine.connect() as conn:
        result = conn.execute(db.text(get_batch_id_query)).fetchall()
        print(f"File Names which are not present are {result}")
            
except Exception as error: 
    print("Connection Refused")
    print(error)

'''

obj_db.files_to_upload()