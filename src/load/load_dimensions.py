import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.db_connection import get_engine


def load_dimensions():
    engine = get_engine()

    with engine.begin() as conn:

        print("Loading dim_date...")

        conn.exec_driver_sql("""
            INSERT INTO dim_date (
                date_key,
                full_date,
                day_name,
                day_of_week,
                week_number,
                month_number,
                month_name,
                quarter,
                year,
                is_weekend
            )
            SELECT DISTINCT
                TO_CHAR(trip_date, 'YYYYMMDD')::INTEGER AS date_key,
                trip_date AS full_date,
                day_of_week AS day_name,
                EXTRACT(ISODOW FROM trip_date)::INTEGER AS day_of_week,
                EXTRACT(WEEK FROM trip_date)::INTEGER AS week_number,
                EXTRACT(MONTH FROM trip_date)::INTEGER AS month_number,
                TO_CHAR(trip_date, 'Month') AS month_name,
                EXTRACT(QUARTER FROM trip_date)::INTEGER AS quarter,
                EXTRACT(YEAR FROM trip_date)::INTEGER AS year,
                is_weekend
            FROM staging_trips
            ON CONFLICT (date_key) DO NOTHING;
        """)

        print("Loading dim_time...")

        conn.exec_driver_sql("""
            INSERT INTO dim_time (
                time_key,
                hour_of_day,
                time_period,
                is_peak_hour,
                is_night_shift
            )
            SELECT DISTINCT
                hour_of_day AS time_key,
                hour_of_day,
                time_period,
                CASE 
                    WHEN hour_of_day BETWEEN 6 AND 9
                      OR hour_of_day BETWEEN 16 AND 19
                      OR hour_of_day BETWEEN 22 AND 23
                      OR hour_of_day BETWEEN 0 AND 2
                    THEN TRUE
                    ELSE FALSE
                END AS is_peak_hour,
                CASE 
                    WHEN hour_of_day BETWEEN 22 AND 23
                      OR hour_of_day BETWEEN 0 AND 5
                    THEN TRUE
                    ELSE FALSE
                END AS is_night_shift
            FROM staging_trips
            ON CONFLICT (time_key) DO NOTHING;
        """)
        print("Loading dim_location...")

        conn.exec_driver_sql("""
            INSERT INTO dim_location (
                area_name,
                latitude,
                longitude,
                location_type
            )
            SELECT DISTINCT
                area_name,
                NULL::NUMERIC AS latitude,
                NULL::NUMERIC AS longitude,
                location_type
            FROM (
                SELECT
                    pickup_area AS area_name,
                    CASE 
                        WHEN pickup_area = 'Manchester Airport' THEN 'Airport'
                        WHEN pickup_area IN ('Deansgate', 'Piccadilly', 'MediaCityUK', 'Salford Quays') THEN 'City Centre'
                        ELSE 'Suburban'
                    END AS location_type
                FROM staging_trips
                WHERE pickup_area IS NOT NULL

                UNION

                SELECT
                    dropoff_area AS area_name,
                    CASE 
                        WHEN dropoff_area = 'Manchester Airport' THEN 'Airport'
                        WHEN dropoff_area IN ('Deansgate', 'Piccadilly', 'MediaCityUK', 'Salford Quays') THEN 'City Centre'
                        ELSE 'Suburban'
                    END AS location_type
                FROM staging_trips
                WHERE dropoff_area IS NOT NULL
            ) AS locations
            ON CONFLICT (area_name) DO NOTHING;
        """)
        
        print("Loading dim_trip_type...")

        conn.exec_driver_sql("""
            INSERT INTO dim_trip_type (
                airport_trip,
                trip_category
            )
            SELECT DISTINCT
                airport_trip,
                CASE 
                    WHEN airport_trip = TRUE THEN 'Airport Trip'
                    ELSE 'Non-Airport Trip'
                END AS trip_category
            FROM staging_trips
            ON CONFLICT (airport_trip) DO NOTHING;
        """)

    print("Dimension tables loaded successfully")


if __name__ == "__main__":
    load_dimensions()