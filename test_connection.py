from src.utils.db_connection import get_engine

engine = get_engine()

with engine.connect() as conn:
    result = conn.exec_driver_sql("SELECT current_database();")

    for row in result:
        print("Connected to:", row[0])