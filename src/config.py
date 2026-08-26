import os
from pathlib import Path

from dotenv import load_dotenv


# Find the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from .env
load_dotenv(PROJECT_ROOT / ".env")

# API configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    raise ValueError(
        "OPENWEATHER_API_KEY is not set. "
        "Please create a .env file with your OpenWeather API key."
    )

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Database
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "weather.db"

# Make sure data directory exists
DATA_DIR.mkdir(exist_ok=True)

CITIES = [
    {
        "City": "Umuahia",
        "State": "Abia",
        "Region": "South East"
    },
    {
        "City": "Yola",
        "State": "Adamawa",
        "Region": "North East"
    },
    {
        "City": "Uyo",
        "State": "Akwa Ibom",
        "Region": "South South"
    },
    {
        "City": "Awka",
        "State": "Anambra",
        "Region": "South East"
    },
    {
        "City": "Bauchi",
        "State": "Bauchi",
        "Region": "North East"
    },
    {
        "City": "Yenagoa",
        "State": "Bayelsa",
        "Region": "South South"
    },
    {
        "City": "Makurdi",
        "State": "Benue",
        "Region": "North Central"
    },
    {
        "City": "Maiduguri",
        "State": "Borno",
        "Region": "North East"
    },
    {
        "City": "Calabar",
        "State": "Cross River",
        "Region": "South South"
    },
    {
        "City": "Asaba",
        "State": "Delta",
        "Region": "South South"
    },
    {
        "City": "Abakaliki",
        "State": "Ebonyi",
        "Region": "South East"
    },
    {
        "City": "Benin City",
        "State": "Edo",
        "Region": "South South"
    },
    {
        "City": "Ado Ekiti",
        "State": "Ekiti",
        "Region": "South West"
    },
    {
        "City": "Enugu",
        "State": "Enugu",
        "Region": "South East"
    },
    {
        "City": "Gombe",
        "State": "Gombe",
        "Region": "North East"
    },
    {
        "City": "Owerri",
        "State": "Imo",
        "Region": "South East"
    },
    {
        "City": "Dutse",
        "State": "Jigawa",
        "Region": "North West"
    },
    {
        "City": "Kaduna",
        "State": "Kaduna",
        "Region": "North West"
    },
    {
        "City": "Kano",
        "State": "Kano",
        "Region": "North West"
    },
    {
        "City": "Katsina",
        "State": "Katsina",
        "Region": "North West"
    },
    {
        "City": "Birnin Kebbi",
        "State": "Kebbi",
        "Region": "North West"
    },
    {
        "City": "Lokoja",
        "State": "Kogi",
        "Region": "North Central"
    },
    {
        "City": "Ilorin",
        "State": "Kwara",
        "Region": "North Central"
    },
    {
        "City": "Lagos",
        "State": "Lagos",
        "Region": "South West"
    },
    {
        "City": "Lafia",
        "State": "Nasarawa",
        "Region": "North Central"
    },
    {
        "City": "Minna",
        "State": "Niger",
        "Region": "North Central"
    },
    {
        "City": "Abeokuta",
        "State": "Ogun",
        "Region": "South West"
    },
    {
        "City": "Akure",
        "State": "Ondo",
        "Region": "South West"
    },
    {
        "City": "Osogbo",
        "State": "Osun",
        "Region": "South West"
    },
    {
        "City": "Ibadan",
        "State": "Oyo",
        "Region": "South West"
    },
    {
        "City": "Jos",
        "State": "Plateau",
        "Region": "North Central"
    },
    {
        "City": "Port Harcourt",
        "State": "Rivers",
        "Region": "South South"
    },
    {
        "City": "Sokoto",
        "State": "Sokoto",
        "Region": "North West"
    },
    {
        "City": "Jalingo",
        "State": "Taraba",
        "Region": "North East"
    },
    {
        "City": "Damaturu",
        "State": "Yobe",
        "Region": "North East"
    },
    {
        "City": "Gusau",
        "State": "Zamfara",
        "Region": "North West"
    },
    {
        "City": "Abuja",
        "State": "FCT",
        "Region": "North Central"
    }
]