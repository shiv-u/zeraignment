from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http.response import JsonResponse
from django.views.static import serve
from rest_framework.decorators import api_view
from django.http import FileResponse
from django.conf import settings
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



@api_view(['GET'])
def get_data(request):

    s = data_helper.StorageHelper() 

    ticker_name = (request.GET["stockname"].strip()).upper()
    ticker_record = s.get_records(ticker_name)

    

    if ticker_record[0]!=None:
        response = json.loads(ticker_record[0])
        date = ticker_record[1]
        csv_file_link = save_to_csv_file(response,ticker_name,date)
        return render(request,"results.html",{"data":response,
        "stock_name":ticker_name,
        "current_data":ticker_record[2],
        "date":date,
        "file_link":csv_file_link,
        })
    else:
        return render(request,"404.html",{"stock_name":ticker_name})


def save_to_csv_file(json_data,ticker_name,date):
    date = date.replace("/","")
    
    file_name = f'{ticker_name}{date}.csv'
    csv_record_file = f'./media/{file_name}'
    data_file = open(csv_record_file,"w")
    csv_writer = csv.writer(data_file)

    header = json_data.keys()
    csv_writer.writerow(header)
    csv_writer.writerow(json_data.values())

    data_file.close()

    return file_name

def index(request):
    return render(request,"index.html")