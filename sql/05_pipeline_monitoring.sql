-- =====================================================
-- PIPELINE MONITORING
-- =====================================================

SELECT
    pipeline_name,
    run_status,
    rows_loaded,
    run_started_at,
    run_finished_at,
    EXTRACT(
        EPOCH FROM
        (run_finished_at - run_started_at)
    ) AS duration_seconds
FROM pipeline_audit
ORDER BY audit_id DESC;