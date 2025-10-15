SELECT 
    role AS playing_role,
    COUNT(*) AS total_players
FROM playerslist
GROUP BY role
ORDER BY total_players DESC;






























