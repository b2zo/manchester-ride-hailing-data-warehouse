# 02 — System Architecture

![Architecture](../assets/diagrams/architecture.svg)

The architecture moves data from raw CSV files through Python ETL into PostgreSQL views consumed by Power BI.

Raw Trip Data (CSV)
          |
          v
+----------------------+
| Python Extract Layer |
+----------------------+
          |
          v
+----------------------+
| PostgreSQL Staging   |
| staging_trips        |
+----------------------+
          |
          v
+----------------------+
| Transform Layer      |
| Dimension Loads      |
+----------------------+
          |
          v
+----------------------+
| Star Schema          |
| fact_trips           |
| dim_date             |
| dim_time             |
| dim_location         |
| dim_trip_type        |
+----------------------+
          |
          v
+----------------------+
| Analytics Views      |
+----------------------+
          |
          v
+----------------------+
| Power BI Dashboard   |
+----------------------+
```
