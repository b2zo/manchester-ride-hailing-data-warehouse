DROP VIEW IF EXISTS vw_daily_performance;
DROP VIEW IF EXISTS vw_area_profitability;
DROP VIEW IF EXISTS vw_airport_performance;
DROP VIEW IF EXISTS vw_hourly_performance;

CREATE VIEW vw_daily_performance AS
SELECT
    d.full_date,
    d.day_name,
    d.month_name,
    d.year,
    COUNT(f.trip_key) AS total_trips,
    ROUND(SUM(f.total_earnings), 2) AS total_revenue,
    ROUND(SUM(f.net_profit), 2) AS total_profit,
    ROUND(AVG(f.earnings_per_hour), 2) AS avg_earnings_per_hour,
    ROUND(AVG(f.profit_per_hour), 2) AS avg_profit_per_hour
FROM fact_trips f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.full_date, d.day_name, d.month_name, d.year;

CREATE VIEW vw_area_profitability AS
SELECT
    l.area_name AS pickup_area,
    l.location_type,
    COUNT(f.trip_key) AS total_trips,
    ROUND(SUM(f.total_earnings), 2) AS total_revenue,
    ROUND(SUM(f.net_profit), 2) AS total_profit,
    ROUND(AVG(f.earnings_per_hour), 2) AS avg_earnings_per_hour,
    ROUND(AVG(f.profit_per_hour), 2) AS avg_profit_per_hour,
    ROUND(AVG(f.earnings_per_mile), 2) AS avg_earnings_per_mile
FROM fact_trips f
JOIN dim_location l ON f.pickup_location_key = l.location_key
GROUP BY l.area_name, l.location_type;

CREATE VIEW vw_airport_performance AS
SELECT
    tt.trip_category,
    COUNT(f.trip_key) AS total_trips,
    ROUND(SUM(f.total_earnings), 2) AS total_revenue,
    ROUND(SUM(f.net_profit), 2) AS total_profit,
    ROUND(AVG(f.distance_miles), 2) AS avg_distance,
    ROUND(AVG(f.duration_minutes), 2) AS avg_duration,
    ROUND(AVG(f.profit_per_hour), 2) AS avg_profit_per_hour
FROM fact_trips f
JOIN dim_trip_type tt ON f.trip_type_key = tt.trip_type_key
GROUP BY tt.trip_category;

CREATE VIEW vw_hourly_performance AS
SELECT
    t.hour_of_day,
    t.time_period,
    t.is_peak_hour,
    t.is_night_shift,
    COUNT(f.trip_key) AS total_trips,
    ROUND(SUM(f.total_earnings), 2) AS total_revenue,
    ROUND(SUM(f.net_profit), 2) AS total_profit,
    ROUND(AVG(f.profit_per_hour), 2) AS avg_profit_per_hour
FROM fact_trips f
JOIN dim_time t ON f.time_key = t.time_key
GROUP BY t.hour_of_day, t.time_period, t.is_peak_hour, t.is_night_shift;