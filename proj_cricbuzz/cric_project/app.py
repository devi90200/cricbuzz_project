import streamlit as st
import pandas as pd
import requests
from db import get_conn, get_engine, Query_List
from sqlalchemy import create_engine, text
from sqlalchemy import text
from cric_api import get_live_matches, fetch_cricbuzz_rankings, get_live_scorecard, search_player,get_player_info
# --------------------------
# Initialize DB
# --------------------------

conn = get_conn()
engine = get_engine()

DB_NAME = "cricbuzz_db"
DB_USER = "postgres"
DB_PASSWORD = "DEVI"
DB_HOST = "localhost"
DB_PORT = "5432"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


# --------------------------
# Streamlit Setup
# --------------------------
st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")
st.title("🏏 Cricbuzz LiveStats Dashboard")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Go to",
        [
            "Home",
            "Live Matches",
            "Search Player",
            "Top Player Stats",
            "SQL Analytics",
            "CRUD Operations",
        ],
    )

# --------------------------
# Home Page
# --------------------------
if page == "Home":
    st.header("🏠 Cricbuzz LiveStats Home")
    st.subheader("📌 Quick Overview")

    # Documentation and Folder Structure Link
    st.markdown(
        """
        ### 📄 Project Documentation
        https://docs.google.com/document/d/1LpjVvTTespcAdsF9gWe2KGQORHTBoBh95MH4hpVGvus/edit?tab=t.0

        ### 🗂 Folder Structure
        ```
        cric_project
          │
          ├── cric_api.py             # Fetch data from APIs (Cricbuzz)
          ├── db.py                   # SQLite database initialization
          ├── app.py                  # Streamlit main dashboard file
          ├── populate_players.py     # Fetch and populate playersList table   
          ├── data.ipynb              # data collected through APIs and connected to PostgreSQL                          
          ├── requirements.txt        # Python dependencies
          └── README.md               # Project overview and instructions

        ```
        """
    )


    try:
        # Fetch data
        matches = get_live_matches()  # list
        rankings = fetch_cricbuzz_rankings()  # list of dicts

        # Quick metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("🔴 Live Matches", len(matches))
        col2.metric("🏏 Total Batsmen Ranked", len([r for r in rankings if "Batsmen" in r.get("Category", "")]))
        col3.metric("🎯 Total Bowlers Ranked", len([r for r in rankings if "Bowlers" in r.get("Category", "")]))

        # Live matches table
        if matches:
            st.subheader("🔴 Live Matches Table")
            df_matches = pd.DataFrame(matches)
            if not df_matches.empty:
                st.dataframe(df_matches, width="stretch")
            else:
                st.info("No live matches currently.")
        else:
            st.info("No live matches currently.")

        # Top 5 ODI Batsmen
        top_batsmen = [
            r for r in rankings if r.get("Category") == "Batsmen_ODI"
        ][:5]
        if top_batsmen:
            st.subheader("📊 Top 5 ODI Batsmen")
            for player in top_batsmen:
                st.markdown(
                    f"""
                    <div style="display:flex; align-items:center; gap:15px; padding:10px; margin:8px 0;
                                border-radius:12px; background:#fdfdfd; box-shadow:0 2px 6px rgba(0,0,0,0.1)">
                        {"<img src='"+player.get('Image','')+"' width='60' height='60' style='border-radius:50%'>" if player.get('Image') else ""}
                        <div>
                            <h4 style="margin:0">#{player.get('Rank')} - {player.get('Player')}</h4>
                            <p style="margin:0"><b>Team:</b> {player.get('Team')}</p>
                            <p style="margin:0"><b>Rating:</b> {player.get('Rating')}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Top 5 ODI Bowlers
        top_bowlers = [
            r for r in rankings if r.get("Category") == "Bowlers_ODI"
        ][:5]
        if top_bowlers:
            st.subheader("📊 Top 5 ODI Bowlers")
            for player in top_bowlers:
                st.markdown(
                    f"""
                    <div style="display:flex; align-items:center; gap:15px; padding:10px; margin:8px 0;
                                border-radius:12px; background:#fdfdfd; box-shadow:0 2px 6px rgba(0,0,0,0.1)">
                        {"<img src='"+player.get('Image','')+"' width='60' height='60' style='border-radius:50%'>" if player.get('Image') else ""}
                        <div>
                            <h4 style="margin:0">#{player.get('Rank')} - {player.get('Player')}</h4>
                            <p style="margin:0"><b>Team:</b> {player.get('Team')}</p>
                            <p style="margin:0"><b>Rating:</b> {player.get('Rating')}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f"Error loading home stats: {e}")

