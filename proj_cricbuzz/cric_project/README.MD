CRICBUZZ PROJECT:

-> PROJECT DESCRIPTION:

    CRICBUZZ is a comprehensive, data-driven platform that provides in-depth insights into cricket players, teams, and match performances. The project leverages historical and live cricket data, collected via APIs and stored in a relational SQLite database, to allow users to analyze, compare, and visualize cricket statistics across multiple formats (ODI, T20I, and Test) and time periods.

    This project is designed for cricket enthusiasts, analysts, and coaches who want to track player performance, understand team dynamics, and make data-driven decisions.

-> Key Features and Objectives:

     1.Player Performance Tracking :

         Tracks batting and bowling performances of individual players across multiple years.

         Computes metrics such as average runs, strike rate, wickets, and economy rate.


    2.Team and Match Analytics :

         Compares team performances in different series, formats, and venues.

         Aggregates data for total runs scored, wickets taken, partnerships, and team averages per match.

         Provides insights into how team composition and player contributions influence match outcomes.

    3.Top Performer Identification :

         Generates rankings of most economical bowlers, highest run-scorers, and players with top strike rates.

         Identifies players with consistent performances over multiple years and matches.


     4.Data Aggregation from API & Database

         Integrates live cricket data from APIs (e.g., Cricbuzz) into the SQLite database.

         Stores match, player, team, venue, and series information in structured tables for efficient querying.

         Enables real-time updates and analytics without manual data entry.

     5.Interactive Dashboard

         Built using Streamlit, offering an intuitive user interface.

         Users can filter data by player, team, match format, year, or series.

         Display tables to visualize performance metrics clearly.

     6. Pages:

         Live Matches – Shows ongoing match details.
         Player Stats – Year-wise batting and bowling performance.
         Rankings – Top batsmen, bowlers, and fielders based on metrics.
         Analytics & Insights
         CRUD OPERATION -Add,Update,Delete

-> Tools & Technologies Used:

    1.Python – Core language for data processing and logic.

    2.SQLite – Relational database to store structured cricket data.

    3.Streamlit – Web framework to create an interactive dashboard.

    4.Pandas & NumPy – Data manipulation and analysis.

    5.API Integration – Fetching live and historical cricket data (Cricbuzz).

-> Workflow & Navigation

    1.Data Collection: Fetch live and historical match data using APIs and store in the SQLite database.

    2.Data Processing: Clean, transform, and aggregate data using Python & pandas.

    3.Visualization: Create tables and charts for player stats, team analysis, and rankings.

    4.Dashboard Navigation:

        * Live Matches Page: Displays ongoing matches.

        * Player Stats Page: Shows individual year-wise performance metrics.

        * Team Analysis Page: Provides match-level and series-level team analytics.

        * Rankings Page: Lists top performers in batting, bowling, and fielding.

        * CRUD Operation : For adding the players, Update their information and for deletion of players.

-> Project Structure :

cric_project
│
├── cric_api.py             # Fetch data from APIs (Cricbuzz)
├── db.py             # SQLite database initialization
├── app.py                  # Streamlit main dashboard file
├── requirements.txt        # Python dependencies
└── README.md               # Project overview and instructions


-> Google Collab link
     
     : For SQL Database
            https://colab.research.google.com/drive/1yO1XpLhGOsDelCnzwCdySgMb7_03OZd7#scrollTo=tgMcHXJkiTN5

     : For Data Collection from CRICBUZZ/RAPID
            https://colab.research.google.com/drive/1nRzkUJlqL3-6w6lpnnEnB7swHBG_4j3I#scrollTo=guIe-7pJXnMY

