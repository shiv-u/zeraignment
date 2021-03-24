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



class StorageHelper:

    def __init__(self):

        self.bse_link = "https://www.bseindia.com/download/BhavCopy/Equity/"
        self.folder_dir = "./bhavcopyapp/files/"

        #comment while running in localhost or in docker
        # self.redis_instance = redis.from_url(os.environ.get("REDIS_URL"))
        # uncomment while running in localhost or using docker
        self.redis_instance  = redis.StrictRedis(host=settings.REDIS_HOST,port=6379,db=0)
        

        IST = pytz.timezone("Asia/Kolkata")

        self.current_date = datetime.now(IST)
        self.previous_date = self.current_date - timedelta(days=1)

        self.current_day = self.current_date.strftime("%d")
        self.current_month = self.current_date.strftime("%m")
        self.current_year = self.current_date.strftime("%y")

        self.previous_day = self.previous_date.strftime("%d")
        self.previous_month = self.previous_date.strftime("%m")
        self.previous_year = self.previous_date.strftime("%y")

       

        self.current_zip_file_name = f"EQ{self.current_day}{self.current_month}{self.current_year}_CSV.ZIP"


        self.current_csv_file_name = ((self.current_zip_file_name.split(".")[0]).split("_")[0])+".CSV"

        self.previous_zip_file_name = f"EQ{self.previous_day}{self.previous_month}{self.previous_year}_CSV.ZIP"

        self.previous_csv_file_name = ((self.previous_zip_file_name.split(".")[0]).split("_")[0])+".CSV"

    def save_to_redis(self,csv_file_name,data_mode):

       
        
        with open(self.folder_dir+csv_file_name,"r") as csv_file:
            csv_reader =  csv.reader(csv_file)
            headers = next(csv_reader)

            for row in csv_reader:
                self.redis_instance.set(row[1].strip(),json.dumps({"code":row[0],
                                                    "open":row[4],
                                                    "high":row[5],
                                                    "low":row[6],
                                                    "close":row[7]}))
            
            self.redis_instance.set(data_mode,"True")
            if data_mode == "current_data":
                date = self.current_date.strftime("%d/%m/%y")
            else:
                date = self.previous_date.strftime("%d/%m/%y")

            

            self.redis_instance.set("date",date)
            
    
    def get_records(self,record_name):
        
        if (self.redis_instance.get("current_data") is None) or (self.redis_instance.get("current_data").decode() == "False"):

            # fetch previous day record and send the response back

           # self.download_data("current_data",self.current_zip_file_name,self.current_csv_file_name)

            
            print("Current data not available")

            if (self.redis_instance.get("previous_data") is None or self.redis_instance.get("previous_data").decode() == "False"):
                    #if previous day record is not found return (None,false)
                print("Downloading previous data")
                self.download_data("previous_data",self.previous_zip_file_name,self.previous_csv_file_name)

                if self.redis_instance.get("previous_data").decode() == "False":
                        return (None,"",False)

                else:
                    date = self.redis_instance.get("date").decode()
                    return (self.redis_instance.get(record_name),date,False)
                
            else:
                # return previous day records if found
                print("Returning previous day's data")
                date = self.redis_instance.get("date").decode()
                return (self.redis_instance.get(record_name),date,False)
            
        print("returning current day's data")
        date = self.redis_instance.get("date").decode()
        return (self.redis_instance.get(record_name),date,True)




# Create your views here.

    def download_data(self,data_mode,zip_file_name,csv_file_name):

        
        print(f"Downloading {data_mode} data")
        

        hdr = {'User-Agent': 'Mozilla/5.0'}

        response = requests.get(self.bse_link+zip_file_name,stream=True,headers=hdr)
        

        if response.status_code != requests.codes.ok :
            # if previous data is not available return no data
            self.redis_instance.set(data_mode,"False")
            return 
  
        # print(os.listdir("./bhavcopyapp/"))

        with open(self.folder_dir+zip_file_name,"wb") as csv_file:
            # lf = tempfile.NamedTemporaryFile()
            for block in response.iter_content(1024*8):
                if not block:
                    break

                csv_file.write(block)

            csv_file.close()

        with zipfile.ZipFile(self.folder_dir+zip_file_name, 'r') as zip_ref:
            zip_ref.extractall(self.folder_dir)
        
        os.remove(self.folder_dir+zip_file_name)

        print(f"{data_mode} Data downloaded")
        self.save_to_redis(csv_file_name,data_mode,)



        
            

