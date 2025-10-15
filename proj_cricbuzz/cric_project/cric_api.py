import requests
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import time
# API Configuration
API_KEY = "3de33699f7msh56cd4727142f71ap17e4e8jsncb26c32b27dc"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}
DB_NAME = "cricbuzz_db"
DB_USER = "postgres"
DB_PASSWORD = "DEVI"
DB_HOST = "localhost"
DB_PORT = "5432"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# --------------------------
# API Functions

@st.cache_data(ttl=60)
def get_live_matches():
    url = f"https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    data = response.json()
    matches = []
    for match_type in data.get("typeMatches", []):
        for series_match in match_type.get("seriesMatches", []):
            if "seriesAdWrapper" in series_match:
                for m in series_match["seriesAdWrapper"].get("matches", []):
                    info = m.get("matchInfo", {})
                    matches.append({
                        "Series": series_match["seriesAdWrapper"]["seriesName"],
                        "Match": f"{info.get('team1', {}).get('teamName')} vs {info.get('team2', {}).get('teamName')}",
                        "Venue": info.get("venueInfo", {}).get("ground"),
                        "Status": info.get("status"),
                    })
    return matches

@st.cache_data(ttl=60)
def get_live_scorecard(match_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/40381/hscard"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"Error fetching scorecard for match {match_id}: {e}")
        return None


@st.cache_data(ttl=600)
def fetch_cricbuzz_rankings():
    """
    Fetches ICC player/team rankings from Cricbuzz API using RapidAPI.
    Caches results for 10 minutes.
    """
    rankings = []
    base_url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/rankings"
    endpoints = {
        "Batsmen_ODI": f"{base_url}/batsmen?formatType=odi",
        "Batsmen_T20": f"{base_url}/batsmen?formatType=t20",
        "Batsmen_Test": f"{base_url}/batsmen?formatType=test",
        "Bowlers_ODI": f"{base_url}/bowlers?formatType=odi",
        "Bowlers_T20": f"{base_url}/bowlers?formatType=t20",
        "Bowlers_Test": f"{base_url}/bowlers?formatType=test",
        "Allrounders_ODI": f"{base_url}/allrounders?formatType=odi",
        "Allrounders_T20": f"{base_url}/allrounders?formatType=t20",
        "Allrounders_Test": f"{base_url}/allrounders?formatType=test",
        "Teams_ODI": f"{base_url}/teams?formatType=odi",
        "Teams_T20": f"{base_url}/teams?formatType=t20",
        "Teams_Test": f"{base_url}/teams?formatType=test",
    }

    for category, url in endpoints.items():
        try:
            res = requests.get(url, headers=HEADERS, timeout=10)
            res.raise_for_status()
            data = res.json()

            for p in data.get("rank", []):
                rankings.append({
                    "Category": category,
                    "Rank": p.get("rank"),
                    "Player": p.get("name"),
                    "Team": p.get("country"),
                    "Rating": p.get("rating"),
                    "Image": (
                        f"https://cricbuzz-cricket.p.rapidapi.com/img/v1/i1/c{p.get('faceImageId')}/i.jpg"
                        if p.get("faceImageId") else ""
                    )
                })
        except Exception as e:
            print(f"⚠️ Error fetching {category}: {e}")

    return rankings


BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player"

@st.cache_data(ttl=300)
def get_player_info(player_id: str):
    """
    Fetch player info safely.
    Returns a dict with only guaranteed fields, avoids null/empty values.
    """
    info = {}
    try:
        res_info = requests.get(f"{BASE_URL}/{player_id}", headers=HEADERS, timeout=15)
        if res_info.status_code == 429:
            print(f"Rate limit hit for player {player_id}, sleeping 60s...")
            time.sleep(60)
            res_info = requests.get(f"{BASE_URL}/{player_id}", headers=HEADERS, timeout=15)

        res_info.raise_for_status()
        data = res_info.json()

        # Only keep guaranteed info
        info = {
            "id": player_id,
            "name": data.get("playerInfo", {}).get("name", "N/A"),
            "dob": data.get("playerInfo", {}).get("DoB", "N/A"),
            "teamName": data.get("playerInfo", {}).get("teams", [])
        }

    except Exception as e:
        print(f"❌ get_player_info() error for {player_id}: {e}")

    return info

@st.cache_data(ttl=300)
def search_player(name: str):
    """Search players by name. Returns a safe list of player dicts with only reliable fields."""
    try:
        if not name.strip():
            return []

        params = {"plrN": name}
        res = requests.get(f"{BASE_URL}/search", headers=HEADERS, params=params, timeout=15)

        if res.status_code == 429:
            print("⚠️ Rate limit hit. Retrying after 60s...")
            time.sleep(60)
            return search_player(name)

        res.raise_for_status()
        players_raw = res.json().get("player", [])

        # Only keep safe fields
        players_safe = []
        for p in players_raw:
            players_safe.append({
                "id": p.get("id"),
                "name": p.get("name"),
                "teamName": p.get("teamName", "N/A"),
                "dob": p.get("dob", "N/A")
            })
        return players_safe

    except Exception as e:
        print(f"❌ search_player() error: {e}")
        return []