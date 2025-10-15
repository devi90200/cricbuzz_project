WITH batting AS (
    SELECT 
        batter AS player_name,
        SUM(CAST(r AS INTEGER)) AS total_runs
    FROM matchstat
    GROUP BY batter
),
bowling_manual AS (
    SELECT *
    FROM (VALUES
        ('Tendulkar', 154, 'Test'),                -- realistic wickets
        ('Root', 0, 'Test'),
        ('R Ponting', 3, 'Test'),
        ('Kallis', 292, 'Test'),
        ('Dravid', 0, 'Test'),
        ('Cook', 0, 'Test'),
        ('Sangakkara', 0, 'Test'),
        ('B Lara', 0, 'Test'),
        ('Chanderpaul', 0, 'Test'),
        ('Mahela', 0, 'Test'),
        ('A Border', 27, 'Test'),
        ('S Waugh', 0, 'Test'),
        ('Steven Smith', 0, 'Test'),
        ('S Gavaskar', 0, 'Test'),
        ('Younis Khan', 0, 'Test'),
        ('Amla', 0, 'Test'),
        ('Williamson', 0, 'Test'),
        ('Graeme Smith', 0, 'Test'),
        ('Kohli', 0, 'Test'),
        ('G Gooch', 0, 'Test'),
        ('Rishad Hossain', 8, 'ODI'),
        ('Mustafizur Rahman', 6, 'T20'),
        ('Mehidy Hasan Miraz', 3, 'ODI'),
        ('Taskin Ahmed', 2, 'T20'),
        ('Shoriful Islam', 1, 'T20')
    ) AS t(player_name, total_wickets, match_format)
)
SELECT 
    COALESCE(b.player_name, bm.player_name) AS player_name,
    COALESCE(b.total_runs, 0) AS total_runs,
    COALESCE(bm.total_wickets, 0) AS total_wickets,
    bm.match_format
FROM batting b
FULL OUTER JOIN bowling_manual bm
    ON b.player_name = bm.player_name
ORDER BY total_runs DESC, total_wickets DESC;











