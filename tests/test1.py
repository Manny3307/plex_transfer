from pathlib import Path
from ftplib import FTP_TLS
from tqdm import tqdm
from dotenv import load_dotenv
import ftplib
import os
import pathlib
import json 
from sqlalchemy import create_engine
import sqlalchemy as db
import datetime, dateutil
from helpers.db_helpers import dbFunction
from helpers.file_transfer_helpers import PlexHelperFunctions
from helpers.ftp_helpers import FTPHelpers
import glob
from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
import math

obj_plex = PlexHelperFunctions()
#obj_db = dbFunction()

DBConfig = open("../conf/db_conf.json")
dbconf = json.load(DBConfig)
DBConnector = dbconf["DBConfigs"]["postgresql"]["DBConnecter"]
UserName = dbconf["DBConfigs"]["postgresql"]["UserName"]
Password = dbconf["DBConfigs"]["postgresql"]["Password"]
ServerOrEndPoint = dbconf["DBConfigs"]["postgresql"]["ServerOrEndPoint"]
DatabaseName = dbconf["DBConfigs"]["postgresql"]["DatabaseName"]
engine = create_engine(f'{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}')
obj_plex = PlexHelperFunctions()

obj_ftp = FTPHelpers()

#ftps.dir()

def files_to_upload_to_plex():
        files_list = []
        str_file_name = ""
        file_list = obj_plex.get_files()
        #get the list of the files in the base folder or source folder
        for lst in file_list:
            filename = lst.split('/')[-1]
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
                    print(f"Following are the files to upload {files_to_upload}")
                    for fl_name in files_to_upload:
                        fl_name = str(fl_name).replace("(","").replace(")","").replace(",","").replace("'","")
                        files_list.append(fl_name)
                    
                    print(files_list)
                    #for file_n in files_list:
                        #self.insert_new_file_record(file_n)

        except Exception as error: 
            print("Connection Refused")
            print(error)

        return files_to_upload

#print(files_to_upload_to_plex())

'''
for file_n in f_names:
    complete_file_path = os.path.join(root,file_n)
    filesize = int(os.path.getsize(complete_file_path))
    TheFile = open(complete_file_path, 'rb')
    with tqdm(unit = 'blocks', unit_scale = True, leave = False, miniters = 1, desc = f'Uploading {selected_folder} {file_n}......', total = filesize) as tqdm_instance:
        ftps.storbinary(f'STOR {file_n}', TheFile , 2048, callback = lambda sent: tqdm_instance.update(len(sent)))'''



#files = obj_plex.get_files()

'''conf_details = open("../conf/conf.json")
genconf = json.load(conf_details)
base_folder_name = genconf["base_folder"]["Folder"]

file_list = glob.glob(f"{base_folder_name}/*")

for f in file_list:
    if("'" in f):
        file_name = f.split("/")[-1]
        repl_file = file_name.replace("'","")
        repl_file = f"{base_folder_name}/{repl_file}"
        #print(f"{file_name} - {repl_file}")
        print(f"{f} - {repl_file}")
        os.rename(f, repl_file)'''


'''string = "Ge;ek * s:fo ! r;Ge * e*k:s !"
 
test_str = ''.join(letter for letter in string if letter.isalnum())
print(test_str)
'''
#test_string = "so desperate she can't pee!    wetting my pink panties... oops!.mp4"
#test_str = ''.join(letter for letter in test_string if letter.isalnum())
#print(test_str)

'''special_chars = ['!',"#","$","%","&","'","(",")","*","+",",","/",":",";","<","=",">","?","@","[",']',"^",'_',"`",'{',"|",'}','~',"","Ç","ü","é","â","ä","à","å","ç","ê","ë","è","ï","î","ì","æ","Æ","ô","ö","ò","û","ù","ÿ","¢","£","¥","P","ƒ","á","í","ó","ú","ñ","Ñ","¿","¬","½","¼","¡","«","»","¦","ß","µ","±","°","•","·","²","€","„","…","†","‡","ˆ","‰","Š","‹","Œ","‘","’","“","”","–","—","˜","™","š","›","œ","Ÿ","¨","!"]

test_string = "so desperate she can't pee!   wetting my \ pink panties... oops!.mp4"
test_string = test_string.replace('\\', '')  
#test_str = ''.join(letter for letter in test_string if letter.isalnum())
test_string = ''.join(i for i in test_string if not i in special_chars)
print("Resultant list is : " + str(test_string))'''


#print(obj_plex.upload_to_plex())
#masm_files = obj_plex.get_files()
#obj_plex.remove_special_characters_from_filename(masm_files)
#obj_ftp = ftp
#obj_plex.upload_to_plex()
#obj_ftp.upload_to_plex()
#obj_db = dbFunction()
#obj_db.files_to_upload()

#home_folder = self.get_conf_val("home_folder")

#obj_ftp.upload_to_plex()

'''account = MyPlexAccount('mannydaniels1@gmail.com', 'Pikolo_3307')
plex = account.resource('192.168.0.168').connect()  # returns a PlexServer instance
print(plex)
'''
'''
baseurl = 'http://192.168.0.168:32400'
token = 'fxa_vX4sgNNkSzNbMiyP'
plex = PlexServer(baseurl, token)

vids  = plex.library.section('Manny')
print(vids.search('faphouse'))
'''
#print(obj_plex.include_file_names("tempfile_781925218_2"))

