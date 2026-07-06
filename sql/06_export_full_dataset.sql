-- Export one joined flat dataset from the warehouse.
-- This combines the fact table with all dimension tables
-- so third-party tools can use one CSV file.

\copy (
    SELECT
        f.trip_id,
        d.full_date,
        d.day_name,
        d.month_name,
        d.year,
        t.hour_of_day,
        t.time_period,
        pickup.area_name AS pickup_area,
        pickup.location_type AS pickup_location_type,
        dropoff.area_name AS dropoff_area,
        dropoff.location_type AS dropoff_location_type,
        tt.trip_category,
        f.distance_miles,
        f.duration_minutes,
        f.fare,
        f.tip,
        f.total_earnings,
        f.estimated_cost,
        f.net_profit,
        f.earnings_per_mile,
        f.earnings_per_hour,
        f.profit_per_hour
    FROM fact_trips f
    LEFT JOIN dim_date d
        ON f.date_key = d.date_key
    LEFT JOIN dim_time t
        ON f.time_key = t.time_key
    LEFT JOIN dim_location pickup
        ON f.pickup_location_key = pickup.location_key
    LEFT JOIN dim_location dropoff
        ON f.dropoff_location_key = dropoff.location_key
    LEFT JOIN dim_trip_type tt
        ON f.trip_type_key = tt.trip_type_key
) TO 'data/exports/ride_hailing_full_dataset.csv' CSV HEADER;