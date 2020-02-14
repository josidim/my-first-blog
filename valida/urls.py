#from django.conf.urls.defaults import * 


from django.urls import path
from . import views





urlpatterns = [
	
	path('', views.upload_csv, name='upload_csv'),
	#path('', views.index, name='index'),
]