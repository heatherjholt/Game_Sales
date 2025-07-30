#flask creates the web app, render_template for index.html, 
#requests to get data from the user, jsonify returns the json data for autocomplete
from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
from request_deals import search_games
# For database functions
from database import *
#for email subscription 
from mailer import emailing

app = Flask(__name__)

#api url for the games and deals
GAMES_API = "https://www.cheapshark.com/api/1.0/games"
STORES_API = "https://www.cheapshark.com/api/1.0/stores"
RESULTS_PER_PAGE = 50

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
    #deals = get_top_50_deals()
    sort = request.args.get("sort", "")
    view = request.args.get("view", "list")
    if   sort == "alpha":   deals = sort_by_alphabetical(limit=RESULTS_PER_PAGE)
    elif sort == "sale":    deals = sort_by_sales_price(limit=RESULTS_PER_PAGE)
    elif sort == "original": deals = sort_by_normal_price(limit=RESULTS_PER_PAGE)
    elif sort == "savings": deals = sort_by_savings(limit=RESULTS_PER_PAGE)
    elif sort == "rating":  deals = sort_by_deal_rating(limit=RESULTS_PER_PAGE)
    else:                   deals = get_top_50_deals()
    #TESTING print(deals[6])
    return render_template(
      "index.html",
      deals=deals,
      sort=sort,
      view=view, 
      store_map=store_map,
      title="Top 50 Deals"
    )



@app.route("/search", methods=["GET", "POST"])
def search():
#support both GET and POST fallback
    query = (request.args.get("title") if request.method == "GET"
                                    else request.form.get("title", ""))
    query = (query or "").strip()

    if not query:
        return redirect(url_for("index"))

#grab sort & view params exactly as in index()
    sort = request.args.get("sort", "")
    view = request.args.get("view", "list")

#get deals
    deals = search_games_database(query)
    if not deals:
        results = search_games(query)
        for d in results:
             d["storeID"] = int(d["storeID"])
             insert_deal(d, "searches")
        deals = search_games_database(query)

#apply sort after fetching search hits
    if   sort == "alpha":    deals.sort(key=lambda d: d["title"].lower())
    elif sort == "sale":     deals.sort(key=lambda d: d["salePrice"])
    elif sort == "original": deals.sort(key=lambda d: d["normalPrice"])
    elif sort == "savings":  deals.sort(key=lambda d: d["savings"], reverse=True)
    elif sort == "rating":   deals.sort(key=lambda d: d["dealRating"], reverse=True)

    return render_template("index.html",deals=deals,store_map=store_map,title=f"Search results for: {query}",search_query=query,sort=sort,view=view)


#listens for get request, uses javascript to send request to api, returns top 5 suggestions (currently)
@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '')
    params = {'title': query, 'limit': 5}
    response = requests.get(GAMES_API, params=params)
    suggestions = [game['external'] for game in response.json()] if response.ok else []
    return jsonify(suggestions)

#email subscription
@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        insert_email(email)
        #emailing()
        return redirect(url_for('index')), emailing()

if __name__ in "__main__":
    create_email_table() 
    create_deals_table()
    create_searches_table()
    clear_table()
    clear_table("searches")
    store_deals(1000)
    store_searches(50000)
    app.run(debug=True)
