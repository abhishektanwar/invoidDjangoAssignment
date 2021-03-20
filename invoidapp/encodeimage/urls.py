from django.contrib import admin
from django.urls import path,include
from encodeimage import views
urlpatterns = [
	path('', views.imageEncode),
]
