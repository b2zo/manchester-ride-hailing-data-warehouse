DROP TABLE IF EXISTS pipeline_audit;

CREATE TABLE pipeline_audit (
    audit_id SERIAL PRIMARY KEY,
    pipeline_name VARCHAR(100),
    run_status VARCHAR(50),
    rows_loaded INTEGER,
    run_started_at TIMESTAMP,
    run_finished_at TIMESTAMP,
    error_message TEXT
);