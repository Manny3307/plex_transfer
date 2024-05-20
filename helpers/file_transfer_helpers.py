import os
import glob
import json
import random, string
from ftplib import FTP_TLS
from tqdm import tqdm
from dotenv import load_dotenv
import ftplib
from pathlib import Path
import pandas as pd
from zipfile import ZipFile


#Class to execute the Plex Helper Functions
class PlexHelperFunctions:
    
    def __inti__(self):
        conf_details = open("/home/manny/plex_transfer/helpers/helper_config.json")
        genconf = json.load(conf_details)
        base_folder_name = genconf["base_folder"]["Folder"]

    #Get Configuration Value
    def get_conf_val(self, conf_holder):
        holder_value = ""
        conf_details = open("/home/manny/plex_transfer/helpers/helper_config.json")
        genconf = json.load(conf_details)
        holder_value = genconf[f"{conf_holder}"]["Folder"]
        return holder_value
    
    #Get the list of files in a directory
    def get_files(self):
        base_folder_name = self.get_conf_val("base_folder")
        file_list = glob.glob(f"{base_folder_name}/*")
        return file_list

    #Get the last file added in a directory
    def get_last_file(self):
        base_folder_name = self.get_conf_val("base_folder")
        file_list = glob.glob(f"{base_folder_name}/*")
        latest_file = max(file_list, key=os.path.getctime)
        return latest_file
    
    #Get a Unique Batch ID
    def generate_batch_ID(self, length):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

    #Get rid of any special characters that may be present in the file name except space and dot(.).
    def remove_special_chars_from_file_name(self, file_name):
        special_chars = ['!',"#","$","%","&","'","(",")","*","+",",","/",":",";","<","=",">","?","@","[",']',"^","`",'{',"|",'}','~',"","Ç","ü","é","â","ä","à","å","ç","ê","ë","è","ï","î","ì","æ","Æ","ô","ö","ò","û","ù","ÿ","¢","£","¥","ƒ","á","í","ó","ú","ñ","Ñ","¿","¬","½","¼","¡","«","»","¦","ß","µ","±","°","•","·","²","€","„","…","†","‡","ˆ","‰","Š","‹","Œ","‘","’","“","”","–","—","˜","™","š","›","œ","Ÿ","¨","!"]
        file_name = file_name.replace('\\', '')  
        file_name = ''.join(i for i in file_name if not i in special_chars)
        return file_name
    
    #Get the filename without the complete path
    def strip_folder_name(self, complete_path):
        folder_name = complete_path.split("/")

        return folder_name[len(folder_name) - 1]
    
    #Remove any special charcaters from the file name
    def remove_special_characters_from_filename(self, file_list):
        for f in file_list:
            file_name_without_path = f.split("/")[-1]
            file_name_without_path = self.remove_special_chars_from_file_name(file_name_without_path)
            base_folder_name = self.get_conf_val("base_folder")
            repl_file = f"{base_folder_name}/{file_name_without_path}"
            os.rename(f, repl_file)
    
    #Only Include the media files and leave the rest
    def include_file_names(self, file_name):
        included_file_name = ""
        included_file_list_extensions = ['mov', 'avi', 'mp4', 'swf', 'flv', 'f4v', 'wmv', 'webm', 'avchd', 'mkv', 'm2ts', 'tiff', 'flac', 'gif', 'jpeg', 'jpg', 'mp3', 'svg', 'wav', 'zip']
        file_extension = file_name.split('.')[-1]
        if(file_extension in included_file_list_extensions):
            included_file_name = file_name
        else:
            included_file_name = "Not a valid file"
        return included_file_name

    #Get the path of the given file
    def get_folder_path(self, file_name):
        folder_path = ""
        # folder path
        base_folder_name = self.get_conf_val("base_folder")
        dir_path = base_folder_name

        # list to store files name
        file_list = []
        for (dir_path, dir_names, file_names) in os.walk(dir_path):
            for fln in file_names:
                file_list.append(os.path.join(dir_path,fln))
            
        for fl in file_list:
            if file_name in fl:
                folder_path = os.path.dirname(os.path.abspath(fl))

        return folder_path
    
    #Using os.walk to get all the files in the main directory and sub-directories.
    def get_all_files(self):
        base_folder_name = self.get_conf_val("base_folder")
        filenames_with_fullpath = list()
        for root, dirs, files in os.walk(base_folder_name):
            for filename in files:
                nm, ext = os.path.splitext(filename)
                fullpath = os.path.abspath(root)
                filenames_with_fullpath.append((filename, fullpath))
        
        df1 = pd.DataFrame(filenames_with_fullpath, columns=['filename', 'fullpath'])
        return df1
    
    #Get all files to run the query over DB to filter out existing filenames in the data base.
    def get_all_filenames_for_query(self):
        str_file_name = ""
        base_folder_name = self.get_conf_val("base_folder")
        for path, subdirs, files in os.walk(base_folder_name):
            for name in files:
                actual_name = name
                Actual_fl_name = f'{path}/{actual_name}'
                filename = self.remove_special_chars_from_file_name(str(actual_name))
                chars_removed_fl_name = f'{path}/{filename}'
                os.rename(Actual_fl_name, chars_removed_fl_name)
                str_file_name_rounded = f"('{actual_name}'),"
                str_file_name += str_file_name_rounded
        
        str_file_name = str_file_name[:-1]
        return str_file_name
    
    #Create a folder name for the zip file to extract.
    def create_folder_name(self, folder_name):
        folder_n = folder_name.split('/')
        file_name = folder_n[len(folder_n) - 1]
        folder = file_name.split('.')
        folders_name = folder[0]
        return folders_name
    
    #Unzip the files to the given zip folder
    def extract_zip_files(self):
        zip_folder = self.get_conf_val("zips_folder")
        base_folder_name = self.get_conf_val("base_folder")
        zip_file_list = self.list_files(base_folder_name, '.zip')
        for zip_file in zip_file_list:
            if(self.chk_folder_exist(zip_file) == False):
                with ZipFile(zip_file, 'r') as zObject:
                    zObject.extractall(path=f"{zip_folder}/{self.create_folder_name(zip_file)}")
                    print(f"Extracting {zip_file}")

    #Get all the files with the given extension
    def list_files(self, filepath, filetype):
        paths = []
        for root, dirs, files in os.walk(filepath):
            for file in files:
                if file.lower().endswith(filetype.lower()):
                    paths.append(os.path.join(root, file))
        return paths
    
    #Check if the extracted zip folder is already present
    def chk_folder_exist(self, file_path):
        zip_folder_Path = self.get_conf_val("zips_folder")
        folder_name  = self.create_folder_name(file_path)
        zip_folder_name = f"{zip_folder_Path}/{folder_name}"
        is_folder_Exist = os.path.exists(zip_folder_name)
        return is_folder_Exist