# --------------------------
# Live Matches Page
# --------------------------
elif page == "Live Matches":
    st.header("🔴 Live Matches - Interactive Dashboard")

    try:
        matches = get_live_matches()

        if not matches:
            st.warning("No live matches currently.")
        else:
            st.subheader("📌 Ongoing Matches")

            for match in matches:
                # Extract basic info
                series = match.get("Series", "N/A")
                venue = match.get("Venue", "N/A")
                status = match.get("Status", "N/A")
                match_name = match.get("Match", "Team 1 vs Team 2")

                # Color coding based on status
                if "live" in status.lower():
                    bg_color = "#d4edda"  # green
                    status_icon = "🟢"
                elif "in progress" in status.lower():
                    bg_color = "#fff3cd"  # yellow
                    status_icon = "🟡"
                else:
                    bg_color = "#f8d7da"  # red/gray
                    status_icon = "🔴"

                # Display match info card
                st.markdown(
                    f"""
                    <div style="padding:15px; margin:10px 0; border-radius:12px;
                                background:{bg_color}; box-shadow:0 2px 6px rgba(0,0,0,0.15)">
                        <h3 style="margin:0">{match_name} {status_icon}</h3>
                        <p style="margin:2px 0"><b>Series:</b> {series}</p>
                        <p style="margin:2px 0"><b>Venue:</b> {venue}</p>
                        <p style="margin:2px 0"><b>Status:</b> {status}</p>
                    """,
                    unsafe_allow_html=True
                )

                # Show innings info if present
                innings_list = match.get("innings", [])
                if innings_list:
                    for inn in innings_list:
                        team_name = inn.get("teamName", "N/A")
                        runs = inn.get("runs", "0")
                        wickets = inn.get("wickets", "0")
                        overs = inn.get("overs", "0.0")
                        strike_rate = inn.get("strikeRate", "N/A")
                        st.markdown(
                            f"""
                            <div style="padding:10px; margin:8px 0; border-radius:10px; background:#e9ecef;">
                                <h4 style="margin:0">{team_name} Innings</h4>
                                <p style="margin:2px 0"><b>Score:</b> {runs}/{wickets} in {overs} overs</p>
                                <p style="margin:2px 0"><b>Strike Rate:</b> {strike_rate}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error fetching live matches: {e}")
# Ranking Page
# --------------------------
elif page == "Top Player Stats":
    st.header("🏏 Player Rankings")

    try:
        rankings = fetch_cricbuzz_rankings()
        if rankings:
            df_rankings = pd.DataFrame(rankings)

            format_choice = st.radio("📄 Select Format", ["ODI", "T20", "Test"], horizontal=True)
            category_choice = st.radio("📊 Select Category", ["Batsmen", "Bowlers", "Allrounders", "Teams"], horizontal=True)

            selected_category = f"{category_choice}_{format_choice}"
            filtered_df = df_rankings[df_rankings["Category"] == selected_category]

            if not filtered_df.empty:
                st.subheader(f"🏆 Top 10 {category_choice} - {format_choice}")
                for _, row in filtered_df.head(10).iterrows():
                    if category_choice != "Teams":
                        st.markdown(
                            f"""
                            <div style="display:flex; align-items:center; gap:15px; padding:10px; margin:8px 0;
                                        border-radius:12px; background:#fdfdfd; box-shadow:0 2px 6px rgba(0,0,0,0.1)">
                                {"<img src='"+row.get('Image','')+"' width='60' height='60' style='border-radius:50%'>" if row.get('Image') else ""}
                                <div>
                                    <h4 style="margin:0">#{row.get('Rank')} - {row.get('Player')}</h4>
                                    <p style="margin:0"><b>Team:</b> {row.get('Team')}</p>
                                    <p style="margin:0"><b>Rating:</b> {row.get('Rating')}</p>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="padding:10px; margin:8px 0; border-radius:12px;
                                        background:#e8f5e9; box-shadow:0 2px 6px rgba(0,0,0,0.1)">
                                <h4 style="margin:0">#{row.get('Rank')} - {row.get('Player')}</h4>
                                <p style="margin:0"><b>Rating:</b> {row.get('Rating')}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
            else:
                st.info("No rankings data available for selected category/format.")
        else:
            st.info("No rankings data available.")
    except Exception as e:
        st.error(f"Error loading rankings: {e}")


# --------------------------
# Search Player Page
# --------------------------
elif page == "Search Player":
    
    st.title("🏏 Cricbuzz Player Search")

    search_term = st.text_input("🔍 Enter Player Name:")

    if st.button("Search") and search_term.strip():
        players = search_player(search_term)

        if not players:
            st.warning("No players found. Try another name.")
        else:
            for player in players:
                player_id = player.get("id")
                name = player.get("name")
                team = player.get("teamName", "N/A")
                dob = player.get("dob", "N/A")

                st.markdown(f"## 👤 {name} ({team})")
                st.write(f"**Date of Birth:** {dob}")
                st.write(f"**player_id:** {player_id}")

                # View Profile button
                st.markdown(
                    f"""
                    <a href="https://www.cricbuzz.com/profiles/{player_id}/{name.replace(' ', '-').lower()}"
                       target="_blank" style="text-decoration:none;">
                        <button style="background-color:#008CBA;color:white;border:none;
                                       padding:10px 16px;border-radius:8px;cursor:pointer;margin-top:10px;">
                            🌐 View Full Profile
                        </button>
                    </a>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("---")
    else:
        st.info("👆 Enter a player name and press **Search** to view results.")



# ---------- TOP PLAYER STATS ----------
elif page == "Top Player Stats":
    st.header("🏆 Top Player Stats")
    st.info("Coming soon! Integrate your ranking API here.")


# --------------------------
# SQL Analytics Page
# --------------------------
elif page == "SQL Analytics":
    st.subheader("📊 SQL Analytics — 25 Queries")
    names = [f"Q{i+1:02d}. {d['title']}" for i, d in enumerate(Query_List)]
    idx = st.selectbox("Pick a query", list(range(len(names))), format_func=lambda i: names[i])
    st.markdown(f"**{Query_List[idx]['title']}**")
    with st.expander("View SQL"):
        st.code(Query_List[idx]["sql"], language="sql")
    if st.button("Run Query"):
        try:
            df = pd.read_sql_query(Query_List[idx]["sql"], conn)
            if not df.empty:
                st.dataframe(df, width="stretch")
            else:
                st.info("No rows returned.")
        except Exception as e:
            st.error(f"Query failed: {e}")

# --------------------------
# CRUD Operations Page
# --------------------------
elif page == "CRUD Operations":
    st.subheader("🛠 Player Management (Local DB)")

    # Tabs for each CRUD operation
    tab_add, tab_view, tab_update, tab_delete, tab_search = st.tabs(
        ["➕ Add", "📋 View", "✏️ Update", "🗑️ Delete", "🔍 Search"]
    )

    # --------------------------
    # ➕ ADD PLAYER
    # --------------------------
    with tab_add:
        st.header("Add New Player")
        with st.form("add_player_form"):
            name = st.text_input("Full Name")
            player_id = st.text_input("Player ID (optional)")
            role = st.selectbox(
                "Role", ["Batsman", "Bowler", "Allrounder", "Wicket-keeper", "Unknown"]
            )
            batting = st.text_input(
                "Batting Style", placeholder="Right-hand bat / Left-hand bat"
            )
            bowling = st.text_input(
                "Bowling Style", placeholder="Right-arm offbreak / Left-arm fast"
            )
            submitted = st.form_submit_button("Add Player")

            if submitted:
                if name.strip():
                    try:
                        # Auto-generate ID if empty
                        if not player_id.strip():
                            df_ids = pd.read_sql("SELECT id FROM playerslist", engine)
                            if df_ids.empty:
                                player_id = "1"  # start from 1 if table is empty
                            else:
                                player_id = str(df_ids["id"].astype(int).max() + 1)

                        with engine.begin() as conn:
                            conn.execute(
                                text(
                                    """
                                    INSERT INTO playerslist (id, name, role, batting_style, bowling_style)
                                    VALUES (:pid, :name, :role, :bat, :bowl)
                                    ON CONFLICT (id) DO NOTHING
                                    """
                                ),
                                {
                                    "pid": player_id,
                                    "name": name,
                                    "role": role,
                                    "bat": batting,
                                    "bowl": bowling,
                                },
                            )
                        st.success(f"✅ Player '{name}' added successfully! (ID: {player_id})")
                    except Exception as e:
                        st.error(f"Insert failed: {e}")
                else:
                    st.warning("⚠️ Please enter a player name.")

    # --------------------------
    # 📋 VIEW PLAYERS
    # --------------------------
    with tab_view:
        st.write("📋 Current Players")
        df = pd.read_sql(
            "SELECT id, name FROM playerslist ORDER BY name ASC",
            engine
        )
        if not df.empty:
            st.dataframe(df, width='stretch')
        else:
            st.info("No players available.")

    # --------------------------
    # ✏️ UPDATE PLAYER
    # --------------------------
    with tab_update:
        st.header("Update Player Details")
        df = pd.read_sql(
            "SELECT id, name, role, batting_style, bowling_style FROM playerslist ORDER BY name",
            engine
        )
        if not df.empty:
            pid_options = df["id"].tolist()

            def safe_format(x):
                row = df[df["id"] == x]
                return row["name"].values[0] if not row.empty else str(x)

            pid = st.selectbox("Select Player", pid_options, format_func=safe_format)
            new_role = st.text_input("New Role")
            new_bat = st.text_input("New Batting Style")
            new_bowl = st.text_input("New Bowling Style")

            if st.button("Update Player"):
                fields = []
                params = {"pid": pid}
                if new_role.strip():
                    fields.append("role = :role")
                    params["role"] = new_role
                if new_bat.strip():
                    fields.append("batting_style = :bat")
                    params["bat"] = new_bat
                if new_bowl.strip():
                    fields.append("bowling_style = :bowl")
                    params["bowl"] = new_bowl

                if fields:
                    sql = f"UPDATE playerslist SET {', '.join(fields)} WHERE id = :pid"
                    with engine.begin() as conn:
                        conn.execute(text(sql), params)
                    st.success("✅ Player updated successfully.")
                else:
                    st.info("Nothing to update.")
        else:
            st.info("No players available to update.")

    # --------------------------
    # 🗑️ DELETE PLAYER
    # --------------------------
    with tab_delete:
        st.header("Delete Player")
        df = pd.read_sql("SELECT id, name FROM playerslist ORDER BY name", engine)
        if not df.empty:
            pid_options = df["id"].tolist()

            def safe_format(x):
                row = df[df["id"] == x]
                return row["name"].values[0] if not row.empty else str(x)

            pid = st.selectbox("Select Player to Delete", pid_options, format_func=safe_format)
            if st.button("Delete Player"):
                with engine.begin() as conn:
                    conn.execute(text("DELETE FROM playerslist WHERE id = :pid"), {"pid": pid})
                st.success("🗑️ Player deleted successfully.")
        else:
            st.info("No players available to delete.")

    # --------------------------
    # 🔍 SEARCH PLAYER
    # --------------------------
    with tab_search:
        st.header("Search Player")
        search_term = st.text_input("Enter player name:")
        if search_term.strip():
            query = text("""
                SELECT * FROM playerslist
                WHERE LOWER(name) LIKE LOWER(:term)
                ORDER BY name
            """)
            df_search = pd.read_sql(query, engine, params={"term": f"%{search_term}%"})
            if not df_search.empty:
                st.dataframe(df_search, width='stretch')
            else:
                st.warning("No matching players found.")



