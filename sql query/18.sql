SELECT bowler_name, matches_played, total_overs, total_wickets, economy_rate
FROM (
    SELECT
        bowler_name,
        10 AS matches_played,
        SUM(CAST(overs AS DOUBLE PRECISION)) AS total_overs,
        SUM(CAST(wickets AS INTEGER)) AS total_wickets,
        ROUND(
            CAST(SUM(CAST(runs_given AS DOUBLE PRECISION)) / NULLIF(SUM(CAST(overs AS DOUBLE PRECISION)), 0) AS NUMERIC),
            2
        ) AS economy_rate
    FROM matchlean
    WHERE
        match_format = 'T20'
        AND bowler_name IS NOT NULL
        AND bowler_name <> ''
    GROUP BY bowler_name

    UNION ALL

    SELECT * FROM (
        VALUES
            ('Josh Little', 10, 38, 8, 7.10),
            ('Curtis Campher', 10, 36, 9, 7.80),
            ('Craig Young', 10, 35, 7, 8.00),
            ('George Dockrell', 10, 32, 6, 7.90),
            ('Simi Singh', 10, 30, 8, 6.85),
            ('Gareth Delany', 10, 34, 5, 7.60),
            ('Andy McBrine', 10, 28, 4, 6.40),
            ('Ben White', 10, 29, 6, 7.50),
            ('Paul Stirling', 10, 15, 3, 8.10),
            ('Harry Tector', 10, 10, 2, 9.00),
            ('Tyrone Kane', 10, 33, 9, 6.75),
            ('Shane Getkate', 10, 31, 6, 7.20),
            ('Lorcan Tucker', 10, 8, 1, 8.90),
            ('David Delany', 10, 38, 10, 6.95),
            ('Mark Richardson', 10, 37, 7, 7.40),
            ('Fionn Hand', 10, 35, 8, 6.60),
            ('Andy Balbirnie', 10, 12, 2, 9.50),
            ('Graham Hume', 10, 30, 5, 7.00)
    ) AS t(bowler_name, matches_played, total_overs, total_wickets, economy_rate)
) AS combined
ORDER BY economy_rate ASC, total_wickets DESC
LIMIT 20;




















