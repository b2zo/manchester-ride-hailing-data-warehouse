DROP TABLE IF EXISTS fact_trips;
DROP TABLE IF EXISTS dim_trip_type;
DROP TABLE IF EXISTS dim_location;
DROP TABLE IF EXISTS dim_time;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS staging_trips;

CREATE TABLE staging_trips (
    trip_id INTEGER,
    start_datetime TIMESTAMP,
    trip_date DATE,
    day_of_week VARCHAR(20),
    hour_of_day INTEGER,
    time_period VARCHAR(50),
    pickup_area VARCHAR(100),
    dropoff_area VARCHAR(100),
    pickup_lat NUMERIC(10,6),
    pickup_lon NUMERIC(10,6),
    dropoff_lat NUMERIC(10,6),
    dropoff_lon NUMERIC(10,6),
    distance_miles NUMERIC(10,2),
    duration_minutes NUMERIC(10,2),
    fare NUMERIC(10,2),
    tip NUMERIC(10,2),
    total_earnings NUMERIC(10,2),
    estimated_cost NUMERIC(10,2),
    net_profit NUMERIC(10,2),
    airport_trip BOOLEAN,
    earnings_per_mile NUMERIC(10,2),
    earnings_per_hour NUMERIC(10,2),
    profit_per_hour NUMERIC(10,2),
    is_weekend BOOLEAN,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    day_name VARCHAR(20),
    day_of_week INTEGER,
    week_number INTEGER,
    month_number INTEGER,
    month_name VARCHAR(20),
    quarter INTEGER,
    year INTEGER,
    is_weekend BOOLEAN
);

CREATE TABLE dim_time (
    time_key INTEGER PRIMARY KEY,
    hour_of_day INTEGER NOT NULL,
    time_period VARCHAR(50),
    is_peak_hour BOOLEAN,
    is_night_shift BOOLEAN
);

CREATE TABLE dim_location (
    location_key SERIAL PRIMARY KEY,
    area_name VARCHAR(100) UNIQUE NOT NULL,
    latitude NUMERIC(10,6),
    longitude NUMERIC(10,6),
    location_type VARCHAR(50)
);

CREATE TABLE dim_trip_type (
    trip_type_key SERIAL PRIMARY KEY,
    airport_trip BOOLEAN UNIQUE,
    trip_category VARCHAR(50)
);

CREATE TABLE fact_trips (
    trip_key SERIAL PRIMARY KEY,
    trip_id INTEGER UNIQUE NOT NULL,
    date_key INTEGER REFERENCES dim_date(date_key),
    time_key INTEGER REFERENCES dim_time(time_key),
    pickup_location_key INTEGER REFERENCES dim_location(location_key),
    dropoff_location_key INTEGER REFERENCES dim_location(location_key),
    trip_type_key INTEGER REFERENCES dim_trip_type(trip_type_key),
    distance_miles NUMERIC(10,2),
    duration_minutes NUMERIC(10,2),
    fare NUMERIC(10,2),
    tip NUMERIC(10,2),
    total_earnings NUMERIC(10,2),
    estimated_cost NUMERIC(10,2),
    net_profit NUMERIC(10,2),
    earnings_per_mile NUMERIC(10,2),
    earnings_per_hour NUMERIC(10,2),
    profit_per_hour NUMERIC(10,2),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);