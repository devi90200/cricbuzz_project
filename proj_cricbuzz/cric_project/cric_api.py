import requests
import streamlit as st
import pandas as pd
# API Configuration
API_KEY = "ad7d733d99mshcd9c76b99e35d43p1309a5jsn8ffde0c445d0"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

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

            # Check data structure
            for p in data.get("rank", []):
                rankings.append({
                    "Category": category,
                    "Rank": p.get("rank"),
                    "Player": p.get("name"),
                    "Team": p.get("country"),
                    "Rating": p.get("rating"),
                    "Image": p.get("faceImageId", "")
                })
        except Exception as e:
            print(f"Error fetching {category}: {e}")

    return rankings

