from django.http import StreamingHttpResponse
from django.shortcuts import render
import time
import requests

def home(request):
    return render(request, "weather.html")


def weather_stream(request):
    city = "Delhi"   # fixed city for beginners

    def event_stream():
        while True:
            # Call the weather API
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY&units=metric"
            data = requests.get(url).json()

            # Simple text output
            if "main" in data:
                temp = data["main"]["temp"]
                condition = data["weather"][0]["description"]
                msg = f"{city} Weather → {temp}°C, {condition}"
            else:
                msg = "Error fetching weather data"

            yield f"data: {msg}\n\n"
            time.sleep(5)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
