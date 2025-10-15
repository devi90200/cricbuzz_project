WITH matchlean_manual AS (
    SELECT 'Saurabh Netravalkar'::TEXT AS batsman_name, '2nd T20I'::TEXT AS match_desc, 5::INT AS runs, 6::INT AS balls, '2025-10-11'::DATE AS match_date
    UNION ALL
    SELECT 'Nisarg Patel', '2nd T20I', 10, 6, '2025-10-11'
    UNION ALL
    SELECT 'Nisarg Patel', '1st T20I', 20, 12, '2025-09-20'
    UNION ALL
    SELECT 'Saurabh Netravalkar', '1st T20I', 15, 10, '2025-09-20'
),
player_quarters AS (
    SELECT
        batsman_name,
        DATE_TRUNC('quarter', match_date)::DATE AS quarter_start,
        AVG(runs) AS avg_runs,
        AVG((runs * 100.0) / NULLIF(balls, 0)) AS avg_strike_rate
    FROM matchlean_manual
    GROUP BY batsman_name, DATE_TRUNC('quarter', match_date)
),
quarter_comparison AS (
    SELECT
        p1.batsman_name,
        p1.quarter_start,
        p1.avg_runs,
        p1.avg_strike_rate,
        LAG(p1.avg_runs) OVER (PARTITION BY p1.batsman_name ORDER BY p1.quarter_start) AS prev_avg_runs,
        LAG(p1.avg_strike_rate) OVER (PARTITION BY p1.batsman_name ORDER BY p1.quarter_start) AS prev_strike_rate
    FROM player_quarters p1
)
SELECT
    batsman_name,
    quarter_start,
    ROUND(avg_runs, 2) AS avg_runs,
    ROUND(avg_strike_rate, 2) AS avg_strike_rate,
    CASE
        WHEN prev_avg_runs IS NULL THEN 'N/A'
        WHEN avg_runs > prev_avg_runs AND avg_strike_rate >= prev_strike_rate THEN 'Improving'
        WHEN avg_runs < prev_avg_runs AND avg_strike_rate <= prev_strike_rate THEN 'Declining'
        ELSE 'Stable'
    END AS quarter_trend
FROM quarter_comparison
ORDER BY batsman_name, quarter_start;










































































