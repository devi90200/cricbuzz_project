import sqlite3

DB_PATH = "cricbuzz.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def ensure_schema_and_seed():
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript("""
                      DROP TABLE IF EXISTS players;
                      DROP TABLE IF EXISTS teams;
                      DROP TABLE IF EXISTS venues;
                      DROP TABLE IF EXISTS series;
                      DROP TABLE IF EXISTS matches;
                      DROP TABLE IF EXISTS batting_stats;
                      DROP TABLE IF EXISTS bowling_stats;
                      DROP TABLE IF EXISTS player_match_batting;
                      DROP TABLE IF EXISTS player_match_bowling;
                      DROP TABLE IF EXISTS partnerships;
                      DROP TABLE IF EXISTS player_fielding;
                      
                      CREATE TABLE players (

                      player_id INTEGER PRIMARY KEY,
                      full_name VARCHAR(100),
                      country VARCHAR(100),
                      role VARCHAR(100),
                      batting_style VARCHAR(100),
                      bowling_style VARCHAR(100)
                      );

                      CREATE TABLE teams (
                      team_id INTEGER PRIMARY KEY,
                      team_name VARCHAR(100),
                      country VARCHAR(100)
                      );

                      CREATE TABLE venues (
                      venue_id INTEGER PRIMARY KEY,
                      name VARCHAR(100),
                      city VARCHAR(100),
                      country VARCHAR(100),
                      capacity INTEGER
                      );

                      CREATE TABLE series (
                      series_id INTEGER PRIMARY KEY,
                      name VARCHAR(100),
                      host_country VARCHAR(100),
                      match_type VARCHAR(100),
                      start_date DATE,
                      total_matches INTEGER
                      );

                      CREATE TABLE matches (
                      match_id INTEGER PRIMARY KEY,
                      description VARCHAR(100),
                      format VARCHAR(100),
                      series_id INTEGER,
                      team1_id INTEGER,
                      team2_id INTEGER,
                      venue_id INTEGER,
                      match_date DATE,
                      winner_team_id INTEGER,
                      toss_winner_team_id INTEGER,
                      toss_decision VARCHAR(100),
                      result_margin INTEGER,
                      result_type VARCHAR(100)
                    );

                      CREATE TABLE batting_stats (
                      player_id INTEGER,
                      format VARCHAR(100),
                      matches_played INTEGER,
                      runs INTEGER,
                      average REAL,
                      strike_rate REAL,
                      centuries INTEGER,
                      half_centuries INTEGER
                      );

                      CREATE TABLE bowling_stats (
                      player_id INTEGER,
                      format VARCHAR(100),
                      matches_played INTEGER,
                      wickets INTEGER,
                      bowling_average REAL,
                      economy REAL
                      );

                      CREATE TABLE player_match_batting (
                      match_id INTEGER,
                      player_id INTEGER,
                      team_id INTEGER,
                      innings_no INTEGER,
                      position INTEGER,
                      runs INTEGER,
                      balls_faced INTEGER,
                      strike_rate REAL
                      );

                      CREATE TABLE player_match_bowling (
                      match_id INTEGER,
                      player_id INTEGER,
                      team_id INTEGER,
                      overs REAL,
                      balls_bowled INTEGER,
                      runs_conceded INTEGER,
                      wickets INTEGER,
                      economy REAL
                      );

                      CREATE TABLE partnerships (
                      match_id INTEGER,
                      innings_no INTEGER,
                       pos1 INTEGER,
                      pos2 INTEGER,
                      player1_id INTEGER,
                      player2_id INTEGER,
                      runs INTEGER
                      );

                      CREATE TABLE player_fielding (
                      player_id INTEGER,
                      format VARCHAR(100),
                      catches INTEGER,
                      stumpings INTEGER
                    );
                      """)
    players = [
    (1, "Virat Kohli", "India", "Batsman", "Right-hand bat", "Right-arm medium"),
    (2, "Rohit Sharma", "India", "Batsman", "Right-hand bat", "Right-arm offbreak"),
    (3, "Ben Stokes", "England", "Allrounder", "Left-hand bat", "Right-arm fast-medium"),
    (4, "Jasprit Bumrah", "India", "Bowler", "Right-hand bat", "Right-arm fast"),
    (5, "Joe Root", "England", "Batsman", "Right-hand bat", "Right-arm offbreak"),
    (6, "KL Rahul", "India", "Wicket-keeper", "Right-hand bat", "Right-arm offbreak"),
    (7, "Rishabh Pant", "India", "Wicket-keeper", "Left-hand bat", "Right-arm offbreak"),
    (8, "Hardik Pandya", "India", "Allrounder", "Right-hand bat", "Right-arm medium-fast"),
    (9, "Shubman Gill", "India", "Batsman", "Right-hand bat", "Right-arm offbreak"),
    (10,"Sam Curran", "England", "Allrounder", "Left-hand bat", "Left-arm medium-fast"),
    (11,"Moeen Ali", "England", "Allrounder", "Left-hand bat", "Right-arm offbreak"),
    (12,"Kuldeep Yadav", "India", "Bowler", "Left-hand bat", "Left-arm chinaman"),
    (13,"Bhuvneshwar Kumar", "India", "Bowler", "Right-hand bat", "Right-arm medium"),
    (14,"Mark Wood", "England", "Bowler", "Right-hand bat", "Right-arm fast"),
    (15,"Jonny Bairstow", "England", "Batsman", "Right-hand bat", "Right-arm medium"),
    (16,"Ravindra Jadeja", "India", "Allrounder", "Left-hand bat", "Left-arm orthodox"),
    (17,"Ollie Pope", "England", "Batsman", "Right-hand bat", "Right-arm offbreak"),
    (18,"Shreyas Iyer", "India", "Batsman", "Right-hand bat", "Right-arm legbreak"),
    (19,"Jos Buttler", "England", "Wicket-keeper", "Right-hand bat", "Right-arm medium"),
    (20,"Axar Patel", "India", "Allrounder", "Left-hand bat", "Left-arm orthodox"),
    (21,"MS Dhoni", "India", "Wicket-keeper", "Right-hand bat", "Right-arm medium"),
    (22,"Yuvraj Singh", "India", "Allrounder", "Left-hand bat", "Left-arm orthodox"),
    (23, "Pat Cummins", "Australia", "Bowler", "Right-hand bat", "Right-arm fast"),
    (24,"Steve Smith", "Australia", "Batsman", "Right-hand bat", "Right-arm legbreak"),
    (25,"Babar Azam", "Pakistan", "Batsman", "Right-hand bat", "Right-arm offbreak"),
    (26,"Rashid Khan", "Afghanistan", "Bowler", "Right-hand bat", "Legbreak googly"),
    (27,"Trent Boult", "New Zealand", "Bowler", "Right-hand bat", "Left-arm fast-medium"),
    (28,"Quinton de Kock", "South Africa", "Wicket-keeper", "Left-hand bat", "None"),
    (29, "Kusal Mendis", "Sri Lanka", "Wicket-keeper", "Right-hand bat", "None"),
    (30,"Nicholas Pooran", "West Indies", "Wicket-keeper", "Left-hand bat", "Right-arm offbreak")
    ]
    teams = [
    (1, "India", "India"),
    (2, "Sri Lanka", "Sri Lanka"),
    (3, "England", "England"),
    (4, "Australia", "Australia"),
    (5, "Pakistan", "Pakistan"),
    (6, "Afghanistan", "Afghanistan"),
    (7, "South Africa", "South Africa"),
    (8, "New Zealand", "New Zealand"),
    (9, "Bangladesh", "Bangladesh"),
    (10, "West Indies", "West Indies")
    ]

    venues = [

    (1, "Eden Gardens", "Kolkata", "India", 66000),
    (2, "Lords", "London", "England", 30000),
    (3, "MCG", "Melbourne", "Australia", 100000),
    (4, "Gaddafi Stadium", "Lahore", "Pakistan", 27000),
    (5, "R. Premadasa Stadium", "Colombo", "Sri Lanka", 35000),
    (6, "Old Trafford", "Manchester", "England", 26000),
    (7, "Sharjah Cricket Stadium", "Sharjah", "UAE", 17000),
    (8, "SuperSport Park", "Centurion", "South Africa", 22000),
    (9, "Pallekele Stadium", "Kandy", "Sri Lanka", 35000)

    ]

    series = [
    (1, "India vs Sri Lanka ODI Series 2025", "Sri Lanka", "ODI", "2025-08-15", 3),
    (2, "England vs Australia Test Series 2025", "England", "Test", "2025-08-10", 5),
    (3, "Pak vs Afg T20I Series 2025", "UAE", "T20I", "2025-08-18", 2),
    (4, "South Africa vs NZ Tour 2025", "South Africa", "Mixed", "2025-08-09", 3),
    (5, "Bangladesh vs WI ODI Series 2025", "Bangladesh", "ODI", "2025-08-10", 3),
    (6, "Pakistan vs Ireland ODI 2025", "Ireland", "ODI", "2025-08-12", 1),
    (7, "India vs Zimbabwe T20I Series 2025", "Zimbabwe", "T20I", "2025-08-05", 5),
    (8, "India vs England ODI Series 2024", "India", "ODI", "2024-02-01", 3),
    (9, "Pakistan vs Australia ODI Series 2024", "Pakistan", "ODI", "2024-03-10", 3)
    ]

    matches = [
    (1,"India vs SL, 3rd ODI","ODI",1,1,2,1,"2025-08-25",1,1,"bat",5,"wickets"),
    (2,"Eng vs Aus, 4th Test","Test",2,3,4,2,"2025-08-24",3,3,"bat",45,"innings"),
    (3,"Pak vs Afg, 2nd T20I","T20I",3,5,6,3,"2025-08-23",6,5,"bat",8,"wickets"),
    (4,"SA vs NZ, 1st ODI","ODI",4,7,8,4,"2025-08-22",8,7,"bowl",3,"wickets"),
    (5,"India vs SL, 2nd ODI","ODI",1,1,2,5,"2025-08-20",1,1,"bat",122,"runs"),
    (6,"Eng vs Aus, 3rd Test","Test",2,3,4,6,"2025-08-19",None,3,"bat",None,"draw"),
    (7,"Pak vs Afg, 1st T20I","T20I",3,5,6,3,"2025-08-18",5,5,"bat",12,"runs"),
    (8,"Ban vs WI, 3rd ODI","ODI",5,9,10,5,"2025-08-17",10,9,"bowl",4,"wickets"),
    (9,"India vs SL, 1st ODI","ODI",1,1,2,1,"2025-08-16",1,2,"bat",7,"wickets"),
    (10,"Eng vs Aus, 2nd Test","Test",2,3,4,2,"2025-08-15",4,3,"bowl",6,"wickets"),
    (11,"SA vs NZ, 2nd T20I","T20I",4,7,8,4,"2025-08-14",7,7,"bat",9,"wickets"),
    (12,"Ban vs WI, 2nd ODI","ODI",5,9,10,5,"2025-08-13",9,9,"bat",85,"runs"),
    (13,"Pak vs Ire, Only ODI","ODI",6,5,3,3,"2025-08-12",5,5,"bat",210,"runs"),
    (14,"Eng vs Aus, 1st Test","Test",2,3,4,2,"2025-08-11",None,3,"bat",None,"draw"),
    (15,"Ban vs WI, 1st ODI","ODI",5,9,10,5,"2025-08-10",10,9,"bowl",3,"wickets"),
    (16,"SA vs NZ, 1st T20I","T20I",4,7,8,4,"2025-08-09",8,8,"bat",7,"runs"),
    (17,"Pak vs Afg, Only ODI","ODI",3,5,6,3,"2025-08-08",5,5,"bat",5,"wickets"),
    (18,"India vs Zim, 5th T20I","T20I",7,1,2,1,"2025-08-07",1,1,"bat",56,"runs"),
    (19,"India vs Zim, 4th T20I","T20I",7,1,2,1,"2025-08-06",2,1,"bowl",3,"wickets"),
    (20,"India vs Zim, 3rd T20I","T20I",7,1,2,1,"2025-08-05",1,1,"bat",8,"wickets"),
    (21, "India vs Eng, 1st ODI","ODI",8,1,3,1,"2024-02-01",1,1,"bat",6,"wickets"),
    (22, "India vs Eng, 2nd ODI","ODI",8,1,3,1,"2024-02-03",3,1,"bowl",40,"runs"),
    (23, "India vs Eng, 3rd ODI","ODI",8,1,3,1,"2024-02-05",1,3,"bat",5,"wickets"),
    (24, "Pak vs Aus, 1st ODI","ODI",9,5,4,4,"2024-03-10",5,5,"bat",80,"runs"),
    (25, "Pak vs Aus, 2nd ODI","ODI",9,5,4,4,"2024-03-12",4,4, "bowl",5,"wickets"),
    (26, "Pak vs Aus, 3rd ODI","ODI",9,5,4,4,"2024-03-14",5,4,"bat",20,"runs"),
    (101,"India vs Aus, ODI","ODI",1,1,4,1,"2025-08-21",1,1,"bat",65,"runs"),
    (102,"Eng vs Pak, T20I","T20I",3,3,5,2,"2025-08-20",5,3,"bowl",7,"wickets"),
    (103,"SA vs NZ, ODI","ODI",4,7,8,4,"2025-08-19",7,7,"bat",4,"wickets"),
    (104,"WI vs SL, T20I","T20I",7,10,2,5,"2025-08-18",10,10,"bat",25,"runs"),
    (105,"Ban vs Ind, ODI","ODI",5,9,1,3,"2025-08-17",1,1,"bat",122,"runs"),
    (106,"Ind vs Aus,ODI","ODI",1,2,1,1,"2020-01-15",1,1,"bat",58,"runs"),
    (107,"Ind vs Aus,ODI","ODI",1,2,1,1,"2020-01-15",1,1,"bowl",2,"wickets"),
    (108,"Pak vs SL, T20","T20",2,3,2,1,"2020-02-10",1,1,"bat",34,"runs"),
    (109,"Pak vs SL, T20","T20",2,3,2,1,"2020-02-10",1,1,"bowl",1,"wickets"),
    (110,"Eng vs NZ,ODI","ODI",4,5,3,2,"2020-03-12",1,1,"bat",72,"runs"),
    (111,"Eng vs NZ, ODI","ODI",4,5,3,2,"2020-03-12",1,1,"bowl",3,"wickets"),
    (112,"SA vs WI,T20","T20",6,7,4,1,"2021-05-05",1,1,"bat",41,"runs"),
    (113,"SA vs WI,T20","T20",6,7,4,1,"2021-05-05",1,1,"bowl",2,"wickets"),
    (114,"Ban vs Pak,ODI","ODI",5,8,5,2,"2021-08-17",1,1,"bat",122,"runs"),
    (115,"Ban vs Pak,ODI","ODI",5,8,5,2,"2021-08-17",1,1,"bowl",1,"wickets"),
    (116,"Aus vs Ind,T20","T20",1,2,6,1,"2022-02-20",1,1,"bat",56,"runs"),
    (117,"Aus vs Ind, T20","T20",1,2,6,1,"2022-02-20",1,1,"bowl",3,"wickets"),
    (118,"NZ vs SA,ODI","ODI",3,4,7,2,"2022-03-15",1,1,"bat",87,"runs"),
    (119,"NZ vs SA,ODI","ODI",3,4,7,2,"2022-03-15",1,1,"bowl",2,"wickets"),
    (120,"WI vs Eng,ODI","ODI",5,6,8,1,"2023-05-05",1,1,"bat",68,"runs"),
    (121,"WI vs Eng,ODI","ODI",5,6,8,1,"2023-05-05",1,1,"bowl",1,"wickets"),
    (122,"SL vs Ban,ODI","ODI",7,8,9,2,"2023-05-07",1,1,"bat",91,"runs"),
    (123,"SL vs Ban,ODI","ODI",7,8,9,2,"2023-05-07",1,1,"bowl",4,"wickets"),
    (124,"Ind vs Pak,T20","T20",1,3,10,1,"2023-09-10",1,1,"bat",45,"runs"),
    (125,"Ind vs Pak, T20","T20",1,3,10,1,"2023-09-10",1,1,"bowl",2,"wickets")
    ]


    batting_stats = ([
    # Virat Kohli
    (1, "Test", 110, 8700, 49.5, 56.2, 28, 29),
    (1, "ODI", 280, 13000, 57.5, 93.2, 46, 65),
    (1, "T20I", 115, 4000, 52.7, 137.0, 1, 37),
    (1, "ODI", 5, 280, 56.0, 92.0, 1, 3),
    (1, "T20I", 5, 210, 42.0, 135.0, 0, 4),
    (1, "Test", 5, 450, 45.0, 55.0, 1, 2),

    # Rohit Sharma
    (2, "Test", 55, 3700, 46.5, 55.3, 10, 15),
    (2, "ODI", 250, 10000, 49.5, 88.1, 30, 55),
    (2, "T20I", 148, 3850, 31.3, 138.9, 4, 29),
    (2, "ODI", 5, 300, 60.0, 90.0, 1, 2),
    (2, "T20I", 5, 190, 38.0, 140.0, 0, 3),
    (2, "Test", 5, 400, 50.0, 54.0, 0, 3),

    # Joe Root
    (5, "Test", 135, 11500, 49.0, 54.1, 30, 50),
    (5, "ODI", 150, 8000, 52.0, 87.0, 20, 40),
    (5, "T20I", 32, 900, 35.0, 128.0, 0, 5),
    (5, "ODI", 5, 280, 56.0, 86.0, 1, 2),
    (5, "T20I", 5, 120, 24.0, 130.0, 0, 1),
    (5, "Test", 5, 420, 52.5, 53.0, 1, 2),

    # Ben Stokes
    (3, "Test", 97, 6300, 36.5, 58.0, 13, 28),
    (3, "ODI", 105, 3000, 40.0, 92.5, 3, 20),
    (3, "T20I", 43, 750, 25.0, 134.0, 0, 2),
    (3, "ODI", 5, 220, 44.0, 88.0, 0, 2),
    (3, "T20I", 5, 150, 30.0, 132.0, 0, 1),
    (3, "Test", 5, 300, 37.5, 57.0, 0, 2),


    # Babar Azam
    (25, "Test", 52, 3900, 47.0, 55.5, 9, 26),
    (25, "ODI", 120, 5400, 58.0, 92.5, 19, 32),
    (25, "T20I", 104, 3700, 41.5, 130.0, 3, 31),
    (25, "ODI", 5, 290, 58.0, 91.0, 1, 2),
    (25, "T20I", 5, 200, 40.0, 128.0, 0, 3),
    (25, "Test", 5, 410, 47.0, 56.0, 1, 2),

    # MS Dhoni
    (21, "Test", 90, 4876, 38.1, 59.1, 6, 33),
    (21, "ODI", 350, 10500, 50.0, 88.0, 10, 70),
    (21, "T20I", 98, 1600, 35.0, 125.0, 0, 2),
    (21, "ODI", 5, 250, 50.0, 87.0, 0, 2),
    (21, "T20I", 5, 140, 28.0, 124.0, 0, 1),
    (21, "Test", 5, 350, 43.0, 58.0, 0, 1),

    # Yuvraj Singh
    (22, "Test", 40, 1900, 33.0, 54.2, 3, 11),
    (22, "ODI", 300, 8700, 36.5, 89.0, 14, 52),
    (22, "T20I", 58, 1177, 28.0, 136.0, 0, 8),
    (22, "ODI", 5, 230, 46.0, 90.0, 0, 2),
    (22, "T20I", 5, 120, 24.0, 135.0, 0, 1),
    (22, "Test", 5, 270, 36.0, 55.0, 0, 1),

    # Hardik Pandya
    (8, "ODI", 5, 160, 32.0, 95.0, 0, 1),
    (8, "T20I", 5, 130, 26.0, 140.0, 0, 2),

    # Ravindra Jadeja
    (16, "ODI", 5, 180, 36.0, 85.0, 0, 1),
    (16, "T20I", 5, 110, 22.0, 130.0, 0, 1),

    # Sam Curran
    (10, "ODI", 5, 120, 24.0, 90.0, 0, 1),
    (10, "T20I", 5, 90, 18.0, 125.0, 0, 0),

    # Moeen Ali
    (11, "ODI", 5, 140, 28.0, 92.0, 0, 1),
    (11, "T20I", 5, 100, 20.0, 130.0, 0, 1),

    (3, "ODI", 120, 2500, 35.0, 87.2, 5, 12),    # Ben Stokes
    (8, "ODI", 90, 1800, 32.0, 96.5, 2, 8),      # Hardik Pandya
    (16,"ODI", 200, 2200, 30.5, 85.0, 3, 10),    # Ravindra Jadeja
    (22,"ODI", 300, 8700, 36.5, 89.0, 14, 52),   # Yuvraj Singh
    (10,"ODI", 70, 1200, 28.0, 90.5, 1, 6),      # Sam Curran
    (11,"ODI", 110, 2200, 29.5, 92.0, 2, 9)      # Moeen Ali
    ])

    bowling_stats =([

    # India Bowlers
    (4, "ODI", 100, 180, 21.5, 4.5),   # Bumrah
    (13,"ODI", 80, 95, 27.0, 4.8),     # Bhuvneshwar Kumar

    # England Bowlers
    (14,"ODI", 60, 85, 32.0, 5.5),     # Mark Wood
    (11,"ODI", 90, 110, 29.5, 5.2),    # Moeen Ali (AR)

    # Pakistan Bowlers
    (27,"ODI", 85, 160, 26.5, 4.6),    # Trent Boult
    (26,"ODI", 70, 120, 25.0, 4.2),    # Rashid Khan (Afghan, but as Pak series sim)

    # Australia Bowlers
    (23,"ODI", 90, 170, 28.0, 4.7),    # Cummins

    # West Indies Bowlers
    (28,"ODI", 100, 75, 35.0, 5.1),     # de Kock (added dummy bowling for query testing)

    (3, "ODI", 120, 85, 32.0, 5.5),    # Stokes
    (8, "ODI", 90, 70, 29.0, 5.6),     # Hardik
    (16,"ODI", 200, 210, 31.5, 4.8),   # Jadeja
    (22,"ODI", 300, 111, 38.0, 5.2),   # Yuvraj
    (10,"ODI", 70, 65, 30.0, 5.4),     # Curran
    (11,"ODI", 110, 110, 32.0, 5.3)    # Moeen Ali

    ])

