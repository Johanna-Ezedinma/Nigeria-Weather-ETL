import sqlite3
from pathlib import Path

import pandas as pd

from src.config import DB_PATH, PROJECT_ROOT


OUTPUT_PATH = PROJECT_ROOT / "data" / "weather_observations.csv"


def export_weather_data():
    """
    Export weather observations from SQLite into an analysis-ready CSV.
    """

    connection = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        w.observation_id,
        c.city,
        c.state,
        c.region,
        c.country,
        w.temperature_c,
        w.feels_like_c,
        w.min_temperature_c,
        w.max_temperature_c,
        w.humidity_percent,
        w.pressure_hpa,
        w.weather_condition,
        w.weather_description,
        w.wind_speed_mps,
        w.wind_direction_deg,
        w.cloudiness_percent,
        w.visibility_km,
        w.weather_timestamp,
        w.weather_time_nigeria,
        w.extracted_at_utc,
        w.collection_date,
        w.collection_hour_nigeria,
        w.time_period
    FROM weather_observations w
    JOIN cities c
        ON w.city_id = c.city_id
    ORDER BY w.weather_time_nigeria;
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    if df.empty:
        print("No weather observations found.")
        return

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    # If an existing CSV exists, combine it with the latest database data.
    if OUTPUT_PATH.exists():

        existing_df = pd.read_csv(OUTPUT_PATH)

        df = pd.concat(
            [existing_df, df],
            ignore_index=True
        )

    # Remove duplicate observations.
    df = df.drop_duplicates(
        subset=["observation_id"],
        keep="last"
    )

    # Sort chronologically.
    df = df.sort_values(
        by=["weather_time_nigeria", "city"]
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"Exported {len(df)} unique observations.")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    export_weather_data()