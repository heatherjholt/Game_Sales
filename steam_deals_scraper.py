from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import os

# Steam uses ids to represent their genres
# Will be used to query for specific genres when scraping
GENRE_TAGS = {
    "action": 19,
    "indie": 492,
    "rpg": 122,
    "simulation": 599,
    "sports": 701,
    "early Access": 493,
    "horror": 1667
}

STEAM_CSV_FILE = "steam.csv"
RESULTS_PER_PAGE = 25
MAX_PAGES = 1

# Developed by Garrett: Setup the driver for Chrome 
# Run in headless mode
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    print("Driver Initialized")
    return driver

# Developed by Garrett: Get the genre to search for by the user
def get_genre():
    print("Available Genres: ")
    for genre in GENRE_TAGS.keys():
        print(f"- {genre}")
        
    genre_opt = input("Choose your genre you want to search: ").lower()
    while genre_opt not in GENRE_TAGS.keys():
        genre_opt = input("Please choose a valid genre: ").lower()
        
    return GENRE_TAGS[genre_opt]

# Developed by Garrett: Returns url string of genre and next page
def build_url(genre, page):
    return f"https://store.steampowered.com/search/?specials=1&tags={genre}&page={page}"

# Developed by Garrett: The code that scrapes the actual steam page
def search_deals(genre):
    driver = setup_driver()
    deals = []
    
    try:
        for page in range(1, MAX_PAGES + 1):
            url = build_url(genre, page)
            driver.get(url)
            
            wait = WebDriverWait(driver, 10)
            
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.search_result_row")))
            
            time.sleep(1)
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            rows = soup.select("a.search_result_row")
            
            if rows:
                for row in rows:
                    title_element = row.select_one(".title")
                    discount_element = row.select_one(".discount_pct")
                    original_price_element = row.select_one(".discount_original_price")
                    discounted_price_element = row.select_one(".discount_final_price")
                    game_url = row.get("href", "").strip()

                    deal = {
                        "title": title_element.text.strip() if title_element else "",
                        "discount": discount_element.text.strip() if discount_element else "",
                        "original price": original_price_element.text.strip() if original_price_element else "",
                        "discount price": discounted_price_element.text.strip() if discounted_price_element else "",
                        "url": game_url if game_url else ""
                    } 
                    deals.append(deal)
                
                print(f"Page {page}: Scrapped {len(rows)} deals.")
            else:
                print(f"No results on page {page}.")
                
    except NoSuchElementException:
        driver.quit()
    
    driver.quit()
    
    return deals

# Developed by Garrett: Writes the dictionary of deals to a csv file
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
    write_to_csv(deals, STEAM_CSV_FILE)
    print("Driver Closed.")
    
if __name__ == "__main__":
    main()