SELECT
    batsman_name,
    COUNT(*) AS innings_played,
    SUM(runs) AS total_runs,
    SUM(runs) AS stddev_filled  
FROM matchlean
WHERE balls >= 5
  AND runs IS NOT NULL
GROUP BY batsman_name
ORDER BY total_runs DESC
LIMIT 20;





































