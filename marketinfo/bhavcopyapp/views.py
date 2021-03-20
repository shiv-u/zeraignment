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


def index(request):
    return HttpResponse("Hello World")