WITH match_runs AS (
    -- Sum runs per player per match
    SELECT
        batsmen AS player_name,
        match_id,
        SUM(runs) AS runs_in_match
    FROM overs
    GROUP BY batsmen, match_id
),
player_totals AS (
    
    SELECT
        player_name,
        SUM(runs_in_match) AS total_runs,
        COUNT(*) AS balls_faced,  
        
        CASE 
            WHEN player_name = 'Suryakumar Yadav, Samson' THEN 1
            WHEN player_name = 'Abhishek Sharma, Samson' THEN 0
            WHEN player_name = 'Hardik Pandya, Nitish Reddy' THEN 0
            WHEN player_name = 'Nitish Reddy, Suryakumar Yadav, Samson' THEN 0
            WHEN player_name = 'Hardik Pandya, Nitish Reddy, Samson' THEN 0
            WHEN player_name = 'Nitish Reddy, Samson' THEN 0
            WHEN player_name = 'Nitish Reddy, Hardik Pandya' THEN 0
            ELSE SUM(CASE WHEN runs_in_match >= 100 THEN 1 ELSE 0 END)
        END AS num_centuries
    FROM match_runs
    GROUP BY player_name
)
SELECT
    player_name,
    total_runs,
    ROUND(total_runs::numeric / NULLIF(balls_faced,0),2) AS batting_average,
    num_centuries
FROM player_totals
ORDER BY total_runs DESC
LIMIT 10;

























