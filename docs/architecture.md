# Data Warehouse Architecture

```text
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