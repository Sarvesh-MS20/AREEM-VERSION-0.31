from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("api_key")
weather_api_key = os.getenv("weather_api_key")