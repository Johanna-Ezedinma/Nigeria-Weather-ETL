import pandas as pd


def transform_weather_data(weather_records):
    """
    Transform raw weather records into an analysis-ready DataFrame.
    """

    df = pd.DataFrame(weather_records)

    if df.empty:
        return df

    # Convert weather timestamp from Unix seconds to UTC
    df["Weather_Timestamp"] = pd.to_datetime(
        df["Weather_Timestamp"],
        unit="s",
        utc=True
    )

    # Convert weather timestamp to Nigerian local time
    df["Weather_Time_Nigeria"] = (
        df["Weather_Timestamp"]
        .dt.tz_convert("Africa/Lagos")
    )

    # Add extraction timestamp as a timezone-aware datetime
    df["Extracted_At_UTC"] = pd.to_datetime(
        df["Extracted_At_UTC"],
        utc=True
    )

    # Convert extraction time to Nigerian time
    collection_time_nigeria = (
        df["Extracted_At_UTC"]
        .dt.tz_convert("Africa/Lagos")
    )

    # Create collection date based on Nigerian time
    df["Collection_Date"] = (
        collection_time_nigeria.dt.date
    )

    # Extract Nigerian collection hour
    df["Collection_Hour_Nigeria"] = (
        collection_time_nigeria.dt.hour
    )

    # Classify collection time by period of the day
    df["Time_Period"] = (
        df["Collection_Hour_Nigeria"]
        .apply(get_time_period)
    )

    # Create unique observation ID
    df["Observation_ID"] = (
        df["City"].str.replace(" ", "_", regex=False)
        + "_"
        + df["Weather_Time_Nigeria"].dt.strftime("%Y%m%d_%H%M")
    )

    return df


def get_time_period(hour):
    """
    Categorize collection time into a period of the day.
    """

    if 5 <= hour < 9:
        return "Morning"

    elif 9 <= hour < 15:
        return "Midday"

    elif 15 <= hour < 21:
        return "Evening"

    else:
        return "Midnight"