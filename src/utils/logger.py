"""
Utility module for pipeline logging.

Purpose:
- Write ETL progress messages to the console
- Save the same messages into a log file
- Make the project look closer to a production data pipeline
"""

import logging
from pathlib import Path


# Create a logs folder automatically if it does not already exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


# Define where the pipeline log file will be saved
LOG_FILE = LOG_DIR / "pipeline.log"


def get_logger(name: str = "ride_hailing_pipeline"):
    """
    Creates and returns a reusable logger.

    This logger writes messages to:
    1. The terminal
    2. logs/pipeline.log
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate log messages if the logger is called multiple times
    if logger.handlers:
        return logger

    # Standard log format used for both console and file output
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File output
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger