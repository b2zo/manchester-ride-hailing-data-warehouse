# Star Schema Data Model

## Fact Table

### fact_trips

Stores one row per trip.

Measures:

- fare
- tip
- total_earnings
- net_profit
- earnings_per_hour
- profit_per_hour

---

## Dimensions

### dim_date

Date intelligence.

### dim_time

Hour and time period analysis.

### dim_location

Pickup and dropoff locations.

### dim_trip_type

Airport vs Non-Airport segmentation.