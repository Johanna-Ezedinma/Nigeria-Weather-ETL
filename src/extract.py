import requests
from datetime import datetime, timezone

from src.config import API_KEY, BASE_URL


def extract_weather(city, state, region):
    """
    Extract current weather data for one Nigerian city.
    """

    params = {
        "q": f"{city},NG",
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as error:
        print(f"Error retrieving {city}: {error}")
        return None

    data = response.json()

    weather_record = {
        "City": city,
        "State": state,
        "Region": region,
        "Country": "Nigeria",

        "Latitude": data["coord"]["lat"],
        "Longitude": data["coord"]["lon"],

        "Temperature_C": data["main"]["temp"],
        "Feels_Like_C": data["main"]["feels_like"],
        "Min_Temperature_C": data["main"]["temp_min"],
        "Max_Temperature_C": data["main"]["temp_max"],

        "Humidity_Percent": data["main"]["humidity"],
        "Pressure_hPa": data["main"]["pressure"],

        "Weather_Condition": data["weather"][0]["main"],
        "Weather_Description": data["weather"][0]["description"],

        "Wind_Speed_mps": data["wind"]["speed"],
        "Wind_Direction_Deg": data["wind"].get("deg"),

        "Cloudiness_Percent": data["clouds"]["all"],

        "Visibility_km": data.get("visibility", None) / 1000
        if data.get("visibility") is not None
        else None,

        "Weather_Timestamp": data["dt"],

        "Extracted_At_UTC": datetime.now(timezone.utc)
    }

    return weather_record