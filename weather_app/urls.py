from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),  
    path('stream/', views.weather_stream),  
]
