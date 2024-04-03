import os
import glob
import json
import random, string
from ftplib import FTP_TLS
from tqdm import tqdm
from dotenv import load_dotenv
import ftplib
from pathlib import Path



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