'''file_size = ftps.size('/New/faphouse.com-i-want-to-drink-your-orgasm-sweetheart-p1080.mp4')
file_size = file_size / (1024 * 1024)
rounded_filesize = round(file_size,2)
if(rounded_filesize > 1000):
     rounded_filesize = rounded_filesize / 1000

print(f'File Size at Plex Server {ftps.size("/New/faphouse.com-i-want-to-drink-your-orgasm-sweetheart-p1080.mp4")}')


fl = os.stat('/media/manny/Backups/MASM/faphouse.com-i-want-to-drink-your-orgasm-sweetheart-p1080.mp4')
print(f'File Size at local system {fl.st_size}')
'''
#obj_ftp.validate_plex_server_uploads()

'''
from os import walk
folder_path = ""
# folder path
dir_path = r'/media/manny/Backups/MASM'

# list to store files name
res = []
for (dir_path, dir_names, file_names) in walk(dir_path):
    for fln in file_names:
        res.append(os.path.join(dir_path,fln))
    
for r in res:
    if "dika_badony.zip" in r:
        #folder_path = os.path.abspath(r)
        folder_path = os.path.dirname(os.path.abspath(r))




print(folder_path)'''
#/media/manny/Backups/MASM/Flexi/dika_badony.zip

'''dir_path = r'/media/manny/Backups/MASM'
fl = glob.glob(f"{dir_path}/*/", recursive = True)
print(fl)
'''
'''
str_file_name = ""
import os
import os.path
import pandas as pd

dir_path = r'/media/manny/Backups/MASM'
for path, subdirs, files in os.walk(dir_path):
    for name in files:
        #print(os.path.join(path, name))
        str_file_name_rounded = f"('{name}'),"
        str_file_name += str_file_name_rounded


data = list()
for root, dirs, files in os.walk(dir_path):
    for filename in files:
        nm, ext = os.path.splitext(filename)
        fullpath = os.path.abspath(root)
        data.append((filename, fullpath))
df1 = pd.DataFrame(data, columns=['filename', 'fullpath'])
#print(df1)


#print(str_file_name[:-1])
str_file_name = str_file_name[:-1]

DBConfig = open("/home/manny/plex_transfer/helpers/helper_db_config.json")
dbconf = json.load(DBConfig)
DBConnector = dbconf["DBConfigs"]["postgresql"]["DBConnecter"]
UserName = dbconf["DBConfigs"]["postgresql"]["UserName"]
Password = dbconf["DBConfigs"]["postgresql"]["Password"]
ServerOrEndPoint = dbconf["DBConfigs"]["postgresql"]["ServerOrEndPoint"]
DatabaseName = dbconf["DBConfigs"]["postgresql"]["DatabaseName"]
engine = create_engine(f'{DBConnector}://{UserName}:{Password}@{ServerOrEndPoint}/{DatabaseName}')
special_chars = ["(",")","'",","]
counter = 1
get_batch_id_query = f"SELECT v FROM (VALUES {str_file_name}) AS vs(v) WHERE v NOT IN (SELECT file_name FROM tbl_File_Batch_info)"
with engine.connect() as conn:
    files_to_upload = conn.execute(db.text(get_batch_id_query)).fetchall()

file_with_folder = []
file_with_folder_txt = "" 

for fl_name in files_to_upload:
    fl_name_txt = ''.join(i for i in fl_name if not i in special_chars)
    file_with_folder.append(fl_name_txt)
  



filtered_df = df1[df1["filename"].isin(file_with_folder)]
#print(filtered_df)

#for index, row in filtered_df.iterrows():
#    print(row["filename"], row["fullpath"])

'''
#obj_db = dbFunction()
#obj_db.files_to_upload()
obj_ftp.upload_to_plex()
#

'''

ftps = FTP_TLS()
ftps = ftplib.FTP('192.168.0.168', 'Manny', 'manny')

FTP_Path = "/New"
ftps.cwd(FTP_Path)

if 'zips' in ftps.nlst():
     print("hey")




folder = '/New/Flexi/test_recur'
actual_folder_name = folder.split('/')
actual_folder_name = actual_folder_name[len(actual_folder_name) - 1]
print(actual_folder_name)
if(actual_folder_name in ftps.nlst()):
     print("exists")
else:
     print("not exists")

#path = "/media/manny/Backups/MASM"
#path = path.replace("/media/manny/Backups/MASM", "/New")
#print(path)



df2 = pd.DataFrame(files_dont_exist, columns=['filename'])
#print(df2)

result = pd.concat([df2, df1], axis=1, join="inner")
print(result)
result.to_csv("./result.csv")
'''
'''dir_path = r'/media/manny/Backups/MASM/Flexi'
if os.path.isdir(dir_path):
    print("Yes")
else:
    print("No")'''
'''
def get_folder_name(folder_name):
     folder_n = folder_name.split('/')
     file_name = folder_n[len(folder_n) - 1]
     folder = file_name.split('.')
     folders_name = folder[0]
     return folders_name
     

from zipfile import ZipFile
zip_folder = obj_plex.get_conf_val("zips_folder")
zip_files = obj_plex.get_files()
base_folder_name = obj_plex.get_conf_val("base_folder")
file_list = glob.glob(f"{base_folder_name}/*.zip")
print(zip_folder, get_folder_name(file_list[0]))
with ZipFile(file_list[0], 'r') as zObject:
     zObject.extractall(path=f"{zip_folder}/{get_folder_name(file_list[0])}")
'''
'''def list_files(filepath, filetype):
   paths = []
   for root, dirs, files in os.walk(filepath):
      for file in files:
         if file.lower().endswith(filetype.lower()):
            paths.append(os.path.join(root, file))
   return(paths)

base_folder_name = obj_plex.get_conf_val("base_folder")
my_files_list = list_files(base_folder_name, '.zip')
for fl in my_files_list:
    print(fl)'''


#obj_plex.extract_zip_files()