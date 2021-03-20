from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http.response import JsonResponse
from datetime import datetime

from bhavcopyapp import data_helper

import requests
import tempfile
import zipfile
import os
import pytz
import redis
import csv
import json

s = data_helper.StorageHelper()


def get_data(request):
    # print(redis_instance.get("HDFC        "))


    ticker_name = request.GET["name"].strip()
    ticker_record = s.get_records(ticker_name)

    

    if ticker_record[0]!=None:
        response = json.loads(ticker_record[0])
        response["current_data"]=ticker_record[1]
        return JsonResponse(response)
    else:
        return JsonResponse({"data":ticker_record[0],"previous_data":False,"current_data":False,"code":404})



    # return JsonResponse(json.loads(redis_instance.get("HDFC")))

def download_data(request):
    pass

    # IST = pytz.timezone("Asia/Kolkata")
    # current_date = datetime.now(IST)

    # day = current_date.strftime("%d")
    # month = current_date.strftime("%m")
    # year = current_date.strftime("%y")

    # zip_file_name = f"EQ{day}{month}{year}_CSV.ZIP"
    
    # zip_file_name="EQ190321_CSV.ZIP"

    # csv_file_name = ((zip_file_name.split(".")[0]).split("_")[0])+".CSV"

    # hdr = {'User-Agent': 'Mozilla/5.0'}

    # response = requests.get(bse_link+zip_file_name,stream=True,headers=hdr)
    

    # if response.status_code != requests.codes.ok :
    #     return HttpResponse("Error downloading file")
    
    
    # # print(os.listdir("./bhavcopyapp/"))

    # with open(folder_dir+zip_file_name,"wb") as csv_file:
    #     # lf = tempfile.NamedTemporaryFile()
    #     for block in response.iter_content(1024*8):
    #         if not block:
    #             break

    #         csv_file.write(block)

    #     csv_file.close()

    # with zipfile.ZipFile(folder_dir+zip_file_name, 'r') as zip_ref:
    #     zip_ref.extractall(folder_dir)
    
    # os.remove(folder_dir+zip_file_name)

    # save_to_redis(csv_file_name)

    # return HttpResponse("data downloaded")
    







def index(request):
    return HttpResponse("Hello World")