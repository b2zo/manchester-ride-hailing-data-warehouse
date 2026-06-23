-- 1. Overall warehouse KPIs
SELECT
    COUNT(*) AS total_trips,
    ROUND(SUM(total_earnings), 2) AS total_revenue,
    ROUND(SUM(net_profit), 2) AS total_profit,
    ROUND(AVG(earnings_per_hour), 2) AS avg_earnings_per_hour,
    ROUND(AVG(profit_per_hour), 2) AS avg_profit_per_hour
FROM fact_trips;


-- 2. Most profitable pickup areas
SELECT
    l.area_name AS pickup_area,
    l.location_type,
    COUNT(f.trip_key) AS total_trips,
    ROUND(SUM(f.total_earnings), 2) AS total_revenue,
    ROUND(AVG(f.profit_per_hour), 2) AS avg_profit_per_hour
FROM fact_trips f
JOIN dim_location l
    ON f.pickup_location_key = l.location_key
GROUP BY l.area_name, l.location_type
ORDER BY avg_profit_per_hour DESC;


-- 3. Best hours to work
SELECT
    t.hour_of_day,
    t.time_period,
    COUNT(f.trip_key) AS total_trips,
    ROUND(AVG(f.profit_per_hour), 2) AS avg_profit_per_hour
FROM fact_trips f
JOIN dim_time t
    ON f.time_key = t.time_key
GROUP BY t.hour_of_day, t.time_period
ORDER BY avg_profit_per_hour DESC;


-- 4. Airport vs non-airport performance
SELECT
    tt.trip_category,
    COUNT(f.trip_key) AS total_trips,
    ROUND(SUM(f.total_earnings), 2) AS total_revenue,
    ROUND(AVG(f.profit_per_hour), 2) AS avg_profit_per_hour
FROM fact_trips f
JOIN dim_trip_type tt
    ON f.trip_type_key = tt.trip_type_key
GROUP BY tt.trip_category;


-- 5. Pipeline audit history
SELECT
    audit_id,
    pipeline_name,
    run_status,
    rows_loaded,
    run_started_at,
    run_finished_at,
    error_message
FROM pipeline_audit
ORDER BY audit_id DESC;