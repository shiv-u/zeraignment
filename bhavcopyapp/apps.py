from django.apps import AppConfig


class BhavcopyappConfig(AppConfig):
    name = 'bhavcopyapp'

    def ready(self):
        from bhavcopyapp import downloader
        print("Starting download")
        downloader.start()


