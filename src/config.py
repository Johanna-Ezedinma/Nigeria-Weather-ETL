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
        "City": "Lagos",
        "State": "Lagos",
        "Region": "South West"
    },
    {
        "City": "Ibadan",
        "State": "Oyo",
        "Region": "South West"
    },
    {
        "City": "Akure",
        "State": "Ondo",
        "Region": "South West"
    },
    {
        "City": "Enugu",
        "State": "Enugu",
        "Region": "South East"
    },
    {
        "City": "Umuahia",
        "State": "Abia",
        "Region": "South East"
    },
    {
        "City": "Awka",
        "State": "Anambra",
        "Region": "South East"
    },
    {
        "City": "Port Harcourt",
        "State": "Rivers",
        "Region": "South South"
    },
    {
        "City": "Calabar",
        "State": "Cross River",
        "Region": "South South"
    },
    {
        "City": "Abuja",
        "State": "FCT",
        "Region": "North Central"
    },
    {
        "City": "Jos",
        "State": "Plateau",
        "Region": "North Central"
    },
    {
        "City": "Kano",
        "State": "Kano",
        "Region": "North West"
    },
    {
        "City": "Maiduguri",
        "State": "Borno",
        "Region": "North East"
    }
]
