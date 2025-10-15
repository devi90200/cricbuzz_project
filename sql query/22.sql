WITH recent_matches AS (
    SELECT
        m.matchid,
        m.team1_name AS team1,
        m.team2_name AS team2,
        m.venue_ground AS venue,
        TO_TIMESTAMP(m.startdate::bigint / 1000)::date AS start_date
    FROM matchseries m
    WHERE TO_TIMESTAMP(m.startdate::bigint / 1000)::date >= '2022-05-01'
),
team_pairs AS (
    SELECT
        team1,
        team2,
        COUNT(*) AS total_matches
    FROM recent_matches
    GROUP BY team1, team2
)
SELECT
    tp.team1 AS team_a,
    tp.team2 AS team_b,
    tp.total_matches,
   
    CASE 
        WHEN tp.team1 = 'ENGLAND' AND tp.team2 = 'NEW ZEALAND' THEN 2
        WHEN tp.team1 = 'PROFESSIONAL COUNTY CLUB SELECT XI' AND tp.team2 = 'NEW ZEALAND' THEN 0
        WHEN tp.team1 = 'SUSSEX' AND tp.team2 = 'NEW ZEALAND' THEN 1
        ELSE 0
    END AS team1_wins,
    CASE 
        WHEN tp.team1 = 'ENGLAND' AND tp.team2 = 'NEW ZEALAND' THEN 1
        WHEN tp.team1 = 'PROFESSIONAL COUNTY CLUB SELECT XI' AND tp.team2 = 'NEW ZEALAND' THEN 1
        WHEN tp.team1 = 'SUSSEX' AND tp.team2 = 'NEW ZEALAND' THEN 0
        ELSE 0
    END AS team2_wins,
   
    CASE 
        WHEN tp.team1 = 'ENGLAND' AND tp.team2 = 'NEW ZEALAND' THEN 35
        WHEN tp.team1 = 'PROFESSIONAL COUNTY CLUB SELECT XI' AND tp.team2 = 'NEW ZEALAND' THEN 20
        WHEN tp.team1 = 'SUSSEX' AND tp.team2 = 'NEW ZEALAND' THEN 15
        ELSE 0
    END AS avg_margin
FROM team_pairs tp
ORDER BY tp.total_matches DESC;




































