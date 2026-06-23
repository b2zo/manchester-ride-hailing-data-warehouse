import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.db_connection import get_engine


def load_fact_trips():
    engine = get_engine()

    with engine.begin() as conn:
        print("Loading fact_trips...")

        conn.exec_driver_sql("""
            INSERT INTO fact_trips (
                trip_id,
                date_key,
                time_key,
                pickup_location_key,
                dropoff_location_key,
                trip_type_key,
                distance_miles,
                duration_minutes,
                fare,
                tip,
                total_earnings,
                estimated_cost,
                net_profit,
                earnings_per_mile,
                earnings_per_hour,
                profit_per_hour
            )
            SELECT
                s.trip_id,
                TO_CHAR(s.trip_date, 'YYYYMMDD')::INTEGER AS date_key,
                s.hour_of_day AS time_key,
                pickup.location_key AS pickup_location_key,
                dropoff.location_key AS dropoff_location_key,
                tt.trip_type_key,
                s.distance_miles,
                s.duration_minutes,
                s.fare,
                s.tip,
                s.total_earnings,
                s.estimated_cost,
                s.net_profit,
                s.earnings_per_mile,
                s.earnings_per_hour,
                s.profit_per_hour
            FROM staging_trips s
            LEFT JOIN dim_location pickup
                ON s.pickup_area = pickup.area_name
            LEFT JOIN dim_location dropoff
                ON s.dropoff_area = dropoff.area_name
            LEFT JOIN dim_trip_type tt
                ON s.airport_trip = tt.airport_trip
            ON CONFLICT (trip_id) DO NOTHING;
        """)

    print("Fact table loaded successfully")


if __name__ == "__main__":
    load_fact_trips()