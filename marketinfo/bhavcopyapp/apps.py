from django.apps import AppConfig


class BhavcopyappConfig(AppConfig):
    name = 'bhavcopyapp'

    def ready(self):
        from bhavcopyapp import jobs
        print("Starting download")
        jobs.start()