# Simplified per-match stats

    player_match_batting = ([

    # Virat Kohli (2020–2025)
    (201, 1, 1, 1, 3, 75, 85, 88.2),  # 2020
    (202, 1, 1, 1, 3, 45, 60, 75.0),
    (203, 1, 1, 1, 3, 88, 92, 95.6),
    (204, 1, 1, 1, 3, 102, 110, 92.7),
    (205, 1, 1, 1, 3, 55, 70, 78.5),

    (206, 1, 1, 1, 3, 120, 125, 96.0), # 2021
    (207, 1, 1, 1, 3, 64, 70, 91.5),
    (208, 1, 1, 1, 3, 85, 95, 89.5),
    (209, 1, 1, 1, 3, 45, 50, 90.0),
    (210, 1, 1, 1, 3, 60, 65, 92.3),

    (211, 1, 1, 1, 3, 100, 110, 91.0), # 2022
    (212, 1, 1, 1, 3, 55, 58, 94.8),
    (213, 1, 1, 1, 3, 77, 85, 90.6),
    (214, 1, 1, 1, 3, 120, 130, 92.3),
    (215, 1, 1, 1, 3, 35, 45, 77.7),

    (216, 1, 1, 1, 3, 88, 95, 92.6), # 2023
    (217, 1, 1, 1, 3, 72, 80, 90.0),
    (218, 1, 1, 1, 3, 115, 120, 95.8),
    (219, 1, 1, 1, 3, 64, 70, 91.4),
    (220, 1, 1, 1, 3, 100, 105, 95.2),

    (221, 1, 1, 1, 3, 78, 85, 89.3), # 2024
    (222, 1, 1, 1, 3, 90, 95, 91.7),
    (223, 1, 1, 1, 3, 65, 70, 87.5),
    (224, 1, 1, 1, 3, 110, 120, 94.1),
    (225, 1, 1, 1, 3, 50, 60, 83.3),

    (226, 1, 1, 1, 3, 120, 125, 96.0), # 2025
    (227, 1, 1, 1, 3, 95, 100, 94.5),
    (228, 1, 1, 1, 3, 80, 85, 93.2),
    (229, 1, 1, 1, 3, 105, 110, 95.8),
    (230, 1, 1, 1, 3, 60, 65, 88.7),

    # Rohit Sharma (2020–2025)
    (231, 2, 1, 1, 3, 70, 80, 88.5),  # 2020
    (232, 2, 1, 1, 3, 55, 60, 91.7),
    (233, 2, 1, 1, 3, 102, 110, 92.7),
    (234, 2, 1, 1, 3, 78, 85, 91.7),
    (235, 2, 1, 1, 3, 80, 90, 88.8),

    (236, 2, 1, 1, 3, 65, 70, 92.8), # 2021
    (237, 2, 1, 1, 3, 55, 62, 88.7),
    (238, 2, 1, 1, 3, 102, 110, 92.7),
    (239, 2, 1, 1, 3, 78, 85, 91.7),
    (240, 2, 1, 1, 3, 80, 90, 88.8),

    # Babar Azam (2020–2025)
    (241, 25, 5, 1, 3, 85, 90, 94.4),   # 2020
    (242, 25, 5, 1, 3, 95, 100, 95.0),
    (243, 25, 5, 1, 3, 80, 85, 93.2),
    (244, 25, 5, 1, 3, 110, 115, 95.6),
    (245, 25, 5, 1, 3, 75, 80, 93.7),

    (246, 25, 5, 1, 3, 102, 110, 92.7),  # 2021
    (247, 25, 5, 1, 3, 80, 85, 94.1),
    (248, 25, 5, 1, 3, 95, 100, 95.0),
    (249, 25, 5, 1, 3, 120, 125, 96.0),
    (250, 25, 5, 1, 3, 70, 75, 90.7),

    (251, 25, 5, 1, 3, 88, 95, 92.6),    # 2022
    (252, 25, 5, 1, 3, 72, 80, 90.0),
    (253, 25, 5, 1, 3, 115, 120, 95.8),
    (254, 25, 5, 1, 3, 64, 70, 91.4),
    (255, 25, 5, 1, 3, 100, 105, 95.2),

    (256, 25, 5, 1, 3, 78, 85, 89.3),    # 2023
    (257, 25, 5, 1, 3, 90, 95, 91.7),
    (258, 25, 5, 1, 3, 65, 70, 87.5),
    (259, 25, 5, 1, 3, 110, 120, 94.1),
    (260, 25, 5, 1, 3, 50, 60, 83.3),

    (261, 25, 5, 1, 3, 120, 125, 96.0),  # 2024
    (262, 25, 5, 1, 3, 95, 100, 94.5),
    (263, 25, 5, 1, 3, 80, 85, 93.2),
    (264, 25, 5, 1, 3, 105, 110, 95.8),
    (265, 25, 5, 1, 3, 60, 65, 88.7),

    (266, 25, 5, 1, 3, 115, 120, 95.8),  # 2025
    (267, 25, 5, 1, 3, 90, 100, 90.0),
    (268, 25, 5, 1, 3, 130, 135, 96.3),
    (269, 25, 5, 1, 3, 65, 70, 92.8),
    (270, 25, 5, 1, 3, 85, 90, 94.4),

    # Steve Smith (2020–2025)
    (271, 24, 4, 1, 3, 45, 50, 90.0),   # 2020
    (272, 24, 4, 1, 3, 65, 70, 92.8),
    (273, 24, 4, 1, 3, 88, 95, 92.6),
    (274, 24, 4, 1, 3, 110, 120, 91.7),
    (275, 24, 4, 1, 3, 75, 80, 93.7),

    (276, 24, 4, 1, 3, 102, 110, 92.7), # 2021
    (277, 24, 4, 1, 3, 60, 70, 85.7),
    (278, 24, 4, 1, 3, 120, 130, 92.3),
    (279, 24, 4, 1, 3, 80, 85, 94.1),
    (280, 24, 4, 1, 3, 95, 100, 95.0),

    (281, 24, 4, 1, 3, 88, 92, 93.1),   # 2022
    (282, 24, 4, 1, 3, 100, 105, 94.3),
    (283, 24, 4, 1, 3, 70, 75, 90.2),
    (284, 24, 4, 1, 3, 110, 120, 95.0),
    (285, 24, 4, 1, 3, 60, 65, 87.5),

    (286, 24, 4, 1, 3, 105, 110, 94.0),  # 2023
    (287, 24, 4, 1, 3, 75, 80, 91.3),
    (288, 24, 4, 1, 3, 120, 125, 95.4),
    (289, 24, 4, 1, 3, 85, 90, 92.8),
    (290, 24, 4, 1, 3, 90, 95, 93.7),

    (291, 24, 4, 1, 3, 100, 105, 94.8),  # 2024
    (292, 24, 4, 1, 3, 65, 70, 91.5),
    (293, 24, 4, 1, 3, 120, 130, 92.3),
    (294, 24, 4, 1, 3, 80, 85, 94.1),
    (295, 24, 4, 1, 3, 95, 100, 95.0),

    (296, 24, 4, 1, 3, 88, 92, 93.0),   # 2025
    (297, 24, 4, 1, 3, 100, 105, 94.5),
    (298, 24, 4, 1, 3, 70, 75, 90.0),
    (299, 24, 4, 1, 3, 120, 125, 95.5),
    (300, 24, 4, 1, 3, 85, 90, 92.8),


    # (Series Top Scorers – India vs Eng 2024 series_id=8) ---
    (21, 1, 1, 1, 2, 85, 90, 94.4),   # Kohli
    (21, 2, 1, 1, 3, 70, 75, 93.3),   # Rohit
    (21, 5, 3, 2, 2, 95, 100, 95.0),  # Root
    (22, 1, 1, 1, 2, 45, 50, 90.0),
    (22, 2, 1, 1, 3, 30, 35, 85.7),
    (22, 5, 3, 2, 2, 120, 115, 104.3),
    (23, 1, 1, 1, 2, 100, 95, 105.3),
    (23, 2, 1, 1, 3, 65, 70, 92.8),
    (23, 5, 3, 2, 2, 40, 45, 88.9),

    # (Most Ducks) ---
    (301, 7, 1, 1, 5, 0, 2, 0.0),   # Pant duck
    (302, 7, 1, 1, 5, 0, 3, 0.0),
    (303, 7, 1, 1, 5, 0, 1, 0.0),
    (304, 19, 3, 1, 4, 0, 2, 0.0),  # Buttler duck
    (305, 19, 3, 1, 4, 0, 3, 0.0),

    # (Highest Strike Rate in a Match) ---
    (401, 30, 10, 1, 4, 70, 25, 280.0),   # Pooran explosive
    (401, 25, 5, 2, 2, 55, 40, 137.5),    # Babar slower
    (401, 15, 3, 1, 1, 45, 35, 128.6),

    # (Team Avg Runs per Match) ---
    (501, 1, 1, 1, 2, 60, 70, 85.7),   # India vs SL
    (501, 2, 1, 1, 3, 40, 50, 80.0),
    (501, 9, 2, 2, 2, 35, 45, 77.8),
    (502, 5, 5, 1, 2, 55, 65, 84.6),
    (502, 25, 5, 1, 3, 65, 70, 92.8),
    (502, 24, 4, 2, 2, 85, 95, 89.5),

    # (Top Run Scorers in 2024) ---
    (601, 1, 1, 1, 2, 88, 95, 92.6),
    (602, 2, 1, 1, 3, 75, 80, 93.8),
    (603, 25, 5, 1, 2, 95, 100, 95.0),
    (604, 30, 10, 1, 3, 65, 60, 108.3),
    (605, 24, 4, 1, 2, 105, 110, 95.5),
    (606, 5, 3, 1, 2, 115, 120, 95.8),

    ])

    player_match_bowling = ([
    # Jasprit Bumrah at Eden Gardens (venue_id = 1)
    (101, 4, 1, 10.0, 60, 40, 2, 4.0),
    (105, 4, 1, 10.0, 58, 35, 3, 3.5),
    (1,   4, 1, 10.0, 62, 45, 4, 4.5),

    # Jasprit Bumrah at Lords (venue_id = 2)
    (2,   4, 1, 12.0, 72, 55, 3, 4.6),
    (10,  4, 1, 12.0, 74, 50, 4, 4.2),
    (14,  4, 1, 12.0, 70, 48, 2, 4.0),

    # Rashid Khan at Sharjah (venue_id = 7)
    (3,   26, 6, 8.0, 48, 30, 2, 3.8),
    (7,   26, 6, 9.0, 54, 35, 3, 3.9),
    (17,  26, 6, 10.0, 60, 40, 4, 4.0),

    # Trent Boult at Pallekele (venue_id = 9)
    (4,   27, 8, 10.0, 60, 38, 3, 3.8),
    (11,  27, 8, 10.0, 62, 42, 2, 4.2),
    (16,  27, 8, 10.0, 61, 37, 4, 3.7),


    # Jasprit Bumrah (10 matches, low econ)
    (300, 4, 1, 10.0, 60, 45, 3, 4.5),
    (301, 4, 1, 8.0, 48, 40, 2, 5.0),
    (302, 4, 1, 9.0, 54, 38, 1, 4.2),
    (303, 4, 1, 10.0, 60, 42, 2, 4.2),
    (304, 4, 1, 7.0, 42, 30, 1, 4.3),
    (305, 4, 1, 8.0, 48, 36, 2, 4.5),
    (306, 4, 1, 9.0, 54, 35, 3, 3.9),
    (307, 4, 1, 10.0, 60, 40, 2, 4.0),
    (308, 4, 1, 6.0, 36, 28, 1, 4.7),
    (309, 4, 1, 8.0, 48, 30, 2, 3.8),

    # Rashid Khan (10 matches, very low econ)
    (310, 26, 6, 8.0, 48, 28, 2, 3.5),
    (311, 26, 6, 9.0, 54, 33, 3, 3.7),
    (312, 26, 6, 10.0, 60, 35, 2, 3.5),
    (313, 26, 6, 8.0, 48, 25, 1, 3.1),
    (314, 26, 6, 7.0, 42, 29, 2, 4.1),
    (315, 26, 6, 10.0, 60, 31, 3, 3.1),
    (316, 26, 6, 9.0, 54, 32, 2, 3.6),
    (317, 26, 6, 8.0, 48, 28, 1, 3.5),
    (318, 26, 6, 10.0, 60, 30, 3, 3.0),
    (319, 26, 6, 7.0, 42, 27, 2, 3.9),

    # Trent Boult (10 matches, mid econ)
    (320, 27, 8, 10.0, 60, 45, 2, 4.5),
    (321, 27, 8, 9.0, 54, 43, 2, 4.7),
    (322, 27, 8, 10.0, 60, 48, 3, 4.8),
    (323, 27, 8, 8.0, 48, 40, 1, 5.0),
    (324, 27, 8, 7.0, 42, 38, 2, 5.4),
    (325, 27, 8, 9.0, 54, 44, 2, 4.9),
    (326, 27, 8, 10.0, 60, 46, 3, 4.6),
    (327, 27, 8, 8.0, 48, 39, 2, 4.9),
    (328, 27, 8, 9.0, 54, 42, 1, 4.7),
    (329, 27, 8, 10.0, 60, 47, 2, 4.7),

    # Mark Wood (10 matches, high econ)
    (330, 14, 3, 8.0, 48, 50, 1, 6.2),
    (331, 14, 3, 9.0, 54, 60, 2, 6.7),
    (332, 14, 3, 10.0, 60, 62, 1, 6.2),
    (333, 14, 3, 7.0, 42, 45, 2, 6.4),
    (334, 14, 3, 9.0, 54, 58, 1, 6.5),
    (335, 14, 3, 8.0, 48, 55, 2, 6.9),
    (336, 14, 3, 10.0, 60, 63, 2, 6.3),
    (337, 14, 3, 9.0, 54, 59, 1, 6.5),
    (338, 14, 3, 8.0, 48, 52, 2, 6.5),
    (339, 14, 3, 7.0, 42, 49, 1, 7.0)
    ])

    partnerships = [

    # Kohli & Rohit (≥ 5 partnerships)
    (901, 1, 2, 3, 1, 2, 65),
    (902, 1, 2, 3, 1, 2, 120),
    (903, 1, 2, 3, 1, 2, 45),
    (904, 1, 2, 3, 1, 2, 78),
    (905, 1, 2, 3, 1, 2, 52),
    (906, 1, 2, 3, 1, 2, 90),

    # Root & Stokes (≥ 5 partnerships)
    (907, 1, 3, 4, 5, 3, 30),
    (908, 1, 3, 4, 5, 3, 150),
    (909, 1, 3, 4, 5, 3, 85),
    (910, 1, 3, 4, 5, 3, 65),
    (911, 1, 3, 4, 5, 3, 25),
    (912, 1, 3, 4, 5, 3, 110)
    ]


    fielding = [
    (1,"ODI",100,0),
    (2,"ODI",80,0),
    (6,"ODI",120,5),    # KL Rahul
    (7,"ODI",25,10),    # Pant
    (15,"ODI",180,10),  # Bairstow
    (21,"ODI",321,38),  # Dhoni
    (19,"ODI",200,25),  # Buttler
    (28,"ODI",210,30),  # de Kock
    (30,"ODI",90,5)     # Pooran
    ]
    cur.executemany("INSERT INTO players (player_id,full_name,country,role,batting_style,bowling_style) VALUES (?,?,?,?,?,?)", players)
    cur.executemany("INSERT INTO teams (team_id,team_name,country) VALUES (?,?,?)", teams)
    cur.executemany("INSERT INTO venues (venue_id,name,city,country,capacity) VALUES (?,?,?,?,?)", venues)
    cur.executemany("INSERT INTO series (series_id,name,host_country,match_type,start_date,total_matches) VALUES (?,?,?,?,?,?)", series)
    cur.executemany("INSERT INTO matches (match_id,description,format,series_id,team1_id,team2_id,venue_id,match_date,winner_team_id, toss_winner_team_id, toss_decision,result_margin,result_type) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", matches)
    cur.executemany("INSERT INTO batting_stats (player_id,format,matches_played,runs,average,strike_rate,centuries,half_centuries) VALUES (?,?,?,?,?,?,?,?)", batting_stats)
    cur.executemany("INSERT INTO bowling_stats (player_id,format,matches_played,wickets,bowling_average,economy) VALUES (?,?,?,?,?,?)", bowling_stats)
    cur.executemany("INSERT INTO player_match_batting (match_id,player_id,team_id,innings_no,position,runs,balls_faced,strike_rate) VALUES (?,?,?,?,?,?,?,?)", player_match_batting)
    cur.executemany("INSERT INTO player_match_bowling (match_id,player_id,team_id,overs,balls_bowled,runs_conceded,wickets,economy) VALUES (?,?,?,?,?,?,?,?)", player_match_bowling)
    cur.executemany("INSERT INTO partnerships (match_id,innings_no,pos1,pos2,player1_id,player2_id,runs) VALUES (?,?,?,?,?,?,?)", partnerships)
    cur.executemany("INSERT INTO player_fielding (player_id,format,catches,stumpings) VALUES (?,?,?,?)", fielding)
    
    conn.commit()



