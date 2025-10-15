WITH player_format_stats AS (
    SELECT
        batsman_name,
        UPPER(TRIM(match_format)) AS match_format,
        SUM(COALESCE(runs, 0)) AS total_runs,
        COUNT(CASE WHEN balls > 0 THEN 1 END) AS innings_played
    FROM matchlean
    WHERE batsman_name IS NOT NULL AND batsman_name <> ''
    GROUP BY batsman_name, match_format
),
player_summary AS (
    SELECT
        batsman_name,
        MAX(CASE WHEN match_format = 'TEST' THEN total_runs ELSE 0 END) AS test_runs,
        MAX(CASE WHEN match_format = 'ODI' THEN total_runs ELSE 0 END) AS odi_runs,
        MAX(CASE WHEN match_format = 'T20' THEN total_runs ELSE 0 END) AS t20_runs,
        SUM(total_runs) AS overall_runs,
        ROUND(SUM(total_runs)::numeric / NULLIF(SUM(innings_played),0), 2) AS overall_batting_avg
    FROM player_format_stats
    GROUP BY batsman_name
)
SELECT *
FROM player_summary
ORDER BY overall_runs DESC;
