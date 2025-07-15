from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import csv
import os


#Epic games genre tags
GENRE_TAGS = {
    "action": "Action",
    "rpg": "Role%20Playing",
    "shooter": "Shooter",
    "strategy": "Strategy",
    "indie": "Indie",
    "horror": "Horror",
    "puzzle": "Puzzle",
    "sports": "Sports"
}

# Epic CSV file for game deals
EPIC_CSV_FILE = "epic.csv"

# Setting up chrome driver 
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    print("Driver Initialized")
    return driver

def get_genre():
    print("Available Genres: ")
    for genre in GENRE_TAGS.keys():
        print(f"- {genre}")
        
    genre_opt = input("Choose your genre you want to search: ").lower()
    while genre_opt not in GENRE_TAGS.keys():
        genre_opt = input("Please choose a valid genre: ").lower()
        
    return GENRE_TAGS[genre_opt]

def build_url(genre):
    return f"https://store.epicgames.com/en-US/browse?sortBy=releaseDate&sortDir=DESC&tag={genre}&priceTier=tierDiscouted&category=Game&count=40&start=0"

def search_deals(genre):
    driver = setup_driver()
    deals = []
    
    try:
        
        url = build_url(genre)
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-1ufzxyu")))
                
        time.sleep(3)

        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.select("a.css-r227zj")
        
        if rows:
            for row in rows:
                title_element = row.select_one(".css-2ucwu")
                discount_element = ""
                original_price_element = row.select_one(".css-119zqif")
                discounted_price_element = row.select_one(".css-16v43w0")
                game_url = row.get("href", "").strip()

                deal = {
                    "title": title_element.text.strip() if title_element else "",
                    "discount": discount_element.text.strip() if discount_element else "",
                    "original price": original_price_element.text.strip() if original_price_element else "",
                    "discount price": discounted_price_element.text.strip() if discounted_price_element else "",
                    "url": game_url if game_url else ""
                } 
                deals.append(deal)
            
            print(f"Scrapped {len(rows)} deals.")
        else:
            print(f"No results found.")
                
    except NoSuchElementException:
        driver.quit()
    
    driver.quit()
    
    return deals

def write_to_csv(deals, file):
    if deals == []:
        print("No deals to be written.")
        return
    else:
        os.makedirs("deals", exist_ok = True)
        with open(os.path.join("deals", file), "w", newline = "") as f:
            csv_writer = csv.DictWriter(f, ["title", "discount", 
                                            "original price", "discount price", "url"])
            csv_writer.writeheader()
            csv_writer.writerows(deals)
            
def main():
    genre = get_genre()
    deals = search_deals(genre)
    print("Writing to CSV file")
    write_to_csv(deals, EPIC_CSV_FILE)
    print("Driver Closed.")
    
if __name__ == "__main__":
    main()