from django.http import StreamingHttpResponse
from django.shortcuts import render
import time
import requests
import asyncio

# Map city to lat/lon
CITY_COORDS = {
    "Delhi": (28.7041, 77.1025),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
}

def weather_stream(request):
    city = request.GET.get("city")
    lat, lon = CITY_COORDS.get(city, CITY_COORDS["Mumbai"])

    def event_stream():
        while True:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

            try:
                data = requests.get(url).json()
                weather = data.get("current_weather", {})

                temp = weather.get("temperature")
                wind = weather.get("windspeed")

                if temp is not None:
                    message = f"{city} Weather → {temp}°C, Wind {wind} km/h"
                else:
                    message = "Weather data unavailable"

            except Exception as e:
                message = "Server error fetching data"

            yield f"data: {message}\n\n"
            time.sleep(2)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")

def home(request):
    return render(request, "weather.html")