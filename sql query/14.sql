SELECT
    ml.bowler_name,
    vm.venue,
    COUNT(*) AS matches_played,
    SUM(CAST(ml.wickets AS INTEGER)) AS total_wickets,
    ROUND(AVG(CAST(ml.economy AS NUMERIC)), 2) AS avg_economy
FROM matchlean ml
JOIN venuematches vm 
    ON LOWER(vm.venue) LIKE LOWER('%' || 'Basin Reserve' || '%')
WHERE CAST(ml.overs AS NUMERIC) >= 4
GROUP BY ml.bowler_name, vm.venue
HAVING COUNT(*) >= 1
ORDER BY total_wickets DESC;














