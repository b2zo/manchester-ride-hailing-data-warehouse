"""
Main ETL pipeline orchestrator.

Purpose:
- Run the full ride-hailing data warehouse pipeline end-to-end
- Load raw trip data into PostgreSQL staging
- Populate dimension tables
- Populate the fact table
- Run data quality checks
- Log pipeline success/failure into PostgreSQL
- Write operational logs to logs/pipeline.log
"""

import sys
from pathlib import Path
from datetime import datetime


# Allow Python to find the src/ folder when running this script directly
sys.path.append(str(Path(__file__).resolve().parents[2]))


# Import database connection helper
from src.utils.db_connection import get_engine


# Import logging helper
from src.utils.logger import get_logger


# Import ETL steps
from src.load.load_staging import load_staging
from src.load.load_dimensions import load_dimensions
from src.load.load_fact_trips import load_fact_trips


# Import data quality validation
from src.utils.data_quality import run_quality_checks


def log_pipeline_run(
    status,
    rows_loaded,
    start_time,
    end_time,
    error_message=None
):
    """
    Save one pipeline run record into the PostgreSQL audit table.

    This gives us a production-style history of:
    - when the pipeline ran
    - whether it succeeded or failed
    - how many rows were loaded
    - what error occurred, if any
    """

    engine = get_engine()

    with engine.begin() as conn:
        conn.exec_driver_sql(
            """
            INSERT INTO pipeline_audit
            (
                pipeline_name,
                run_status,
                rows_loaded,
                run_started_at,
                run_finished_at,
                error_message
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                "ride_hailing_dw_pipeline",
                status,
                rows_loaded,
                start_time,
                end_time,
                error_message
            )
        )


def run_pipeline():
    """
    Run the full ETL pipeline.

    Pipeline flow:
    1. Load raw CSV data into PostgreSQL staging table
    2. Load dimension tables
    3. Load fact table
    4. Run data quality checks
    5. Record pipeline outcome in audit table
    """

    logger = get_logger()

    start_time = datetime.now()

    try:
        logger.info("=" * 60)
        logger.info("RIDE-HAILING DATA WAREHOUSE PIPELINE STARTED")
        logger.info("=" * 60)

        logger.info("STEP 1 - Loading raw CSV data into staging_trips")
        load_staging()

        logger.info("STEP 2 - Loading dimension tables")
        load_dimensions()

        logger.info("STEP 3 - Loading fact_trips table")
        load_fact_trips()

        logger.info("STEP 4 - Running data quality checks")
        run_quality_checks()

        end_time = datetime.now()

        # At this stage we know the current pipeline generated/loaded 50,000 rows
        log_pipeline_run(
            status="SUCCESS",
            rows_loaded=50000,
            start_time=start_time,
            end_time=end_time,
            error_message=None
        )

        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)

    except Exception as e:
        end_time = datetime.now()

        # Log error to terminal and logs/pipeline.log
        logger.error(f"PIPELINE FAILED: {str(e)}")

        # Log failure to PostgreSQL audit table
        log_pipeline_run(
            status="FAILED",
            rows_loaded=0,
            start_time=start_time,
            end_time=end_time,
            error_message=str(e)
        )

        # Re-raise the error so Python still shows the full traceback
        raise


if __name__ == "__main__":
    run_pipeline()