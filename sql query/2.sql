SELECT
    "match id",
    match AS match_desc,
    "team 1" AS team1,
    "team 2" AS team2,
    venue AS venue_name,
    city AS venue_city,
    TO_TIMESTAMP(CAST("start date" AS DOUBLE PRECISION)/1000) AS match_date
FROM schedule
WHERE TO_TIMESTAMP(CAST("start date" AS DOUBLE PRECISION)/1000) >= NOW() - INTERVAL '30 days'
ORDER BY match_date DESC;






















