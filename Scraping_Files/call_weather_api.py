import requests
import json

def call_weather_api(url):
    """Calls weather API and returns info"""

    req = requests.get(url)
    return req

def write_weather (weatherData):
    """Retrieves weather information from openweathermap and stores as JSON"""

    req_weather = weatherData.text
    json_weather = json.loads(req_weather)
    print(json_weather)
    return json_weather

url="http://api.openweathermap.org/data/2.5/forecast?id=5344157&APPID=c8610607135716bfdae60b788f8e0c8d"
call_weather_api(url)
weatherData = call_weather_api(url)
json_weather=write_weather(weatherData)
