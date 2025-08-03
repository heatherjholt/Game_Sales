from request_deals import top_deals
import sqlite3

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
    
# Creates a seperate table for searches
def create_searches_table():
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    table.execute("""
                CREATE TABLE IF NOT EXISTS searches (
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
def insert_deal(deal, table_name="deals"):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    table.execute(f"""
            INSERT OR REPLACE INTO {table_name} (
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
def store_deals(num_deals):
    deals = top_deals(num_deals)
    for deal in deals:
        insert_deal(deal)
        
def store_searches(num_deals):
    deals = top_deals(num_deals)
    for deal in deals:
        insert_deal(deal, "searches")
        
# Function that deletes deals from the database, unused
def delete_deal(dealID, table_name="deals"):
    conn = sqlite3.connect("deals.db")
    table = conn.cursor()
    table.execute(f"DELETE FROM {table_name} WHERE dealID = ?", (dealID,))
    conn.commit()
    conn.close()
    
# Function that updates current deals in the database, unused
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
        SELECT * FROM searches
        WHERE title LIKE ?
        ORDER BY dealRating DESC
        LIMIT ?
        """, (f"%{title}%", limit))
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

# Function that sorts by alphabetical order using database sorting
def sort_by_alphabetical(table_name="deals", limit=50, search_query=None):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    if search_query:
        table.execute(f"""SELECT * FROM {table_name}
                      WHERE title LIKE ? ORDER
                      BY title ASC LIMIT ?
                      """, (f"%{search_query}%", limit))
    else:
        table.execute(f"""
                    SELECT * FROM {table_name}
                    ORDER BY title ASC LIMIT ?
                """, (limit,))
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

# Function that sorts by games' sales price
def sort_by_sales_price(table_name="deals", limit=50, search_query=None):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    if search_query:
        table.execute(f"""SELECT * FROM {table_name}
                      WHERE title LIKE ?
                      ORDER BY salePrice ASC LIMIT ?
                      """, (f"%{search_query}%", limit))
    else:
        table.execute(f"""
                    SELECT * FROM {table_name}
                    ORDER BY salePrice ASC
                    LIMIT ?""", (limit,))
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

# Sort by normal or original price
def sort_by_normal_price(table_name="deals", limit=50, search_query=None):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    if search_query:
        table.execute(f""" SELECT * FROM {table_name}
                      WHERE title LIKE ? ORDER
                      BY normalPrice ASC LIMIT ?
                      """, (f"%{search_query}%", limit))
    else:
        table.execute(f"""
                    SELECT * FROM {table_name}
                    ORDER BY normalPrice ASC LIMIT ?
                    """, (limit,))
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

# Sort by deal rating, which is the default, but needed if user wants to resort by deal rating
def sort_by_deal_rating(table_name="deals", limit=50, search_query=None):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    if search_query:
        table.execute(f"""SELECT * FROM {table_name}
                      WHERE title LIKE ? ORDER
                      BY dealRating DESC LIMIT ?
                      """, (f"%{search_query}%", limit))
    else:    
        table.execute(f"""
                    SELECT * FROM {table_name}
                    ORDER by dealRating DESC LIMIT ?
                    """, (limit,))
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

# Sort by the amount of money saved
def sort_by_savings(table_name="deals", limit=50, search_query=None):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    conn.row_factory = sqlite3.Row
    table = conn.cursor()
    if search_query:
        table.execute(f"""SELECT * FROM {table_name}
                      WHERE title LIKE ? ORDER BY 
                      savings DESC LIMIT ? 
                      """, (f"%{search_query}%", limit))
    else:
        table.execute(f"""
                    SELECT * FROM {table_name}
                    ORDER BY savings DESC LIMIT ?
                    """, (limit,))
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

# Clear the table of deals
def clear_table(table_name="deals"):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    table.execute(f"DELETE FROM {table_name}")
    conn.commit()
    conn.close()
    
# Planned function to hide duplicates but didnt have time to implement
def hide_duplicates(table_name="deals"):
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    table.execute(f"""
                  SELECT * FROM {table_name} WHERE (title, salePrice)
                  IN (SELECT title, MIN(salePrice) FROM {table_name} GROUP BY title
    """)
    deals = [dict(row) for row in table.fetchall()]
    conn.close()
    return deals

# Testing function
def print_to_text_file(deals, filename="deals.txt"):
    with open(filename, "w") as f:
        for i, deal in enumerate(deals, 1):
            f.write(f"{i}. {deal['title']} | StoreID: {deal['storeID']} | Sale Price: ${deal['salePrice']} | Normal Price: ${deal['normalPrice']} | Savings: {deal['savings']}% | Deal Rating: {deal['dealRating']}\n")
    
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

# Function that gets the emails and returns them to send emails to
def get_emails():
    conn = sqlite3.connect("deals.db", isolation_level=None)
    table = conn.cursor()
    table.execute("SELECT email FROM emails")
    emails = [row[0] for row in table.fetchall()]
    conn.close()
    return emails
