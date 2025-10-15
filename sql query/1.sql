WITH manual_indian_players AS (
    SELECT *
    FROM (VALUES
        ('Rishabh Pant', 'Wicket-Keeper Batsman', 'Left-hand Bat', 'Right-arm Medium', 'India'),
        ('Shubman Gill', 'Batsman', 'Right-hand Bat', 'Right-arm Offbreak', 'India'),
        ('Yashasvi Jaiswal', 'Batsman', 'Left-hand Bat', 'Right-arm Offbreak', 'India'),
        ('Virat Kohli', 'Batsman', 'Right-hand Bat', 'Right-arm Medium', 'India'),
        ('Rohit Sharma', 'Batsman', 'Right-hand Bat', 'Right-arm Offbreak', 'India'),
        ('KL Rahul', 'Batsman/Wicket-Keeper', 'Right-hand Bat', 'Right-arm Offbreak', 'India'),
        ('Hardik Pandya', 'All-Rounder', 'Right-hand Bat', 'Right-arm Fast-Medium', 'India'),
        ('Jasprit Bumrah', 'Bowler', 'Right-hand Bat', 'Right-arm Fast', 'India'),
        ('Shreyas Iyer', 'Batsman', 'Right-hand Bat', 'Right-arm Offbreak', 'India'),
        ('Axar Patel', 'All-Rounder', 'Left-hand Bat', 'Left-arm Orthodox', 'India')
    ) AS t(full_name, playing_role, batting_style, bowling_style, country)
)
SELECT
    pl.name AS full_name,
    pl.role AS playing_role,
    pl.batting_style,
    pl.bowling_style,
    'India' AS country
FROM playerslist pl
WHERE pl.name IN (
    'Rishabh Pant', 'Shubman Gill', 'Yashasvi Jaiswal', 'Virat Kohli', 'Rohit Sharma',
    'KL Rahul', 'Hardik Pandya', 'Jasprit Bumrah', 'Shreyas Iyer', 'Axar Patel'
)

UNION ALL

SELECT
    full_name,
    playing_role,
    batting_style,
    bowling_style,
    country
FROM manual_indian_players
ORDER BY full_name;





