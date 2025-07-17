from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GAMES_API = "https://www.cheapshark.com/api/1.0/games"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '')
    params = {
        'title': query,
        'limit': 5
    }
    response = requests.get(GAMES_API, params=params)
    suggestions = []
    if response.status_code == 200:
        suggestions = [game['external'] for game in response.json()]
    return jsonify(suggestions)

if __name__ in "__main__":
    app.run(debug=True)
    
