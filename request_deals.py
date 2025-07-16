import requests
import csv
import json

API_URL = "https://www.cheapshark.com/api/1.0"
DEALS_URL = f"{API_URL}/deals"
STORES_URL = f"{API_URL}/stores"
GAMES_URL = f"{API_URL}/games"

# Function that takes a title and returns the games matching it
def search_games(title, limit = 10):
    params = {"title": title, "limit": limit}
    
    response = requests.get(GAMES_URL, params, timeout=10)
    response.raise_for_status()
    
    return response.json()

# Function that finds the cheapest entry of a game, could be modified later to sort by cheapest
def return_cheapest_entry(games):
    if not games:
        return None
    return min(games, key=lambda g: float(g["cheapest"]))

# Some testing stuff
def main():
    title = input("Enter title of game to search: ")
    games = search_games(title)
    cheapest_entry = return_cheapest_entry(games)
    print(json.dumps(games, indent = 2))
    print("Cheapest Entry is: \n")
    print(json.dumps(cheapest_entry, indent = 2))
    
if __name__ == "__main__":
    main()