# ---------------------- 25 SQL QUERIES ----------------------
# db.py — Correct list-of-dicts for your 25 analytics queries
Query_List = [
    {
        "title": "Q1 • All players from India",
        "sql": """
            SELECT full_name, role, batting_style, bowling_style
            FROM players
            WHERE country = 'India';
        """
    },
    {
        "title": "Q2 • Matches in last 30 days",
        "sql": """
            SELECT m.description, t1.team_name AS team1, t2.team_name AS team2, v.name AS venue, v.city, m.match_date
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            JOIN venues v ON v.venue_id = m.venue_id
            WHERE DATE(m.match_date) >= DATE('now','-30 day')
            ORDER BY DATE(m.match_date) DESC;
        """
    },
    {
        "title": "Q3 • Top 10 ODI run scorers",
        "sql": """
            SELECT p.full_name,
                   SUM(b.runs) AS total_runs,
                   ROUND(AVG(b.average),2) AS batting_avg,
                   SUM(b.centuries) AS centuries
            FROM batting_stats b
            JOIN players p ON b.player_id = p.player_id
            WHERE b.format = 'ODI'
            GROUP BY p.player_id
            ORDER BY total_runs DESC
            LIMIT 10;
        """
    },
    {
        "title": "Q4 • Venues with capacity > 50,000",
        "sql": """
            SELECT name, city, country, capacity
            FROM venues
            WHERE capacity > 50000
            ORDER BY capacity DESC;
        """
    },
    {
        "title": "Q5 • Matches each team has won",
        "sql": """
            SELECT t.team_name, COUNT(*) AS total_wins
            FROM matches m
            JOIN teams t ON t.team_id = m.winner_team_id
            GROUP BY t.team_id
            ORDER BY total_wins DESC;
        """
    },
    {
        "title": "Q6 • Player count by role",
        "sql": """
            SELECT role, COUNT(*) AS player_count
            FROM players
            GROUP BY role
            ORDER BY player_count DESC;
        """
    },
    {
        "title": "Q7 • Highest individual batting score per format",
        "sql": """
            SELECT m.format, MAX(pmb.runs) AS highest_score
            FROM player_match_batting pmb
            JOIN matches m ON m.match_id = pmb.match_id
            GROUP BY m.format;
        """
    },
    {
        "title": "Q8 • Series started in 2024",
        "sql": """
            SELECT name, host_country, match_type, start_date, total_matches
            FROM series
            WHERE strftime('%Y', start_date) = '2024';
        """
    },
    {
        "title": "Q9 • All-rounders: >1000 runs AND >50 wickets",
        "sql": """
            SELECT p.full_name, b.format,
                   SUM(b.runs) AS total_runs,
                   SUM(w.wickets) AS total_wickets
            FROM players p
            JOIN batting_stats b ON p.player_id = b.player_id
            JOIN bowling_stats w ON p.player_id = w.player_id AND b.format = w.format
            WHERE p.role LIKE '%All%'
            GROUP BY p.player_id, b.format
            HAVING total_runs > 1000 AND total_wickets > 50;
        """
    },
    {
        "title": "Q10 • Last 20 completed matches (with result details)",
        "sql": """
            SELECT m.description,
                   t1.team_name AS team1,
                   t2.team_name AS team2,
                   tw.team_name AS winner,
                   m.result_margin,
                   m.result_type,
                   v.name AS venue,
                   m.match_date
            FROM matches m
            JOIN teams t1 ON t1.team_id = m.team1_id
            JOIN teams t2 ON t2.team_id = m.team2_id
            LEFT JOIN teams tw ON tw.team_id = m.winner_team_id
            JOIN venues v ON v.venue_id = m.venue_id
            WHERE m.result_type IS NOT NULL
            ORDER BY DATE(m.match_date) DESC
            LIMIT 20;
        """
    },
    {
        "title": "Q11 • Players with ≥2 formats: Test/ODI/T20I runs + overall avg",
        "sql": """
            SELECT
                p.full_name,
                SUM(CASE WHEN b.format='Test' THEN b.runs ELSE 0 END) AS test_runs,
                SUM(CASE WHEN b.format='ODI'  THEN b.runs ELSE 0 END) AS odi_runs,
                SUM(CASE WHEN b.format='T20I' THEN b.runs ELSE 0 END) AS t20i_runs,
                ROUND(AVG(b.average),2) AS overall_avg
            FROM players p
            JOIN batting_stats b ON b.player_id = p.player_id
            GROUP BY p.player_id
            HAVING
                ((SUM(CASE WHEN b.format='Test' THEN b.runs ELSE 0 END) > 0) +
                 (SUM(CASE WHEN b.format='ODI'  THEN b.runs ELSE 0 END) > 0) +
                 (SUM(CASE WHEN b.format='T20I' THEN b.runs ELSE 0 END) > 0)) >= 2;
        """
    },
    {
        "title": "Q12 • Team wins at Home vs Away",
        "sql": """
            SELECT
                t.team_name,
                CASE WHEN t.country = v.country THEN 'Home' ELSE 'Away' END AS location,
                COUNT(*) AS matches,
                SUM(CASE WHEN m.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS wins
            FROM matches m
            JOIN teams t ON t.team_id IN (m.team1_id, m.team2_id)
            JOIN venues v ON v.venue_id = m.venue_id
            GROUP BY t.team_name, location;
        """
    },
    {
        "title": "Q13 • Partnerships ≥ 100 by consecutive batsmen",
        "sql": """
            SELECT p1.full_name AS player1,
                   p2.full_name AS player2,
                   pr.runs,
                   pr.innings_no
            FROM partnerships pr
            JOIN players p1 ON pr.player1_id = p1.player_id
            JOIN players p2 ON pr.player2_id = p2.player_id
            WHERE ABS(pr.pos2 - pr.pos1) = 1
              AND pr.runs >= 100;
        """
    },
    {
        "title": "Q14 • Bowling at venues (≥3 matches, ≥4 overs each)",
        "sql": """
            SELECT p.full_name,
                   v.name AS venue,
                   COUNT(*) AS matches,
                   ROUND(AVG(b.economy),2) AS avg_economy,
                   SUM(b.wickets) AS total_wickets
            FROM player_match_bowling b
            JOIN players p ON b.player_id = p.player_id
            JOIN matches m ON m.match_id = b.match_id
            JOIN venues v ON v.venue_id = m.venue_id
            WHERE b.overs >= 4
            GROUP BY p.full_name, v.name
            HAVING COUNT(*) >= 3;
        """
    },
    {
        "title": "Q15 • Player batting in close matches",
        "sql": """
            SELECT p.full_name,
                   ROUND(AVG(pmb.runs),2) AS avg_runs_close,
                   COUNT(*) AS close_matches
            FROM player_match_batting pmb
            JOIN matches m ON m.match_id = pmb.match_id
            JOIN players p ON p.player_id = pmb.player_id
            WHERE (m.result_type = 'runs' AND m.result_margin < 50)
               OR (m.result_type = 'wickets' AND m.result_margin < 5)
            GROUP BY p.player_id;
        """
    },
    {
        "title": "Q16 • Player performance by year since 2020",
        "sql": """
            SELECT p.full_name,
                   strftime('%Y', m.match_date) AS year,
                   ROUND(AVG(pmb.runs),2) AS avg_runs,
                   ROUND(AVG(pmb.strike_rate),2) AS avg_sr,
                   COUNT(*) AS matches
            FROM player_match_batting pmb
            JOIN players p ON p.player_id = pmb.player_id
            JOIN matches m ON m.match_id = pmb.match_id
            WHERE DATE(m.match_date) >= '2020-01-01'
            GROUP BY p.player_id, year
            HAVING COUNT(*) >= 5;
        """
    },
    {
        "title": "Q17 • Toss advantage by decision",
        "sql": """
            SELECT toss_decision,
                   COUNT(*) AS total,
                   SUM(CASE WHEN toss_winner_team_id = winner_team_id THEN 1 ELSE 0 END) AS wins,
                   ROUND(
                     100.0 * SUM(CASE WHEN toss_winner_team_id = winner_team_id THEN 1 ELSE 0 END) / COUNT(*),
                     2
                   ) AS win_pct
            FROM matches
            WHERE toss_decision IN ('bat','bowl')
            GROUP BY toss_decision;
        """
    },
    {
        "title": "Q18 • Economical bowlers in ODI/T20I (≥10 matches, avg ≥2 overs)",
        "sql": """
            SELECT p.full_name,
                   m.format,
                   ROUND(SUM(b.runs_conceded) * 1.0 / SUM(b.overs), 2) AS economy,
                   SUM(b.wickets) AS wickets,
                   COUNT(DISTINCT m.match_id) AS matches
            FROM player_match_bowling b
            JOIN matches m ON m.match_id = b.match_id
            JOIN players p ON p.player_id = b.player_id
            WHERE m.format IN ('ODI','T20I')
            GROUP BY p.player_id, m.format
            HAVING matches >= 10
               AND (SUM(b.overs) * 1.0 / matches) >= 2;
        """
    },
    {
        "title": "Q19 • Consistent scorers since 2022",
        "sql": """
            SELECT p.full_name,
                   ROUND(AVG(pmb.runs),2) AS avg_runs,
                   ROUND(AVG(pmb.runs * pmb.runs) - AVG(pmb.runs) * AVG(pmb.runs), 2) AS variance
            FROM player_match_batting pmb
            JOIN matches m ON m.match_id = pmb.match_id
            JOIN players p ON p.player_id = pmb.player_id
            WHERE DATE(m.match_date) >= '2022-01-01'
              AND pmb.balls_faced >= 10
            GROUP BY p.player_id;
        """
    },
    {
        "title": "Q20 • Matches per format + batting avg per format (≥20 total)",
        "sql": """
            SELECT p.full_name,
                   SUM(CASE WHEN b.format='Test' THEN b.matches_played ELSE 0 END) AS test_matches,
                   ROUND(AVG(CASE WHEN b.format='Test' THEN b.average END),2) AS test_avg,
                   SUM(CASE WHEN b.format='ODI'  THEN b.matches_played ELSE 0 END) AS odi_matches,
                   ROUND(AVG(CASE WHEN b.format='ODI'  THEN b.average END),2) AS odi_avg,
                   SUM(CASE WHEN b.format='T20I' THEN b.matches_played ELSE 0 END) AS t20_matches,
                   ROUND(AVG(CASE WHEN b.format='T20I' THEN b.average END),2) AS t20_avg,
                   SUM(b.matches_played) AS total_matches
            FROM batting_stats b
            JOIN players p ON p.player_id = b.player_id
            GROUP BY p.player_id
            HAVING total_matches >= 20;
        """
    },
    {
        "title": "Q21 • Composite performance score (bat/bowl/field)",
        "sql": """
            SELECT p.full_name, b.format,
                   ROUND((b.runs * 0.01) + (b.average * 0.5) + (b.strike_rate * 0.3), 2) AS batting_pts,
                   ROUND((w.wickets * 2) + ((50 - w.bowling_average) * 0.5) + ((6 - w.economy) * 2), 2) AS bowling_pts,
                   (f.catches + f.stumpings) AS fielding_pts
            FROM players p
            LEFT JOIN batting_stats  b ON p.player_id = b.player_id
            LEFT JOIN bowling_stats  w ON p.player_id = w.player_id AND b.format = w.format
            LEFT JOIN player_fielding f ON p.player_id = f.player_id AND f.format = b.format;
        """
    },
    {
        "title": "Q22 • Head-to-head (last 3 years, ≥5 matches)",
        "sql": """
            SELECT t1.team_name AS team_a,
                   t2.team_name AS team_b,
                   COUNT(*) AS matches,
                   SUM(CASE WHEN m.winner_team_id = t1.team_id THEN 1 ELSE 0 END) AS wins_a,
                   SUM(CASE WHEN m.winner_team_id = t2.team_id THEN 1 ELSE 0 END) AS wins_b
            FROM matches m
            JOIN teams t1 ON t1.team_id = m.team1_id
            JOIN teams t2 ON t2.team_id = m.team2_id
            WHERE DATE(m.match_date) >= DATE('now','-3 years')
            GROUP BY t1.team_id, t2.team_id
            HAVING matches >= 5;
        """
    },
    {
        "title": "Q23 • Recent form: last 10 innings",
        "sql": """
            WITH last10 AS (
              SELECT
                pmb.player_id,
                pmb.runs,
                ROW_NUMBER() OVER (PARTITION BY pmb.player_id ORDER BY m.match_date DESC) AS rn
              FROM player_match_batting pmb
              JOIN matches m ON m.match_id = pmb.match_id
            )
            SELECT p.full_name,
                   AVG(CASE WHEN rn <= 5  THEN runs END) AS avg_last5,
                   AVG(CASE WHEN rn <= 10 THEN runs END) AS avg_last10,
                   SUM(CASE WHEN rn <= 10 AND runs >= 50 THEN 1 ELSE 0 END) AS fifties
            FROM last10 l
            JOIN players p ON p.player_id = l.player_id
            WHERE rn <= 10
            GROUP BY p.player_id;
        """
    },
    {
        "title": "Q24 • Best batting partnerships (≥5 together)",
        "sql": """
            SELECT p1.full_name AS player1,
                   p2.full_name AS player2,
                   COUNT(*) AS inns,
                   ROUND(AVG(pr.runs),2) AS avg_runs,
                   SUM(CASE WHEN pr.runs > 50 THEN 1 ELSE 0 END) AS over50,
                   MAX(pr.runs) AS highest
            FROM partnerships pr
            JOIN players p1 ON pr.player1_id = p1.player_id
            JOIN players p2 ON pr.player2_id = p2.player_id
            GROUP BY p1.full_name, p2.full_name
            HAVING COUNT(*) >= 5;
        """
    },
    {
        "title": "Q25 • Quarterly batting performance",
        "sql": """
            SELECT
              p.full_name,
              strftime('%Y', m.match_date) || '-Q' || ((CAST(strftime('%m', m.match_date) AS INT)-1)/3 + 1) AS quarter,
              ROUND(AVG(pmb.runs),2) AS avg_runs,
              ROUND(AVG(pmb.strike_rate),2) AS avg_sr
            FROM player_match_batting pmb
            JOIN matches m ON m.match_id = pmb.match_id
            JOIN players p ON p.player_id = pmb.player_id
            GROUP BY p.player_id, quarter
            HAVING COUNT(*) >= 5;
        """
    }
]


