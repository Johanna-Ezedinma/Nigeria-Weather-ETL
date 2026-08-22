import sqlite3

from src.config import API_KEY, CITIES, DB_PATH
from src.extract import extract_weather
from src.transform import transform_weather_data
from src.load import (
    create_database,
    load_cities,
    load_weather_data
)


def run_pipeline():

    print("=" * 60)
    print("NIGERIA WEATHER ETL PIPELINE")
    print("=" * 60)

    # Validate API key
    if not API_KEY:
        raise ValueError(
            "OPENWEATHER_API_KEY is not configured."
        )

    print("\n[1/4] Connecting to database...")

    connection = sqlite3.connect(DB_PATH)

    try:

        # Create tables
        create_database(connection)

        # Load city reference data
        print("[2/4] Loading city reference data...")

        load_cities(
            connection,
            CITIES
        )

        # Extract
        print("[3/4] Extracting weather data...")

        weather_records = []

        for location in CITIES:

            print(
                f"   Collecting {location['City']}..."
            )

            weather = extract_weather(
                location["City"],
                location["State"],
                location["Region"]
            )

            if weather is not None:
                weather_records.append(weather)

        print(
            f"   Successfully extracted "
            f"{len(weather_records)} cities."
        )

        if not weather_records:
            raise RuntimeError(
                "No weather data was extracted."
            )

        # Transform
        print("[4/4] Transforming and loading data...")

        transformed_df = transform_weather_data(
            weather_records
        )

        # Load
        rows_loaded = load_weather_data(
            connection,
            transformed_df
        )

        print(
            f"\nSuccessfully loaded "
            f"{rows_loaded} weather observations."
        )

        # Check total records
        total_records = connection.execute(
            """
            SELECT COUNT(*)
            FROM weather_observations
            """
        ).fetchone()[0]

        print(
            f"Total observations in database: "
            f"{total_records}"
        )

    finally:

        connection.close()

    print("\nPipeline completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()