from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from bhavcopyapp import download_job


def start():
    dm = download_job.DownloadManager()
    scheduler = BackgroundScheduler()
    scheduler.add_job(dm.download_data, 'cron',hour=18,timezone="Asia/Kolkata")
    scheduler.start()