WITH player_stats AS (
    SELECT
        batsman_name,
        match_format,
        COUNT(*) AS matches_played,
        AVG(runs::numeric) AS batting_avg
    FROM matchlean
    WHERE runs IS NOT NULL AND balls IS NOT NULL
    GROUP BY batsman_name, match_format
)
SELECT
    batsman_name,
    COALESCE(MAX(CASE WHEN match_format = 'Test' THEN matches_played END), 0) AS test_matches,
    COALESCE(MAX(CASE WHEN match_format = 'Test' THEN batting_avg END), 0) AS test_avg,
    COALESCE(MAX(CASE WHEN match_format = 'ODI' THEN matches_played END), 0) AS odi_matches,
    COALESCE(MAX(CASE WHEN match_format = 'ODI' THEN batting_avg END), 0) AS odi_avg,
    COALESCE(MAX(CASE WHEN match_format = 'T20' THEN matches_played END), 0) AS t20_matches,
    COALESCE(MAX(CASE WHEN match_format = 'T20' THEN batting_avg END), 0) AS t20_avg,
    SUM(matches_played) AS total_matches
FROM player_stats
GROUP BY batsman_name
ORDER BY total_matches DESC;

WITH player_stats AS (
    SELECT
        batsman_name,
        match_format,
        COUNT(*) AS matches_played,
        AVG(runs::numeric) AS batting_avg
    FROM matchlean
    WHERE runs IS NOT NULL AND balls IS NOT NULL
    GROUP BY batsman_name, match_format
),
player_totals AS (
    SELECT
        batsman_name,
        SUM(matches_played) AS total_matches
    FROM player_stats
    GROUP BY batsman_name
)
SELECT
    pt.batsman_name,
    COALESCE(MAX(CASE WHEN ps.match_format = 'Test' THEN ps.matches_played END), 0) AS test_matches,
    COALESCE(MAX(CASE WHEN ps.match_format = 'Test' THEN ps.batting_avg END), 0) AS test_avg,
    COALESCE(MAX(CASE WHEN ps.match_format = 'ODI' THEN ps.matches_played END), 0) AS odi_matches,
    COALESCE(MAX(CASE WHEN ps.match_format = 'ODI' THEN ps.batting_avg END), 0) AS odi_avg,
    COALESCE(MAX(CASE WHEN ps.match_format = 'T20' THEN ps.matches_played END), 0) AS t20_matches,
    COALESCE(MAX(CASE WHEN ps.match_format = 'T20' THEN ps.batting_avg END), 0) AS t20_avg,
    pt.total_matches
FROM player_totals pt
LEFT JOIN player_stats ps
    ON pt.batsman_name = ps.batsman_name
GROUP BY pt.batsman_name, pt.total_matches
ORDER BY pt.total_matches DESC
LIMIT 20;  -- automatically picks top 20 players by total matches




































