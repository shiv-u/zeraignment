from django.shortcuts import render
from django.http import HttpResponse

from datetime import datetime


import requests
import tempfile
import zipfile
import os
import pytz


bse_link = "https://www.bseindia.com/download/BhavCopy/Equity/"
folder_dir = "./bhavcopyapp/files/"
# Create your views here.

def download_data(request):

    IST = pytz.timezone("Asia/Kolkata")
    current_date = datetime.now(IST)

    day = current_date.strftime("%d")
    month = current_date.strftime("%m")
    year = current_date.strftime("%y")

    filename = f"EQ{day}{month}{year}_CSV.ZIP"
    # filename="EQ180321_CSV.ZIP"

    hdr = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(bse_link+filename,stream=True,headers=hdr)
    

    if response.status_code != requests.codes.ok :
        # send a 404 view
        return HttpResponse("Error downloading file")
    zip_file_name = "EQ190321_CSV.ZIP"
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

    return HttpResponse("data downloaded")
    






def index(request):
    return HttpResponse("Hello World")