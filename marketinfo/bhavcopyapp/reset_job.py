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



class DataResetter:
    def __init__(self):
        # self.redis_instance = redis.from_url(os.environ.get("REDIS_URL"))
        self.redis_instance  = redis.StrictRedis(host="localhost",port=6379,db=0)
    def reset(self):
        print("resetting current data")
        self.redis_instance.set("current_data","False")
        