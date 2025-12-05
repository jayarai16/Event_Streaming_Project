from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),  
    path('weather_stream/', views.weather_stream, name="weather_stream"),  
]
