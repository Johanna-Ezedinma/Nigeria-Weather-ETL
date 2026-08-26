# 🇳🇬 Nigeria Weather Data Bank & ETL Pipeline

## Overview

This is a Python-based ETL pipeline that continuously collects real-time weather observations from the OpenWeather API for locations across Nigeria.

The project demonstrates how raw API data can be transformed into a structured, analysis-ready data bank using Python, Pandas, and SQLite.

The long-term goal is to build a historical weather dataset that can support exploratory analysis, regional comparisons, time-based analysis, and interactive Power BI dashboards.

---

## Project Objectives

This project was built to demonstrate a complete data engineering and analytics workflow:

- Extract real-time data from an external API.
- Transform raw API responses into structured datasets.
- Validate and clean collected data.
- Store historical observations in SQLite.
- Maintain a master reference table for Nigerian locations.
- Build a scalable data collection process.
- Analyze weather patterns across Nigerian regions.
- Develop an interactive Power BI dashboard from the collected data.

---

## Data Source

Weather data is collected from the:

**OpenWeather API**

The pipeline currently uses the OpenWeather Current Weather API.

Data is retrieved using geographic coordinates for each location rather than relying only on city-name searches.

---

## Geographic Coverage

The data bank is designed to cover **37 Nigerian locations**, representing the 36 states plus the Federal Capital Territory.

Locations are grouped into Nigeria's six geopolitical zones:

### South West

- Lagos
- Ibadan
- Abeokuta
- Akure
- Osogbo
- Ado-Ekiti

### South East

- Umuahia
- Awka
- Abakaliki
- Enugu
- Owerri

### South South

- Uyo
- Yenagoa
- Calabar
- Asaba
- Benin City
- Port Harcourt

### North Central

- Abuja
- Makurdi
- Lokoja
- Ilorin
- Lafia
- Minna
- Jos

### North West

- Dutse
- Kaduna
- Kano
- Katsina
- Birnin Kebbi
- Sokoto
- Gusau

### North East

- Yola
- Bauchi
- Maiduguri
- Gombe
- Jalingo
- Damaturu

---

## ETL Architecture

The pipeline follows a standard Extract, Transform, Load architecture.

```text
                    OpenWeather API
                           │
                           ▼
                    ┌─────────────┐
                    │   EXTRACT   │
                    │   Python    │
                    │  Requests   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  TRANSFORM  │
                    │   Pandas    │
                    │             │
                    │ • Clean     │
                    │ • Convert   │
                    │ • Enrich    │
                    │ • Validate  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    LOAD     │
                    │   SQLite    │
                    │             │
                    │ Location    │
                    │ Weather     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   ANALYZE   │
                    │   Power BI  │
                    └─────────────┘
```

## Data Pipeline

### 1. Extract

Python sends requests to the OpenWeather API using the configured API key.

For each active location, the pipeline collects weather information including:

- City
- State
- Region
- Latitude
- Longitude
- Temperature
- Feels-like temperature
- Minimum temperature
- Maximum temperature
- Humidity
- Atmospheric pressure
- Weather condition
- Weather description
- Wind speed
- Wind direction
- Cloudiness
- Visibility
- Weather timestamp
- Extraction timestamp

---

### 2. Transform

The raw API response is transformed using Pandas.

The transformation process includes:

- Converting Unix timestamps into datetime values
- Converting UTC timestamps to Nigerian time
- Creating collection dates
- Creating collection hours
- Classifying observations into time periods
- Creating unique observation IDs
- Preparing data types for SQLite
- Structuring data for analytical use

Time periods are classified as:

| Time        | Period  |
| ----------- | ------- |
| 05:00–08:59 | Morning |
| 09:00–14:59 | Midday  |
| 15:00–20:59 | Evening |
| 21:00–04:59 | Night   |

---

## Database Design

The SQLite database uses a relational structure.

### Location Dimension

The `locations` table acts as the master reference table.

It contains:

- `location_id`
- `city`
- `state`
- `region`
- `country`
- `latitude`
- `longitude`
- `location_type`
- `active`

### Weather Fact Table

The `weather_observations` table stores individual weather observations.

It contains:

- `observation_id`
- `location_id`
- `temperature_c`
- `feels_like_c`
- `min_temperature_c`
- `max_temperature_c`
- `humidity_percent`
- `pressure_hpa`
- `weather_condition`
- `weather_description`
- `wind_speed_mps`
- `wind_direction_deg`
- `cloudiness_percent`
- `visibility_km`
- `weather_timestamp`
- `weather_time_nigeria`
- `extracted_at_utc`
- `collection_date`
- `collection_hour_nigeria`
- `time_period`

