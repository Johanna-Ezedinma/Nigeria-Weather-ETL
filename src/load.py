import sqlite3
import pandas as pd


def create_database(connection):
    """
    Create the database tables if they don't already exist.
    """

    create_cities_table = """
    CREATE TABLE IF NOT EXISTS cities (
        city_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT NOT NULL UNIQUE,
        state TEXT NOT NULL,
        region TEXT NOT NULL,
        country TEXT NOT NULL
    );
    """

    create_weather_table = """
    CREATE TABLE IF NOT EXISTS weather_observations (
        observation_id TEXT PRIMARY KEY,
        city_id INTEGER NOT NULL,
        temperature_c REAL,
        feels_like_c REAL,
        min_temperature_c REAL,
        max_temperature_c REAL,
        humidity_percent INTEGER,
        pressure_hpa REAL,
        weather_condition TEXT,
        weather_description TEXT,
        wind_speed_mps REAL,
        wind_direction_deg REAL,
        cloudiness_percent INTEGER,
        visibility_km REAL,
        weather_timestamp TEXT,
        weather_time_nigeria TEXT,
        extracted_at_utc TEXT,
        collection_date TEXT,
        collection_hour_nigeria INTEGER,
        time_period TEXT,
        FOREIGN KEY (city_id)
            REFERENCES cities(city_id)
    );
    """

    connection.execute(create_cities_table)
    connection.execute(create_weather_table)
    connection.commit()


def load_cities(connection, cities):
    """
    Insert cities into the reference table.
    Existing cities are ignored.
    """

    insert_query = """
    INSERT OR IGNORE INTO cities
    (city, state, region, country)
    VALUES (?, ?, ?, ?);
    """

    for location in cities:
        connection.execute(
            insert_query,
            (
                location["City"],
                location["State"],
                location["Region"],
                "Nigeria"
            )
        )

    connection.commit()


def load_weather_data(connection, df):
    """
    Load transformed weather observations into SQLite.
    Duplicate observations are ignored.
    """

    if df.empty:
        print("No weather data to load.")
        return 0

    # Get city IDs
    city_lookup = pd.read_sql_query(
        "SELECT city_id, city FROM cities",
        connection
    )

    # Match city names to city IDs
    df = df.merge(
        city_lookup,
        left_on="City",
        right_on="city",
        how="left"
    )

    # Check for missing city IDs
    if df["city_id"].isnull().any():
        missing_cities = df.loc[
            df["city_id"].isnull(),
            "City"
        ].tolist()

        raise ValueError(
            f"Missing city IDs for: {missing_cities}"
        )

    # Select columns for database
    load_df = df[
        [
            "Observation_ID",
            "city_id",
            "Temperature_C",
            "Feels_Like_C",
            "Min_Temperature_C",
            "Max_Temperature_C",
            "Humidity_Percent",
            "Pressure_hPa",
            "Weather_Condition",
            "Weather_Description",
            "Wind_Speed_mps",
            "Wind_Direction_Deg",
            "Cloudiness_Percent",
            "Visibility_km",
            "Weather_Timestamp",
            "Weather_Time_Nigeria",
            "Extracted_At_UTC",
            "Collection_Date",
            "Collection_Hour_Nigeria",
            "Time_Period"
        ]
    ].copy()

    # Rename columns to database naming convention
    load_df = load_df.rename(
        columns={
            "Observation_ID": "observation_id",
            "Temperature_C": "temperature_c",
            "Feels_Like_C": "feels_like_c",
            "Min_Temperature_C": "min_temperature_c",
            "Max_Temperature_C": "max_temperature_c",
            "Humidity_Percent": "humidity_percent",
            "Pressure_hPa": "pressure_hpa",
            "Weather_Condition": "weather_condition",
            "Weather_Description": "weather_description",
            "Wind_Speed_mps": "wind_speed_mps",
            "Wind_Direction_Deg": "wind_direction_deg",
            "Cloudiness_Percent": "cloudiness_percent",
            "Visibility_km": "visibility_km",
            "Weather_Timestamp": "weather_timestamp",
            "Weather_Time_Nigeria": "weather_time_nigeria",
            "Extracted_At_UTC": "extracted_at_utc",
            "Collection_Date": "collection_date",
            "Collection_Hour_Nigeria": "collection_hour_nigeria",
            "Time_Peak": "time_period"
        }
    )

    # Convert datetime columns to strings for SQLite
    datetime_columns = [
        "weather_timestamp",
        "weather_time_nigeria",
        "extracted_at_utc"
    ]

    for column in datetime_columns:
        load_df[column] = load_df[column].astype(str)

    # Insert observations
    insert_query = """
    INSERT OR IGNORE INTO weather_observations (
        observation_id,
        city_id,
        temperature_c,
        feels_like_c,
        min_temperature_c,
        max_temperature_c,
        humidity_percent,
        pressure_hpa,
        weather_condition,
        weather_description,
        wind_speed_mps,
        wind_direction_deg,
        cloudiness_percent,
        visibility_km,
        weather_timestamp,
        weather_time_nigeria,
        extracted_at_utc,
        collection_date,
        collection_hour_nigeria,
        time_period
    )
    VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    );
    """

    rows_loaded = 0

    for row in load_df.itertuples(
        index=False,
        name=None
    ):
        cursor = connection.execute(
            insert_query,
            row
        )

        rows_loaded += cursor.rowcount

    connection.commit()

    return rows_loaded