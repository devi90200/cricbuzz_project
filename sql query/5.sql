SELECT 
    winner AS team_name,
    COUNT(*) AS total_wins
FROM (
    SELECT
        TRIM(SPLIT_PART(status, ' won', 1)) AS winner
    FROM matchess
    WHERE status ILIKE '%won%'
) AS sub
GROUP BY winner
ORDER BY total_wins DESC;





