The relationship between the tables is:

```text
locations
     │
     │ 1
     │
     │
     │ many
     ▼
weather_observations
```

This allows multiple weather observations to be associated with each location over time.

```
Nigeria-Weather-ETL/
│
├── data/
│ ├── locations.csv
│ └── weather.db
│
├── notebook/
│ └── 01_weather_etl.ipynb
│
├── src/
│ ├── **init**.py
│ ├── config.py
│ ├── extract.py
│ ├── transform.py
│ ├── load.py
│ └── pipeline.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

> The SQLite database and API credentials are excluded from version control.

| Technology       | Purpose                             |
| ---------------- | ----------------------------------- |
| Python           | ETL pipeline development            |
| Requests         | API requests                        |
| Pandas           | Data transformation and analysis    |
| SQLite           | Historical data storage             |
| python-dotenv    | Secure API key management           |
| Jupyter Notebook | Exploration and documentation       |
| Git              | Version control                     |
| GitHub           | Project repository                  |
| Power BI         | Data visualization and dashboarding |

---

## Data Security

The OpenWeather API key is stored in a local .env file.

The .env file is excluded from Git using .gitignore.

Example:
`OPENWEATHER_API_KEY=your_api_key_here`

---

## Data Quality

The pipeline is designed to support ongoing data collection.

### Data quality checks include:

- Number of active locations
- Number of observations collected
- Missing location IDs
- Duplicate observation IDs
- Missing weather values
- Valid temperature ranges
- Valid humidity ranges
- Collection timestamps
- Location coverage

Further profiling and validation will be performed as the historical dataset grows.

---

## Planned Analysis

As more observations accumulate, the dataset can be used to investigate questions such as:

- Temperature
- Which Nigerian locations are consistently the hottest?
- Which regions have the lowest average temperatures?
- How does temperature change throughout the day?
- Which locations experience the largest temperature ranges?
- Humidity
- Which locations have the highest average humidity?
- Are southern locations consistently more humid than northern locations?
- How does humidity vary by time of day?
- Regional Differences
- How do weather conditions differ across Nigeria's geopolitical zones?
- Are there measurable differences between northern and southern locations?
- Which regions experience the greatest weather variability?
- Weather Conditions
- Which weather conditions occur most frequently?
- Which cities experience the most cloudy observations?
- How frequently are rain-related conditions recorded?
- Time-Based Analysis
- How does weather change from morning to night?
- Are there recurring patterns across collection periods?
- How does weather vary from day to day?

---

### Power BI Dashboard

The historical dataset will eventually be connected to Power BI to create an interactive weather analytics dashboard.

Potential dashboard components include:

- Current weather overview
- Average temperature by region
- Temperature comparison by city
- Humidity comparison
- Weather condition distribution
- Temperature trends over time
- Regional weather comparisons
- Geographic weather map
- Time-of-day analysis
- KPI cards for temperature, humidity, wind speed, and observations

**The dashboard will allow users to filter the analysis by:**

- State
- City
- Geopolitical region
- Date
- Time period
- Weather condition

---

## Current Status

### Completed

- [x] OpenWeather API connection
- [x] API extraction using Python
- [x] Initial ETL pipeline
- [x] Pandas transformations
- [x] SQLite database
- [x] Location reference table
- [x] Expansion to 37 Nigerian locations
- [x] Location-to-observation relationship
- [x] Environment variable configuration
- [x] Git version control
- [x] GitHub repository

### In Progress

- [ ] Historical data collection
- [ ] Data profiling
- [ ] Data quality analysis
- [ ] Analytical star schema
- [ ] Power BI data model
- [ ] Power BI dashboard
- [ ] Weather insights and storytelling

---

## Future Improvements

**Potential future improvements include:**

- Automated scheduled collection
- Additional weather variables
- Forecast data
- Historical weather comparisons
- Automated data-quality monitoring
- Power BI refresh automation
- Cloud database storage
- Weather anomaly detection
- Regional weather trend analysis
- Long-term climate pattern exploration

---

**Author** : Johanna Ezedinma

---

## Disclaimer

This project is intended for educational and portfolio purposes.

Weather observations are retrieved from the OpenWeather API and represent conditions reported by the API at the time of collection.
