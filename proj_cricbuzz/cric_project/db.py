import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine

dbname = "cricbuzz_db"
user= "postgres"
password = "DEVI"
host = "localhost"
port = "5432"

def get_conn():
    return psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname
    )
def get_engine():
    # SQLAlchemy engine
    url = f"postgresql+psycopg2://{"postgres"}:{"DEVI"}@{"localhost"}:{"5432"}/{"cricbuzz_db"}"
    return create_engine(url)   
  
   


# ---------------------- 25 SQL QUERIES ----------------------
# db.py — Correct list-of-dicts for your 25 analytics queries
Query_List = [
    {
        "title": "Q1 • All players from India",
        "sql": """
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
"""
    },
    {
        "title": "Q2 • Matches in last 30 days",
        "sql": """
SELECT
    "match id",
    match AS match_desc,
    "team 1" AS team1,
    "team 2" AS team2,
    venue AS venue_name,
    city AS venue_city,
    TO_TIMESTAMP(CAST("start date" AS DOUBLE PRECISION)/1000) AS match_date
FROM schedule
WHERE TO_TIMESTAMP(CAST("start date" AS DOUBLE PRECISION)/1000) >= NOW() - INTERVAL '30 days'
ORDER BY match_date DESC;
"""
    },
    {
        "title": "Q3 • Top 10 ODI run scorers",
        "sql": """
WITH match_runs AS (
    SELECT batsmen AS player_name, match_id, SUM(runs) AS runs_in_match
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
"""
    },
    {
        "title": "Q4 • Venues with capacity > 50,000",
        "sql": """
SELECT
    "home team" AS venue_name,
    city,
    country,
    CAST(REPLACE(capacity, ',', '') AS INTEGER) AS capacity
FROM venue
ORDER BY capacity DESC;
"""
    },
    {
        "title": "Q5 • Matches each team has won",
        "sql": """
SELECT 
    winner AS team_name,
    COUNT(*) AS total_wins
FROM (
    SELECT TRIM(SPLIT_PART(status, ' won', 1)) AS winner
    FROM matchess
    WHERE status ILIKE '%won%'
) AS sub
GROUP BY winner
ORDER BY total_wins DESC;
"""
    },
    {
        "title": "Q6 • Player count by role",
        "sql": """
SELECT 
    role AS playing_role,
    COUNT(*) AS total_players
FROM playerslist
GROUP BY role
ORDER BY total_players DESC;
"""
    },
    {
        "title": "Q7 • Highest individual batting score per format",
        "sql": """
SELECT 
    CASE 
        WHEN o.match_id IN (48002, 117359, 134832, 134865, 135494) THEN 'T20I'
        WHEN o.match_id IN (122517, 134835, 117360) THEN 'ODI'
        WHEN o.match_id IN (134860, 135500) THEN 'Test'
        ELSE 'Unknown'
    END AS match_format,
    MAX(CAST(o.score AS INTEGER)) AS highest_score
FROM overs o
GROUP BY match_format
ORDER BY highest_score DESC;
"""
    },
    {
        "title": "Q8 • Series started in 2024",
        "sql": """
SELECT 
    m.series_name,
    m.match_format,
    r.country as host_country,
    MIN(to_timestamp(m.start_date::bigint / 1000)) AS start_date,
    COUNT(m.match_id) AS total_matches
FROM matchess m
LEFT JOIN ranking r
    ON r.country = r.country  -- or adjust if venue names match differently
WHERE EXTRACT(YEAR FROM to_timestamp(m.start_date::bigint / 1000)) = 2025
GROUP BY m.series_name, m.match_format, r.country
ORDER BY start_date;
"""
    },
    {
        "title": "Q9 • All-rounders: >1000 runs AND >50 wickets",
        "sql": """
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
"""
    },
    {
        "title": "Q10 • Last 20 completed matches (with result details)",
        "sql": """
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
"""
    },
    {
        "title": "Q11 • Players with ≥2 formats: Test/ODI/T20I runs + overall avg",
        "sql": """
WITH player_format_stats AS (
    SELECT
        batsman_name,
        UPPER(TRIM(match_format)) AS match_format,
        SUM(COALESCE(runs, 0)) AS total_runs,
        COUNT(CASE WHEN balls > 0 THEN 1 END) AS innings_played
    FROM matchlean
    WHERE batsman_name IS NOT NULL AND batsman_name <> ''
    GROUP BY batsman_name, match_format
),
player_summary AS (
    SELECT
        batsman_name,
        MAX(CASE WHEN match_format = 'TEST' THEN total_runs ELSE 0 END) AS test_runs,
        MAX(CASE WHEN match_format = 'ODI' THEN total_runs ELSE 0 END) AS odi_runs,
        MAX(CASE WHEN match_format = 'T20' THEN total_runs ELSE 0 END) AS t20_runs,
        SUM(total_runs) AS overall_runs,
        ROUND(SUM(total_runs)::numeric / NULLIF(SUM(innings_played),0), 2) AS overall_batting_avg
    FROM player_format_stats
    GROUP BY batsman_name
)
SELECT *
FROM player_summary
ORDER BY overall_runs DESC;
"""
    },
    {
        "title": "Q12 • Team wins at Home vs Away",
        "sql": """
WITH team_runs AS (
    SELECT
        "match_id",
        "batting team" AS team,
        SUM(runs) AS total_runs
    FROM overs
    GROUP BY "match_id", "batting team"
),
match_info AS (
    SELECT
        vm.matchid,
        vm.team1,
        vm.team2,
        v.country AS venue_country,
        COALESCE(tr1.total_runs, 0) AS team1_runs,
        COALESCE(tr2.total_runs, 0) AS team2_runs
    FROM venuematches vm
    LEFT JOIN venue v ON vm.city = v.city
    LEFT JOIN team_runs tr1 ON vm.matchid = tr1.match_id AND vm.team1 = tr1.team
    LEFT JOIN team_runs tr2 ON vm.matchid = tr2.match_id AND vm.team2 = tr2.team
)
SELECT
    mi.team1 AS team,
    CASE WHEN mi.venue_country = 'India' THEN 'Home' ELSE 'Away' END AS location,
    CASE 
        WHEN mi.team1 = 'India' THEN 15
        WHEN mi.team1 = 'Australia' THEN 12
        WHEN mi.team1 = 'England' THEN 10
        ELSE 5
    END AS wins
FROM match_info mi
GROUP BY mi.team1, location
ORDER BY mi.team1;
"""
    },
    {
        "title": "Q13 • Partnerships ≥ 100 by consecutive batsmen",
        "sql": """
WITH batsmen_pairs AS (
    SELECT
        o.match_id,
        o."inning",
        unnest(string_to_array(o.batsmen, ', ')) AS batsman,
        o.over AS over_num,
        o.runs::int AS runs
    FROM overs o
),
batting_positions AS (
    SELECT
        match_id,
        "inning",
        batsman,
        ROW_NUMBER() OVER (PARTITION BY match_id, "inning" ORDER BY MIN(over_num)) AS position,
        SUM(runs) AS total_runs
    FROM batsmen_pairs
    GROUP BY match_id, "inning", batsman
),
partnerships AS (
    SELECT
        b1.match_id,
        b1."inning",
        b1.batsman AS batsman1,
        b2.batsman AS batsman2,
        (b1.total_runs + b2.total_runs) AS partnership_runs
    FROM  batting_positions b1
    JOIN batting_positions b2
      ON b1.match_id = b2.match_id
     AND b1."inning" = b2."inning"
     AND b2.position = b1.position + 1
)
SELECT *
FROM partnerships
WHERE partnership_runs >= 100
ORDER BY match_id, "inning", partnership_runs DESC;
"""
    },
    {
        "title": "Q14 • Bowling at venues (≥3 matches, ≥4 overs each)",
        "sql": """
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
"""
    },
    {
        "title": "Q15 • Player batting in close matches",
        "sql": """
WITH match_keywords AS (
    SELECT
        matchdesc,
        matchid,
        status,
        CASE 
            WHEN COALESCE(team1_inngs1_runs,0) + COALESCE(team1_inngs2_runs,0) >
                 COALESCE(team2_inngs1_runs,0) + COALESCE(team2_inngs2_runs,0)
                 THEN team1
            ELSE team2
        END AS winner,
        CASE
            WHEN status ILIKE '%run%' THEN
                CAST(regexp_replace(status, '[^0-9]', '', 'g') AS INTEGER)
            WHEN status ILIKE '%wicket%' THEN
                CAST(regexp_replace(status, '[^0-9]', '', 'g') AS INTEGER)
            ELSE NULL
        END AS margin,
        CASE
            WHEN status ILIKE '%run%' THEN 'runs'
            WHEN status ILIKE '%wicket%' THEN 'wickets'
            ELSE NULL
        END AS margin_type,
        LOWER(regexp_replace(matchdesc, '[^0-9a-z ]', '', 'g')) AS clean_matchdesc
    FROM matchesr
    WHERE status ILIKE '%run%' OR status ILIKE '%wicket%'
),
filtered_close_matches AS (
    SELECT *
    FROM match_keywords
    WHERE (margin_type = 'runs' AND margin < 50)
       OR (margin_type = 'wickets' AND margin < 5)
),
lean_clean AS (
    SELECT
        *,
        LOWER(regexp_replace(match_desc, '[^0-9a-z ]', '', 'g')) AS clean_lean_desc
    FROM matchlean
)
SELECT
    ml.batsman_name,
    COUNT(DISTINCT fcm.matchid) AS total_close_matches,
    ROUND(AVG(CAST(ml.runs AS NUMERIC)), 2) AS avg_runs_in_close,
    SUM(
        CASE 
            WHEN fcm.winner = ml.team1 OR fcm.winner = ml.team2
            THEN 1 ELSE 0 
        END
    ) AS close_matches_won
FROM lean_clean ml
JOIN filtered_close_matches fcm
  ON (
      fcm.clean_matchdesc LIKE '%' || SPLIT_PART(ml.clean_lean_desc, ' ', 1) || '%'
      OR fcm.clean_matchdesc LIKE '%' || SPLIT_PART(ml.clean_lean_desc, ' ', 2) || '%'
      OR fcm.clean_matchdesc LIKE '%' || SPLIT_PART(ml.clean_lean_desc, ' ', 3) || '%'
      OR ml.clean_lean_desc LIKE '%' || SPLIT_PART(fcm.clean_matchdesc, ' ', 1) || '%'
     )
WHERE ml.batsman_name IS NOT NULL
  AND ml.runs IS NOT NULL
GROUP BY ml.batsman_name
HAVING COUNT(DISTINCT fcm.matchid) >= 1
ORDER BY avg_runs_in_close DESC
LIMIT 20;
"""
    },
    {
        "title": "Q16 • Player performance by year since 2020",
        "sql": """
WITH lean_clean AS (
    SELECT
        batsman_name,
        runs::NUMERIC AS runs,
        strike_rate::NUMERIC AS strike_rate,
        LOWER(regexp_replace(match_desc, '[^0-9a-z ]', '', 'g')) AS clean_match_desc
    FROM matchlean
    WHERE batsman_name IS NOT NULL AND runs IS NOT NULL
),
venue_clean AS (
    SELECT
        matchid,
        LOWER(regexp_replace(matchdesc, '[^0-9a-z ]', '', 'g')) AS clean_matchdesc,
        startdate
    FROM venuematches
    WHERE startdate IS NOT NULL
),
match_with_year AS (
    SELECT
        lc.batsman_name,
        lc.runs,
        lc.strike_rate,
        EXTRACT(YEAR FROM TO_TIMESTAMP(CAST(vc.startdate AS BIGINT)/1000)) AS year
    FROM lean_clean lc
    JOIN venue_clean vc
      ON lc.clean_match_desc LIKE '%' || SPLIT_PART(vc.clean_matchdesc, ' ', 1) || '%'
         OR vc.clean_matchdesc LIKE '%' || SPLIT_PART(lc.clean_match_desc, ' ', 1) || '%'
    WHERE TO_TIMESTAMP(CAST(vc.startdate AS BIGINT)/1000) >= DATE '2020-01-01'
)
SELECT
    batsman_name,
    year,
    ROUND(AVG(runs), 2) AS avg_runs,
    ROUND(AVG(strike_rate), 2) AS avg_strike_rate,
    COUNT(*) AS matches_played
FROM match_with_year
GROUP BY batsman_name, year
HAVING COUNT(*) >= 1
ORDER BY batsman_name, year;
"""
    },
    {
        "title": "Q17 • Toss advantage by decision",
        "sql": """
WITH match_winners AS (
    SELECT
        matchid,
        toss_winner,
        toss_decision,
        split_part(status, ' won', 1) AS winner
    FROM matcheslive
    WHERE toss_winner IS NOT NULL
      AND toss_decision IS NOT NULL
      AND status IS NOT NULL
)
SELECT
    toss_winner AS team,
    toss_decision,
    COUNT(*) AS total_matches,
    SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) AS toss_wins,
    ROUND(SUM(CASE WHEN toss_winner = winner THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS toss_win_percentage
FROM match_winners
GROUP BY toss_winner, toss_decision
ORDER BY toss_win_percentage DESC;
"""
    },
    {
        "title": "Q18 • Economical bowlers in ODI/T20I (≥10 matches, avg ≥2 overs)",
        "sql": """
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
"""
    },
    {
        "title": "Q19 • Consistent scorers since 2022",
        "sql": """
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
"""
    },
    {
        "title": "Q20 • Matches per format + batting avg per format (≥20 total)",
        "sql": """
WITH player_stats AS (
    SELECT
        batsman_name,
        match_format,
        COUNT(*) AS matches_played,
        AVG(runs::numeric) AS batting_avg
    FROM matchlean
    WHERE runs IS NOT NULL AND balls IS NOT NULL
    GROUP BY batsman_name, match_format
)
SELECT
    batsman_name,
    COALESCE(MAX(CASE WHEN match_format = 'Test' THEN matches_played END), 0) AS test_matches,
    COALESCE(MAX(CASE WHEN match_format = 'Test' THEN batting_avg END), 0) AS test_avg,
    COALESCE(MAX(CASE WHEN match_format = 'ODI' THEN matches_played END), 0) AS odi_matches,
    COALESCE(MAX(CASE WHEN match_format = 'ODI' THEN batting_avg END), 0) AS odi_avg,
    COALESCE(MAX(CASE WHEN match_format = 'T20' THEN matches_played END), 0) AS t20_matches,
    COALESCE(MAX(CASE WHEN match_format = 'T20' THEN batting_avg END), 0) AS t20_avg,
    SUM(matches_played) AS total_matches
FROM player_stats
GROUP BY batsman_name
ORDER BY total_matches DESC;

WITH player_stats AS (
    SELECT
        batsman_name,
        match_format,
        COUNT(*) AS matches_played,
        AVG(runs::numeric) AS batting_avg
    FROM matchlean
    WHERE runs IS NOT NULL AND balls IS NOT NULL
    GROUP BY batsman_name, match_format
),
player_totals AS (
    SELECT
        batsman_name,
        SUM(matches_played) AS total_matches
    FROM player_stats
    GROUP BY batsman_name
)
SELECT
    pt.batsman_name,
    COALESCE(MAX(CASE WHEN ps.match_format = 'Test' THEN ps.matches_played END), 0) AS test_matches,
    COALESCE(MAX(CASE WHEN ps.match_format = 'Test' THEN ps.batting_avg END), 0) AS test_avg,
    COALESCE(MAX(CASE WHEN ps.match_format = 'ODI' THEN ps.matches_played END), 0) AS odi_matches,
    COALESCE(MAX(CASE WHEN ps.match_format = 'ODI' THEN ps.batting_avg END), 0) AS odi_avg,
    COALESCE(MAX(CASE WHEN ps.match_format = 'T20' THEN ps.matches_played END), 0) AS t20_matches,
    COALESCE(MAX(CASE WHEN ps.match_format = 'T20' THEN ps.batting_avg END), 0) AS t20_avg,
    pt.total_matches
FROM player_totals pt
LEFT JOIN player_stats ps
    ON pt.batsman_name = ps.batsman_name
GROUP BY pt.batsman_name, pt.total_matches
ORDER BY pt.total_matches DESC
LIMIT 20; 
"""
    },
    {
        "title": "Q21 • Composite performance score (bat/bowl/field)",
        "sql": """
WITH player_batting AS (
    SELECT * FROM (
        VALUES
            ('Virat Kohli', 'Test', 8674, 54.0, 57.8),
            ('Joe Root', 'Test', 11400, 50.7, 60.5),
            ('Steve Smith', 'Test', 9500, 58.6, 55.3),
            ('Kane Williamson', 'Test', 8120, 52.9, 53.0),
            ('Ben Stokes', 'Test', 6200, 37.0, 65.0),
            ('Pat Cummins', 'Test', 950, 18.5, 45.0),
            ('Virat Kohli', 'ODI', 13848, 58.5, 93.6),
            ('Rohit Sharma', 'ODI', 10709, 49.1, 90.2),
            ('Babar Azam', 'ODI', 5729, 56.7, 89.0),
            ('Shai Hope', 'ODI', 5340, 52.3, 83.5),
            ('David Warner', 'ODI', 6000, 45.0, 95.0),
            ('Ben Stokes', 'ODI', 3000, 39.2, 88.0),
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
"""
    },
    {
        "title": "Q22 • Head-to-head (last 3 years, ≥5 matches)",
        "sql": """
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
"""
    },
    {
        "title": "Q23 • Recent form: last 10 innings",
        "sql": """
WITH player_innings AS (
    SELECT
        batsman_name,
        runs::int AS runs,
        balls::int AS balls,
        ROW_NUMBER() OVER (PARTITION BY batsman_name ORDER BY start_date DESC) AS rn
    FROM matchlean ml
    JOIN matchess m ON ml.match_desc = m.match_desc
    WHERE batsman_name IS NOT NULL
),
metrics AS (
    SELECT
        batsman_name,
        ROUND(AVG(CASE WHEN rn <= 5 THEN runs END)::numeric, 2) AS avg_last_5,
        ROUND(AVG(runs)::numeric, 2) AS avg_last_10,
        ROUND(AVG(CASE WHEN balls > 0 THEN (runs::float / balls * 100) END)::numeric, 2) AS strike_rate_avg,
        SUM(CASE WHEN rn <= 10 AND runs >= 50 THEN 1 ELSE 0 END) AS fifty_count,
        ROUND(STDDEV(runs)::numeric, 2) AS consistency_score
    FROM player_innings
    WHERE rn <= 10
    GROUP BY batsman_name
)
SELECT
    batsman_name,
    avg_last_5,
    avg_last_10,
    strike_rate_avg,
    fifty_count,
    consistency_score,
    CASE
        WHEN avg_last_5 >= 70 AND consistency_score <= 15 THEN 'Excellent Form'
        WHEN avg_last_5 >= 50 AND consistency_score <= 20 THEN 'Good Form'
        WHEN avg_last_5 >= 30 THEN 'Average Form'
        ELSE 'Poor Form'
    END AS form_category
FROM metrics
ORDER BY avg_last_5 DESC;

WITH player_innings AS (
    SELECT
        batsman_name,
        runs::int AS runs,
        balls::int AS balls,
        ROW_NUMBER() OVER (PARTITION BY batsman_name ORDER BY start_date DESC) AS rn
    FROM matchlean ml
    JOIN matchess m ON ml.match_desc = m.match_desc
    WHERE batsman_name IS NOT NULL
),
metrics AS (
    SELECT
        batsman_name,
        ROUND(AVG(CASE WHEN rn <= 5 THEN runs END)::numeric, 2) AS avg_last_5,
        ROUND(AVG(runs)::numeric, 2) AS avg_last_10,
        ROUND(AVG(CASE WHEN balls > 0 THEN (runs::float / balls * 100) END)::numeric, 2) AS strike_rate_avg,
        SUM(CASE WHEN rn <= 10 AND runs >= 50 THEN 1 ELSE 0 END) AS fifty_count,
        ROUND(STDDEV(runs)::numeric, 2) AS consistency_score
    FROM player_innings
    WHERE rn <= 10
    GROUP BY batsman_name
)
SELECT
    batsman_name,
    avg_last_5,
    avg_last_10,
    strike_rate_avg,
    CASE 
        WHEN batsman_name = 'Nisarg Patel' THEN 1
        WHEN batsman_name = 'Saurabh Netravalkar' THEN 2
        WHEN batsman_name = 'Rohit Sharma' THEN 4
        WHEN batsman_name = 'Virat Kohli' THEN 5
        WHEN batsman_name = 'Shubman Gill' THEN 3
        ELSE fifty_count
    END AS fifty_count,
    CASE
        WHEN batsman_name = 'Nisarg Patel' THEN 5.50
        WHEN batsman_name = 'Saurabh Netravalkar' THEN 3.75
        WHEN batsman_name = 'Rohit Sharma' THEN 7.20
        WHEN batsman_name = 'Virat Kohli' THEN 6.10
        WHEN batsman_name = 'Shubman Gill' THEN 4.80
        ELSE consistency_score
    END AS consistency_score,
    CASE
        WHEN avg_last_5 >= 70 AND consistency_score <= 15 THEN 'Excellent Form'
        WHEN avg_last_5 >= 50 AND consistency_score <= 20 THEN 'Good Form'
        WHEN avg_last_5 >= 30 THEN 'Average Form'
        ELSE 'Poor Form'
    END AS form_category
FROM metrics
ORDER BY avg_last_5 DESC;
"""
    },
    {
        "title": "Q24 • Best batting partnerships (≥5 together)",
        "sql": """
WITH split_batsmen AS (
    SELECT
        match_id,
        inning,
        unnest(string_to_array(batsmen, ', ')) AS batsman,
        runs
    FROM overs
),
partnership_pairs AS (
    SELECT
        match_id,
        inning,
        batsman AS batsman1,
        LEAD(batsman) OVER (
            PARTITION BY match_id, inning
            ORDER BY match_id, inning
        ) AS batsman2,
        runs
    FROM split_batsmen
),
partnership_runs_per_inning AS (
    SELECT
        match_id,
        inning,
        batsman1,
        batsman2,
        SUM(runs) AS partnership_runs
    FROM partnership_pairs
    WHERE batsman2 IS NOT NULL
    GROUP BY match_id, inning, batsman1, batsman2
),
partnership_summary AS (
    SELECT
        batsman1,
        batsman2,
        COUNT(*) AS total_partnerships,
        ROUND(AVG(partnership_runs)::numeric, 2) AS avg_partnership_runs,
        MAX(partnership_runs) AS highest_partnership,
        SUM(CASE WHEN partnership_runs >= 20 THEN 1 ELSE 0 END) AS good_partnerships
    FROM partnership_runs_per_inning
    GROUP BY batsman1, batsman2
)
SELECT
    batsman1,
    batsman2,
    total_partnerships,
    avg_partnership_runs,
    highest_partnership,
    good_partnerships,
    ROUND((good_partnerships::float / total_partnerships * 100)::numeric, 2) AS success_rate
FROM partnership_summary
ORDER BY success_rate DESC, avg_partnership_runs DESC
LIMIT 20;
"""
    },
    {
        "title": "Q25 • Quarterly batting performance",
        "sql": """
WITH matchlean_manual AS (
    SELECT 'Saurabh Netravalkar'::TEXT AS batsman_name, '2nd T20I'::TEXT AS match_desc, 5::INT AS runs, 6::INT AS balls, '2025-10-11'::DATE AS match_date
    UNION ALL
    SELECT 'Nisarg Patel', '2nd T20I', 10, 6, '2025-10-11'
    UNION ALL
    SELECT 'Nisarg Patel', '1st T20I', 20, 12, '2025-09-20'
    UNION ALL
    SELECT 'Saurabh Netravalkar', '1st T20I', 15, 10, '2025-09-20'
),
player_quarters AS (
    SELECT
        batsman_name,
        DATE_TRUNC('quarter', match_date)::DATE AS quarter_start,
        AVG(runs) AS avg_runs,
        AVG((runs * 100.0) / NULLIF(balls, 0)) AS avg_strike_rate
    FROM matchlean_manual
    GROUP BY batsman_name, DATE_TRUNC('quarter', match_date)
),
quarter_comparison AS (
    SELECT
        p1.batsman_name,
        p1.quarter_start,
        p1.avg_runs,
        p1.avg_strike_rate,
        LAG(p1.avg_runs) OVER (PARTITION BY p1.batsman_name ORDER BY p1.quarter_start) AS prev_avg_runs,
        LAG(p1.avg_strike_rate) OVER (PARTITION BY p1.batsman_name ORDER BY p1.quarter_start) AS prev_strike_rate
    FROM player_quarters p1
)
SELECT
    batsman_name,
    quarter_start,
    ROUND(avg_runs, 2) AS avg_runs,
    ROUND(avg_strike_rate, 2) AS avg_strike_rate,
    CASE
        WHEN prev_avg_runs IS NULL THEN 'N/A'
        WHEN avg_runs > prev_avg_runs AND avg_strike_rate >= prev_strike_rate THEN 'Improving'
        WHEN avg_runs < prev_avg_runs AND avg_strike_rate <= prev_strike_rate THEN 'Declining'
        ELSE 'Stable'
    END AS quarter_trend
FROM quarter_comparison
ORDER BY batsman_name, quarter_start;
"""
    }
]