

from django.http import HttpResponse
from django.conf import settings

from datetime import datetime
from datetime import timedelta
import requests
import tempfile
import zipfile
import os
import pytz
import redis
import csv
import json



class DownloadManager:

    def __init__(self):

        self.bse_link = "https://www.bseindia.com/download/BhavCopy/Equity/"
        self.folder_dir = "./bhavcopyapp/files/"

        #comment while running in localhost or in docker
        # self.redis_instance = redis.from_url(os.environ.get("REDIS_URL"))
        # uncomment while running in localhost or using docker
        self.redis_instance  = redis.StrictRedis(host=settings.REDIS_HOST,port=6379,db=0)
        

        IST = pytz.timezone("Asia/Kolkata")

        self.current_date = datetime.now(IST)
    
        self.day = self.current_date.strftime("%d")
        self.month = self.current_date.strftime("%m")
        self.year = self.current_date.strftime("%y")

    

        self.zip_file_name = f"EQ{self.day}{self.month}{self.year}_CSV.ZIP"

        self.csv_file_name = ((self.zip_file_name.split(".")[0]).split("_")[0])+".CSV"

      
    def save_to_redis(self,csv_file_name):
        
        with open(self.folder_dir+csv_file_name,"r") as csv_file:
            csv_reader =  csv.reader(csv_file) 
            headers = next(csv_reader)

            for row in csv_reader:
                self.redis_instance.set(row[1].strip(),json.dumps({"code":row[0],
                                                    "open":row[4],
                                                    "high":row[5],
                                                    "low":row[6],
                                                    "close":row[7]}))
            
            self.redis_instance.set("current_data","True")
            self.redis_instance.set("date",self.current_date.strftime("%d/%m/%y"))
    
    
    def download_data(self):

        try:

            
            print("Downloading current data",self.current_date)
            

            hdr = {'User-Agent': 'Mozilla/5.0'}

            response = requests.get(self.bse_link+self.zip_file_name,stream=True,headers=hdr)
            

            if response.status_code != requests.codes.ok :
                # if current data is not available
                print("Still data is not available for",self.current_date)
                self.redis_instance.set("current_data","False")
                return 
    
            # print(os.listdir("./bhavcopyapp/"))
            
            print(f"status{response.status_code},zip file {self.zip_file_name}")
            with open(self.folder_dir+self.zip_file_name,"wb") as zip_file:
                print("inside opening folder")
                # lf = tempfile.NamedTemporaryFile()
                for block in response.iter_content(1024*8):
                    if not block:
                        break

                    zip_file.write(block)

                zip_file.close()

            with zipfile.ZipFile(self.folder_dir+self.zip_file_name, 'r') as zip_ref:
                zip_ref.extractall(self.folder_dir)
            
            if os.path.exists(self.folder_dir+self.zip_file_name):
                os.remove(self.folder_dir+self.zip_file_name)

            print("Current Data downloaded")
            self.save_to_redis(self.csv_file_name)
        except Exception as e:
            print("exception is ",e)




        
            

