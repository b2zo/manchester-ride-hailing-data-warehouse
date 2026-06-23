"""
Incremental load transformation.

Purpose:
- Read the raw trip CSV
- Compare trip IDs against the PostgreSQL fact table
- Keep only trips that do not already exist in the warehouse
- Save the new records into data/staging/new_trips.csv

This simulates a real-world incremental ETL process.
"""

import sys
from pathlib import Path

import pandas as pd

# Allow Python to find the project source folder
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.warehouse_checks import get_existing_trip_ids


RAW_FILE = "data/raw/trips_raw.csv"
NEW_TRIPS_FILE = "data/staging/new_trips.csv"


def filter_new_trips():
    """
    Filter raw trip data so only new trips move forward in the pipeline.

    Output:
    - data/staging/new_trips.csv
    """

    df = pd.read_csv(RAW_FILE)

    existing_trip_ids = get_existing_trip_ids()

    new_df = df[~df["trip_id"].isin(existing_trip_ids)]

    new_df.to_csv(
        NEW_TRIPS_FILE,
        index=False
    )

    print(f"Raw rows: {len(df)}")
    print(f"Existing rows skipped: {len(df) - len(new_df)}")
    print(f"New rows available for load: {len(new_df)}")

    return len(new_df)


if __name__ == "__main__":
    filter_new_trips()