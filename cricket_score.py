import requests
import time
import os
from datetime import datetime

# CONFIG 
REFRESH_SECONDS = 30

# ESPN public cricket API endpoints — no key needed
LEAGUES = {
    "1": ("IPL 2025",          "https://site.api.espn.com/apis/site/v2/sports/cricket/8048/scoreboard"),
    "2": ("International (All)","https://site.api.espn.com/apis/site/v2/sports/cricket/7645/scoreboard"),
    "3": ("Women's Cricket",    "https://site.api.espn.com/apis/site/v2/sports/cricket/8238/scoreboard"),
}

HEADERS = {"User-Agent": "Mozilla/5.0"}

# HELPERS 
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def now():
    return datetime.now().strftime("%I:%M:%S %p")

# FETCH DATA 
def fetch_scores(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        return res.json()

    except requests.exceptions.ConnectionError:
        return {"error": "No internet connection."}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Try again."}
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e}"}
    except Exception as e:
        return {"error": str(e)}

# DISPLAY SCORES 
def display(data, league_name):
    print(f" LIVE CRICKET — {league_name}")
    print(f"    Last updated: {now()}")
    print("=" * 52)

    # Handle errors
    if "error" in data:
        print(f"\n   {data['error']}\n")
        return

    events = data.get("events", [])

    # No matches right now
    if not events:
        print("\n   No live matches right now.")
        print("     Try again during match hours.\n")
        return

    # Loop through each match
    for event in events:
        match_name = event.get("shortName", event.get("name", "Unknown Match"))
        status     = event.get("status", {})
        state      = status.get("type", {}).get("description", "")
        detail     = status.get("detail", "")

        print(f"\n  🏟️  {match_name}")
        print(f"  📌 {state}")

        # Teams and scores
        competitions = event.get("competitions", [])
        if competitions:
            competitors = competitions[0].get("competitors", [])
            for team in competitors:
                team_name = team.get("team", {}).get("shortDisplayName", "?")
                score     = team.get("score", "N/A")
                print(f"      {team_name:<20} {score}")

        # Ball-by-ball detail
        if detail:
            print(f"\n  {detail}")

        print("  " + "─" * 48)

# MAIN LOOP 
def main():
    clear()
    print("Cricket Score Tracker\n")
    print("Select league:")
    for key, (name, ) in LEAGUES.items():
        print(f"  {key} → {name}")

    choice = input("\nEnter choice (1/2/3): ").strip()

    if choice not in LEAGUES:
        print("Invalid choice. Defaulting to IPL.")
        choice = "1"

    league_name, url = LEAGUES[choice]

    print(f"\nTracking {league_name}...")
    print("Press Ctrl+C anytime to stop.\n")
    time.sleep(1)

    while True:
        clear()
        data = fetch_scores(url)
        display(data, league_name)
        print(f"\n Refreshing in {REFRESH_SECONDS}s... | Ctrl+C to quit")

        time.sleep(REFRESH_SECONDS)

if name == "main":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  👋 Stopped. Enjoy the match!\n")
