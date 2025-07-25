import requests

API_URL = "https://www.cheapshark.com/api/1.0"
DEALS_URL = f"{API_URL}/deals"
STORES_URL = f"{API_URL}/stores"
GAMES_URL = f"{API_URL}/games"

# Function that takes a title and returns the games matching it
def search_games(title, limit = 10):
    params = {"title": title, "limit": limit, "exact": 0}
    
    response = requests.get(DEALS_URL, params, timeout=10)
    response.raise_for_status()
    
    return response.json()

# Function that finds the cheapest entry of a game, could be modified later to sort by cheapest
def return_cheapest_entry(games):
    if not games:
        return None
    return min(games, key=lambda g: float(g.get("cheapest",0)))

# Function to return highest rating
def return_highest_rating(games):
    if not games:
        return None
    return max(games, key=lambda g: float(g.get("dealRating",0)))

# Function to pull all top deals
def top_deals(n):
    resp = requests.get(DEALS_URL, params={"pageSize": n}, timeout = 10)
    resp.raise_for_status()
    return resp.json()