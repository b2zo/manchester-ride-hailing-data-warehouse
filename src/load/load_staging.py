import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.db_connection import get_engine

RAW_FILE_PATH = "data/raw/trips_raw.csv"

def load_staging():
    engine = get_engine()

    df = pd.read_csv(RAW_FILE_PATH)

    # Rename columns to match staging table where possible
    df = df.rename(columns={
        "pickup_datetime": "start_datetime",
        "pickup_location": "pickup_area",
        "trip_type": "time_period",
        "fare_amount": "fare"
    })

    # Add missing warehouse columns for now
    df["trip_date"] = pd.to_datetime(df["start_datetime"]).dt.date
    df["day_of_week"] = pd.to_datetime(df["start_datetime"]).dt.day_name()
    df["hour_of_day"] = pd.to_datetime(df["start_datetime"]).dt.hour
    df["dropoff_area"] = df["pickup_area"]
    df["pickup_lat"] = None
    df["pickup_lon"] = None
    df["dropoff_lat"] = None
    df["dropoff_lon"] = None
    df["tip"] = 0
    df["total_earnings"] = df["fare"]
    df["estimated_cost"] = df["distance_miles"] * 0.28
    df["net_profit"] = df["total_earnings"] - df["estimated_cost"]
    df["airport_trip"] = df["pickup_area"].eq("Manchester Airport")
    df["earnings_per_mile"] = df["total_earnings"] / df["distance_miles"]
    df["earnings_per_hour"] = df["total_earnings"] / (df["duration_minutes"] / 60)
    df["profit_per_hour"] = df["net_profit"] / (df["duration_minutes"] / 60)
    df["is_weekend"] = df["day_of_week"].isin(["Saturday", "Sunday"])

    required_columns = [
        "trip_id", "start_datetime", "trip_date", "day_of_week", "hour_of_day",
        "time_period", "pickup_area", "dropoff_area", "pickup_lat", "pickup_lon",
        "dropoff_lat", "dropoff_lon", "distance_miles", "duration_minutes",
        "fare", "tip", "total_earnings", "estimated_cost", "net_profit",
        "airport_trip", "earnings_per_mile", "earnings_per_hour",
        "profit_per_hour", "is_weekend"
    ]

    df = df[required_columns]

    df.to_sql(
        "staging_trips",
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} rows into staging_trips")

if __name__ == "__main__":
    load_staging()