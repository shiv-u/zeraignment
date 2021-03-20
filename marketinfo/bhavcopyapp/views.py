from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http.response import JsonResponse
from datetime import datetime


import requests
import tempfile
import zipfile
import os
import pytz
import redis
import csv
import json

bse_link = "https://www.bseindia.com/download/BhavCopy/Equity/"
folder_dir = "./bhavcopyapp/files/"

redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT, db=0)

# Create your views here.

def get_data(request):
    # print(redis_instance.get("HDFC        "))

    return JsonResponse(json.loads(redis_instance.get("HDFC")))

def download_data(request):

    IST = pytz.timezone("Asia/Kolkata")
    current_date = datetime.now(IST)

    day = current_date.strftime("%d")
    month = current_date.strftime("%m")
    year = current_date.strftime("%y")

    zip_file_name = f"EQ{day}{month}{year}_CSV.ZIP"
    
    zip_file_name="EQ190321_CSV.ZIP"

    csv_file_name = ((zip_file_name.split(".")[0]).split("_")[0])+".CSV"

    hdr = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(bse_link+zip_file_name,stream=True,headers=hdr)
    

    if response.status_code != requests.codes.ok :
        return HttpResponse("Error downloading file")
    
    
    # print(os.listdir("./bhavcopyapp/"))

    with open(folder_dir+zip_file_name,"wb") as csv_file:
        # lf = tempfile.NamedTemporaryFile()
        for block in response.iter_content(1024*8):
            if not block:
                break

            csv_file.write(block)

        csv_file.close()

    with zipfile.ZipFile(folder_dir+zip_file_name, 'r') as zip_ref:
        zip_ref.extractall(folder_dir)
    
    os.remove(folder_dir+zip_file_name)

    save_to_redis(csv_file_name)

    return HttpResponse("data downloaded")
    

def save_to_redis(csv_file_name):
    
    with open(folder_dir+csv_file_name,"r") as csv_file:
        csv_reader =  csv.reader(csv_file) 
        headers = next(csv_reader)

        for row in csv_reader:
            redis_instance.set(row[1].strip(),json.dumps({"code":row[0],
                                                  "open":row[4],
                                                  "high":row[5],
                                                  "low":row[6],
                                                  "close":row[7]}))

    print(redis_instance.get("IFCI310312A "))
        






def index(request):
    return HttpResponse("Hello World")