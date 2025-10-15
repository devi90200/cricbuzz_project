WITH player_batting AS (
    SELECT * FROM (
        VALUES
            -- Test Players
            ('Virat Kohli', 'Test', 8674, 54.0, 57.8),
            ('Joe Root', 'Test', 11400, 50.7, 60.5),
            ('Steve Smith', 'Test', 9500, 58.6, 55.3),
            ('Kane Williamson', 'Test', 8120, 52.9, 53.0),
            ('Ben Stokes', 'Test', 6200, 37.0, 65.0),
            ('Pat Cummins', 'Test', 950, 18.5, 45.0),

            -- ODI Players
            ('Virat Kohli', 'ODI', 13848, 58.5, 93.6),
            ('Rohit Sharma', 'ODI', 10709, 49.1, 90.2),
            ('Babar Azam', 'ODI', 5729, 56.7, 89.0),
            ('Shai Hope', 'ODI', 5340, 52.3, 83.5),
            ('David Warner', 'ODI', 6000, 45.0, 95.0),
            ('Ben Stokes', 'ODI', 3000, 39.2, 88.0),

            -- T20 Players
            ('Suryakumar Yadav', 'T20', 2200, 45.5, 172.5),
            ('Jos Buttler', 'T20', 3000, 34.0, 140.0),
            ('Glenn Maxwell', 'T20', 2500, 31.0, 155.0),
            ('Hardik Pandya', 'T20', 1700, 28.5, 145.0),
            ('Mark Adair', 'T20', 100, 12.5, 110.0),
            ('Barry McCarthy', 'T20', 80, 10.5, 100.0),
            ('Nisarg Patel', 'T20', 200, 25.0, 120.0),
            ('Saurabh Netravalkar', 'T20', 120, 18.0, 95.0)
    ) AS t(player_name, match_format, total_runs, batting_avg, strike_rate)
),
player_bowling AS (
    SELECT * FROM (
        VALUES
            ('Pat Cummins', 'Test', 270, 22.0, 2.8),
            ('Ben Stokes', 'Test', 200, 32.5, 3.1),
            ('Mark Adair', 'T20', 80, 22.0, 7.8),
            ('Barry McCarthy', 'T20', 75, 23.5, 8.0),
            ('Hardik Pandya', 'T20', 70, 27.0, 8.5),
            ('Saurabh Netravalkar', 'T20', 60, 21.0, 6.9),
            ('Nisarg Patel', 'T20', 50, 25.5, 7.0),
            ('Virat Kohli', 'ODI', 5, 45.0, 5.5),
            ('Ben Stokes', 'ODI', 40, 35.0, 6.1),
            ('Rohit Sharma', 'ODI', 8, 40.0, 6.5)
    ) AS t(player_name, match_format, wickets_taken, bowling_avg, economy_rate)
),
player_fielding AS (
    SELECT * FROM (
        VALUES
            ('Virat Kohli', 'Test', 180, 0),
            ('Joe Root', 'Test', 160, 0),
            ('Steve Smith', 'Test', 170, 0),
            ('Kane Williamson', 'Test', 150, 0),
            ('Ben Stokes', 'Test', 120, 0),
            ('Rohit Sharma', 'ODI', 100, 0),
            ('David Warner', 'ODI', 95, 0),
            ('Babar Azam', 'ODI', 85, 0),
            ('Jos Buttler', 'T20', 90, 20),
            ('Suryakumar Yadav', 'T20', 60, 0),
            ('Hardik Pandya', 'T20', 50, 0),
            ('Glenn Maxwell', 'T20', 70, 0),
            ('Mark Adair', 'T20', 30, 0),
            ('Barry McCarthy', 'T20', 25, 0),
            ('Nisarg Patel', 'T20', 20, 5),
            ('Saurabh Netravalkar', 'T20', 15, 0)
    ) AS t(player_name, match_format, total_catches, total_stumpings)
),
combined AS (
    SELECT
        COALESCE(b.player_name, bw.player_name, f.player_name) AS player_name,
        COALESCE(b.match_format, bw.match_format, f.match_format) AS match_format,

        COALESCE(b.total_runs, 0) AS runs_scored,
        COALESCE(b.batting_avg, 0) AS batting_average,
        COALESCE(b.strike_rate, 0) AS strike_rate,

        COALESCE(bw.wickets_taken, 0) AS wickets_taken,
        COALESCE(bw.bowling_avg, 50) AS bowling_average,
        COALESCE(bw.economy_rate, 6) AS economy_rate,

        COALESCE(f.total_catches, 0) AS catches,
        COALESCE(f.total_stumpings, 0) AS stumpings
    FROM player_batting b
    FULL OUTER JOIN player_bowling bw
        ON b.player_name = bw.player_name AND b.match_format = bw.match_format
    FULL OUTER JOIN player_fielding f
        ON COALESCE(b.player_name, bw.player_name) = f.player_name
        AND COALESCE(b.match_format, bw.match_format) = f.match_format
),
ranked AS (
    SELECT
        player_name,
        match_format,
        runs_scored,
        batting_average,
        strike_rate,
        wickets_taken,
        bowling_average,
        economy_rate,
        catches,
        stumpings,

        ((runs_scored * 0.01) + (batting_average * 0.5) + (strike_rate * 0.3)) AS batting_points,
        ((wickets_taken * 2) + ((50 - bowling_average) * 0.5) + ((6 - economy_rate) * 2)) AS bowling_points,
        ((catches + stumpings) * 1.5) AS fielding_points,

        ((runs_scored * 0.01) + (batting_average * 0.5) + (strike_rate * 0.3))
        + ((wickets_taken * 2) + ((50 - bowling_average) * 0.5) + ((6 - economy_rate) * 2))
        + ((catches + stumpings) * 1.5) AS total_score
    FROM combined
)
SELECT
    match_format,
    player_name,
    ROUND(runs_scored, 1) AS runs,
    ROUND(batting_average, 2) AS batting_avg,
    ROUND(strike_rate, 2) AS strike_rate,
    wickets_taken,
    ROUND(bowling_average, 2) AS bowling_avg,
    ROUND(economy_rate, 2) AS economy,
    catches,
    stumpings,
    ROUND(batting_points, 2) AS batting_points,
    ROUND(bowling_points, 2) AS bowling_points,
    ROUND(fielding_points, 2) AS fielding_points,
    ROUND(total_score, 2) AS total_score
FROM ranked
ORDER BY match_format, total_score DESC
LIMIT 20;



































