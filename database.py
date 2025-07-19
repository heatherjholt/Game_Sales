from request_deals import search_games, top_deals
import sqlite3

# Function that creates the table in the database for
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
    
def store_deals():
    deals = top_deals(50000)
    for deal in deals:
        insert_deal(deal)
        
def delete_deal(dealID):
    conn = sqlite3.connect("deals.db")
    table = conn.cursor()
    table.execute("DELETE FROM deals WHERE dealID = ?", (dealID,))
    conn.commit()
    conn.close()
    
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
        

# ----------------------------------------------------------------------------------------
# Database section for emails

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
    
def insert_email(email):
    conn = sqlite3.connect("deals.db", isolation_level = None)
    table = conn.cursor()
    try:
        table.execute("INSERT INTO emails (email) VALUES (?)", (email,))
    except sqlite3.IntegrityError:
        print(f"Email {email} already exists in the database...")
    conn.commit()
    conn.close()

def get_emails():
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    table.execute("SELECT email FROM emails")
    emails = [row[0] for row in table.fetchall()]
    conn.close()
    return emails
    
create_email_table()
insert_email("gfj2e@outlook.com")
emails = get_emails()
print(emails)