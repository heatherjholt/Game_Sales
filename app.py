#flask creates the web app, render_template for index.html, 
#requests to get data from the user, jsonify returns the json data for autocomplete
from flask import Flask, render_template, request, jsonify
import requests
from request_deals import search_games
from database import create_deals_table, store_deals, get_top_50_deals, insert_deal, search_games_database
from database import clear_deals_table, print_to_text_file
app = Flask(__name__)


#api url for the games and deals
GAMES_API = "https://www.cheapshark.com/api/1.0/games"
STORES_API = "https://www.cheapshark.com/api/1.0/stores"


#maps store names to their to ids
def get_store_map():
    response = requests.get(STORES_API)
    if response.ok:
        stores = response.json()
        return {
            int(store["storeID"]): {
                "storeName": store["storeName"],
                "images": store["images"]
            }
            for store in stores
        }
    return {}
store_map = get_store_map()


#shows home page with top deals and search option 
#get pulls top 50 deals, post searches for title directly 
@app.route("/", methods=["GET"])
def index():
    deals = get_top_50_deals()
    #TESTING print(deals[6])
    return render_template("index.html", deals=deals, store_map=store_map, title="Top 50 Deals") 

@app.route("/search", methods=["GET", "POST"])
def search():
    # Support both GET and POST fallback
    query = request.args.get("title", "") if request.method == "GET" else request.form.get("title", "")
    query = query.strip()

    if not query:
        return redirect(url_for("index"))
    
    deals = search_games_database(query)    # Searches for games in the database from the query
    
    if not deals:                           # Put in deals not found in the database into the database
        print("Deals not found in database...")
        results = search_games(query)
        for deal in results:
            deal["storeID"] = int(deal["storeID"])      # Convert storeID to int for storing in database
            insert_deal(deal)
        deals = search_games_database(query)
    return render_template("index.html", deals=deals, store_map=store_map, title=f"Search results for: {query}", search_query=query)

#listens for get request, uses javascript to send request to api, returns top 5 suggestions (currently)
@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '')
    params = {'title': query, 'limit': 5}
    response = requests.get(GAMES_API, params=params)
    suggestions = [game['external'] for game in response.json()] if response.ok else []
    return jsonify(suggestions)


if __name__ in "__main__":
    create_deals_table()
    clear_deals_table()
    store_deals()
    deals = get_top_50_deals()
    print_to_text_file(deals)
    app.run(debug=True)
