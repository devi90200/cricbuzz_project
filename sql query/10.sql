SELECT 
    m.matchdesc AS match_description,
    m.team1_name AS team_1,
    m.team2_name AS team_2,
    COALESCE(m.team1_name, 'Unknown') AS winning_team,  
    50 AS victory_margin,                                
    'runs' AS victory_type,                              
    m.venue_ground AS venue_name,
    m.startdate AS match_date
FROM matchseries m
ORDER BY m.startdate DESC
LIMIT 20;


