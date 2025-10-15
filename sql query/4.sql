SELECT
    "home team" AS venue_name,
    city,
    country,
    CAST(REPLACE(capacity, ',', '') AS INTEGER) AS capacity
FROM venue
ORDER BY capacity DESC;





























