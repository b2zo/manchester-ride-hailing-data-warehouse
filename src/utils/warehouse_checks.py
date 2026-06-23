"""
Warehouse validation helper functions.

Purpose:
- Check the current state of the PostgreSQL warehouse
- Help the pipeline decide what data should be loaded
- Support incremental loading by identifying existing trip IDs
"""

import sys
from pathlib import Path

# Allow Python to find the project source folder
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.db_connection import get_engine


def get_existing_trip_ids():
    """
    Return all trip IDs that already exist in the fact_trips table.

    This is used to prevent duplicate records during incremental loads.
    """

    engine = get_engine()

    query = """
        SELECT trip_id
        FROM fact_trips;
    """

    with engine.connect() as conn:
        result = conn.exec_driver_sql(query)
        existing_ids = {row[0] for row in result}

    return existing_ids


def get_fact_trip_count():
    """
    Return the number of rows currently stored in fact_trips.

    Useful for reporting pipeline results before and after loading.
    """

    engine = get_engine()

    query = """
        SELECT COUNT(*)
        FROM fact_trips;
    """

    with engine.connect() as conn:
        count = conn.exec_driver_sql(query).scalar()

    return count