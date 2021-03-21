from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('download',views.download_data,name="download_data"),
    path("get_data",views.get_data,name="get_data"),
    path("equity",views.servefiles,name="serve_files")

]