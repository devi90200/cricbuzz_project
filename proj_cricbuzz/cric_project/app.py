import streamlit as st
import pandas as pd
import sqlite3
import requests
import ssl
import certifi

from db import get_conn, ensure_schema_and_seed, Query_List
from cric_api import get_live_matches, fetch_cricbuzz_rankings, get_live_scorecard

# --------------------------
# Initialize DB
# --------------------------
ensure_schema_and_seed()
conn = get_conn()

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
          ├── db.py             # SQLite database initialization
          ├── app.py                  # Streamlit main dashboard file
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
                st.dataframe(df_matches, use_container_width=True)
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
    st.header("📊 Player Rankings")
    try:
        rankings = fetch_cricbuzz_rankings()
        if rankings:
            df_rankings = pd.DataFrame(rankings)
            format_choice = st.radio("📌 Select Format", ["ODI", "T20", "Test"], horizontal=True)
            category_choice = st.radio("📌 Select Category", ["Batsmen", "Bowlers", "Allrounders", "Teams"], horizontal=True)
            
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
# Player Search Page
# --------------------------
elif page == "Search Player":
    st.header("🔍 Search Player Info (Local DB)")
    search_name = st.text_input("Enter Player Name", "")
    if search_name:
        try:
            query = "SELECT * FROM players WHERE full_name LIKE ?"
            df_players = pd.read_sql_query(query, conn, params=(f"%{search_name}%",))
            if not df_players.empty:
                st.success(f"Found {len(df_players)} player(s):")
                for _, row in df_players.iterrows():
                    st.subheader(row["full_name"])
                    st.write(f"**Country:** {row['country']}")
                    st.write(f"**Role:** {row['role']}")
                    st.write(f"**Batting Style:** {row['batting_style']}")
                    st.write(f"**Bowling Style:** {row['bowling_style']}")
            else:
                st.warning("No players found in the database.")
        except Exception as e:
            st.error(f"Error fetching players from DB: {e}")

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
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No rows returned.")
        except Exception as e:
            st.error(f"Query failed: {e}")

# --------------------------
# CRUD Operations Page
# --------------------------
elif page == "CRUD Operations":
    st.subheader("🛠 Player Management (Local DB)")
    tab_add, tab_view, tab_update, tab_delete = st.tabs(["Add", "View", "Update", "Delete"])

    # ➕ Add Player
    with tab_add:
        with st.form("add_player"):
            name = st.text_input("Full Name")
            country = st.text_input("Country")
            role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper", "Unknown"])
            batting = st.text_input("Batting Style", placeholder="Right-hand bat / Left-hand bat")
            bowling = st.text_input("Bowling Style", placeholder="Right-arm offbreak / Left-arm fast")
            submitted = st.form_submit_button("Add Player")
            if submitted:
                try:
                    cur = conn.cursor()
                    cur.execute(
                        "INSERT INTO players(full_name, country, role, batting_style, bowling_style) VALUES (?, ?, ?, ?, ?)",
                        (name, country, role, batting, bowling),
                    )
                    conn.commit()
                    st.success("Player added.")
                except Exception as e:
                    st.error(f"Insert failed: {e}")

    # 👀 View Players
    with tab_view:
        st.write("All Players")
        try:
            df = pd.read_sql_query(
                "SELECT player_id, full_name, country, role, batting_style, bowling_style FROM players", conn
            )
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No players in the database.")
        except Exception as e:
            st.error(f"Load failed: {e}")

    # ✏️ Update Player
    with tab_update:
        st.write("Update Player Role / Styles")
        try:
            df = pd.read_sql_query("SELECT player_id, full_name FROM players", conn)
            id_list = df["player_id"].tolist() if not df.empty else []
        except:
            id_list = []
        pid = st.selectbox("Player ID", id_list) if id_list else None
        new_role = st.selectbox("New Role", ["(no change)", "Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
        new_bat = st.text_input("New Batting Style (leave blank = no change)")
        new_bowl = st.text_input("New Bowling Style (leave blank = no change)")
        if st.button("Update") and pid:
            try:
                fields, params = [], []
                if new_role != "(no change)":
                    fields.append("role = ?")
                    params.append(new_role)
                if new_bat.strip():
                    fields.append("batting_style = ?")
                    params.append(new_bat.strip())
                if new_bowl.strip():
                    fields.append("bowling_style = ?")
                    params.append(new_bowl.strip())
                if not fields:
                    st.info("Nothing to update.")
                else:
                    params.append(pid)
                    sql = f"UPDATE players SET {', '.join(fields)} WHERE player_id = ?"
                    cur = conn.cursor()
                    cur.execute(sql, params)
                    conn.commit()
                    st.success("Player updated.")
            except Exception as e:
                st.error(f"Update failed: {e}")

    # 🗑 Delete Player
    with tab_delete:
        st.write("Delete Player")
        try:
            df = pd.read_sql_query("SELECT player_id, full_name FROM players", conn)
            id_list = df["player_id"].tolist() if not df.empty else []
        except:
            id_list = []
        pid = st.selectbox("Player ID to delete", id_list) if id_list else None
        if st.button("Delete") and pid:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM players WHERE player_id = ?", (pid,))
                conn.commit()
                st.success("Player deleted.")
            except Exception as e:
                st.error(f"Delete failed: {e}")
