# players_fetch.py
import requests
import pandas as pd
import time
from sqlalchemy import create_engine

# ---------- CONFIGURATION ----------
API_SEARCH = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
API_INFO = "https://cricbuzz-cricket2.p.rapidapi.com/stats/v1/player/{}"  # player_id
HEADERS = {
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com",
    "x-rapidapi-key": "3de33699f7msh56cd4727142f71ap17e4e8jsncb26c32b27dc"
}

DB_NAME = "cricbuzz_db"
DB_USER = "postgres"
DB_PASSWORD = "DEVI"
DB_HOST = "localhost"
DB_PORT = "5432"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# ---------- FUNCTIONS ----------
def fetch_players_for_letter(letter):
    """Fetch players starting with a letter"""
    try:
        params = {"plrN": letter}
        res = requests.get(API_SEARCH, headers=HEADERS, params=params, timeout=10)
        if res.status_code == 429:
            print(f"Rate limit hit, sleeping 60s for '{letter}'")
            time.sleep(60)
            return fetch_players_for_letter(letter)
        res.raise_for_status()
        data = res.json()
        return data.get("player", [])
    except Exception as e:
        print(f"Error fetching letter {letter}: {e}")
        return []

def fetch_player_info(player_id):
    """Fetch full bio for a player"""
    try:
        res = requests.get(API_INFO.format(player_id), headers=HEADERS, timeout=10)
        if res.status_code == 429:
            print(f"Rate limit hit for player {player_id}, sleeping 5s...")
            time.sleep(5)
            return fetch_player_info(player_id)
        res.raise_for_status()
        data = res.json()
        p = data.get("player", {})
        return {
            "role": p.get("role"),
            "batting_style": p.get("battingStyle"),
            "bowling_style": p.get("bowlStyle"),
            "category": p.get("category"),
            "dob": p.get("dob"),
            "image": p.get("faceImageId")
        }
    except Exception as e:
        print(f"Error fetching player {player_id}: {e}")
        return {}

# ---------- MAIN SCRIPT ----------
all_players = []

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    players = fetch_players_for_letter(letter)
    for p in players:
        all_players.append({
            "player_id": p.get("id"),
            "name": p.get("name"),
            "team": p.get("teamName"),
            "dob": p.get("dob")
        })
    time.sleep(0.5)  # gentle delay

df = pd.DataFrame(all_players).drop_duplicates(subset=["player_id"]).reset_index(drop=True)

# Save basic info
df.to_csv("players_basic.csv", index=False)

# Load into database
df.to_sql("playerslist", engine, if_exists="replace", index=False)
print("✅ Basic players info saved to DB")
