import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.db_connection import get_engine


def run_quality_checks():
    engine = get_engine()

    checks = {
        "staging row count": "SELECT COUNT(*) FROM staging_trips;",
        "fact row count": "SELECT COUNT(*) FROM fact_trips;",
        "duplicate trip ids": """
            SELECT COUNT(*)
            FROM (
                SELECT trip_id
                FROM fact_trips
                GROUP BY trip_id
                HAVING COUNT(*) > 1
            ) duplicates;
        """,
        "negative fares": "SELECT COUNT(*) FROM fact_trips WHERE fare < 0;",
        "zero or negative distance": "SELECT COUNT(*) FROM fact_trips WHERE distance_miles <= 0;",
        "zero or negative duration": "SELECT COUNT(*) FROM fact_trips WHERE duration_minutes <= 0;",
        "missing pickup location": "SELECT COUNT(*) FROM fact_trips WHERE pickup_location_key IS NULL;",
        "missing dropoff location": "SELECT COUNT(*) FROM fact_trips WHERE dropoff_location_key IS NULL;"
    }

    print("\nDATA QUALITY REPORT")
    print("-" * 40)

    with engine.connect() as conn:
        for check_name, query in checks.items():
            result = conn.exec_driver_sql(query).scalar()
            print(f"{check_name}: {result}")

    print("-" * 40)
    print("Data quality checks complete")


if __name__ == "__main__":
    run_quality_checks()