#tools/weather.py
import json
import requests
import re
from config.settings import weather_api_key
# -------------------------------------------------------------------------------------------
#                              BUILDING TOOLS
# -------------------------------------------------------------------------------------------

# # for weather
# with open('weather_api.json', 'r') as f:
#     api = json.load(f)
# weather_api = api["key"]

weather_api = weather_api_key
# for weather
with open('weather_api.json', 'r') as f:
    api = json.load(f)
weather_api = api["key"]

def weather(query, memory=None):
    match = re.search(r"in (\w+)", query.lower())
    if match:
        city = match.group(1)
    elif memory and "city" in memory:
        city = memory["city"]
    else:
        city = "chennai"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric"
    response = requests.get(url).json()
    # {
    #     "main": {"temp": 30},
    #     "weather": [{"description": "clear sky"}]
    # }

    try:
        temp = response["main"]["temp"]
        description = response["weather"][0]["description"]
        return f"temperature : {temp}{chr(176)}C description : {description}"
    except:
        return "weather not found"
