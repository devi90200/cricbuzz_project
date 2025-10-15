SELECT 
    m.series_name,
    m.match_format,
    r.country as host_country,
    MIN(to_timestamp(m.start_date::bigint / 1000)) AS start_date,
    COUNT(m.match_id) AS total_matches
FROM matchess m
LEFT JOIN ranking r
    ON r.country = r.country  -- or adjust if venue names match differently
WHERE EXTRACT(YEAR FROM to_timestamp(m.start_date::bigint / 1000)) = 2025
GROUP BY m.series_name, m.match_format, r.country
ORDER BY start_date;



    

































