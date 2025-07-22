from request_deals import search_games, top_deals
import sqlite3
import requests

# Function that creates the table in the database for deals
def create_deals_table():
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    table.execute("""
                CREATE TABLE IF NOT EXISTS deals (
                    dealID TEXT PRIMARY KEY,
                    title TEXT,
                    storeID INTEGER,
                    gameID INTEGER,
                    salePrice REAL,
                    normalPrice REAL,
                    savings REAL,
                    metacriticScore INTEGER,
                    steamRatingPercent INTEGER,
                    steamAppID TEXT,
                    dealRating REAL,
                    thumb TEXT
                )
            """)
    conn.commit()
    conn.close()
    
# Function that inserts a deal into the database
def insert_deal(deal):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    table.execute("""
            INSERT OR REPLACE INTO deals (
                dealID, title, storeID, gameID, salePrice, normalPrice,
                savings, metacriticScore, steamRatingPercent, steamAppID, dealRating, thumb 
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            """, (
                deal.get("dealID"),
                deal.get("title"),
                int(deal.get("storeID", 0)),
                int(deal.get("gameID", 0)),
                float(deal.get("salePrice", 0)),
                float(deal.get("normalPrice", 0)),
                float(deal.get("savings", 0)),
                int(deal.get("metacriticScore", 0)) if deal.get("metacriticScore") else None,
                int(deal.get("steamRatingPercent", 0)) if deal.get("steamRatingPercent") else None,
                deal.get("steamAppID"),
                float(deal.get("dealRating", 0)),
                deal.get("thumb")
            ))
    conn.commit()
    conn.close()
    
# Function that will store deals retrieved from the CheapShark API
def store_deals():
    deals = top_deals(50000)
    for deal in deals:
        insert_deal(deal)
        
# Function that deletes deals from the database
def delete_deal(dealID):
    conn = sqlite3.connect("deals.db")
    table = conn.cursor()
    table.execute("DELETE FROM deals WHERE dealID = ?", (dealID,))
    conn.commit()
    conn.close()
    
# Function that updates current deals in the database
def update_deal(dealID, **kwargs):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    fields = []
    values = []
    for key, value in kwargs.items():
        fields.append(f"{key} = ?")
        values.append(value)
    values.append(dealID)
    query = f"UPDATE deals SET {', '.join(fields)} WHERE dealID = ?"
    table.execute(query, values)
    conn.commit()
    conn.close()

# Returns top 50 deals from the database
def get_top_50_deals():
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    table.execute("""
        SELECT title, storeID, salePrice, normalPrice, savings, dealRating, thumb, dealID
        FROM deals
        ORDER BY dealRating DESC
        LIMIT 50
    """)
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

# Search for games from the database
def search_games_database(title, limit=50):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    table.execute("""
        SELECT * FROM deals
        WHERE title LIKE ?
        ORDER BY dealRating DESC
        LIMIT ?
        """, (f"%{title}%", limit))
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

def sort_by_alphabetical(limit=50):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    table.execute("""
                  SELECT * FROM deals
                  ORDER BY title ASC
            """)
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

def sort_by_sales_price(limit=50):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    table.execute("""
                  SELECT * FROM deals
                  ORDER BY salePrice ASC
            """)
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

def sort_by_normal_price(limit=50):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    table.execute("""
                  SELECT * FROM deals
                  ORDER BY normalPrice ASC
            """)
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

def sort_by_deal_rating(limit=50):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    table.execute("""
                  SELECT * FROM deals
                  ORDER by dealRating DESC
            """)
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

def sort

def clear_deals_table():
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    table.execute("DELETE FROM deals")
    conn.commit()
    conn.close()
    
# ----------------------------------------------------------------------------------------
# Database section for emails

# Create email table
def create_email_table():
    conn = sqlite3.connect("deals.db", isolation_level = None)
    table = conn.cursor()
    table.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            emailID INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            subscribed INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()
    
# Insert emails entered in by the user
def insert_email(email):
    conn = sqlite3.connect("deals.db", isolation_level = None)
    table = conn.cursor()
    try:
        table.execute("INSERT INTO emails (email) VALUES (?)", (email,))
    except sqlite3.IntegrityError:
        print(f"Email {email} already exists in the database...")
    conn.commit()
    conn.close()

# Helper function to look at the database
def get_emails():
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    table.execute("SELECT email FROM emails")
    emails = [row[0] for row in table.fetchall()]
    conn.close()
    return emails
