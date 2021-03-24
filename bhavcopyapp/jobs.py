from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from bhavcopyapp import download_job
from bhavcopyapp import reset_job


def start():
    download_manager = download_job.DownloadManager()
    data_resetter  = reset_job.DataResetter()
    scheduler = BackgroundScheduler()
    scheduler.add_job(download_manager.download_data, 'cron',hour=18,minute=00,timezone="Asia/Kolkata",id="download_job")
    scheduler.add_job(data_resetter.reset, 'cron',hour=23,minute=59,second=59,timezone="Asia/Kolkata",id="reset_job")
    # scheduler.add_job(download_manager.download_data, 'interval',seconds=30,timezone="Asia/Kolkata",id="download_job")
    scheduler.start()