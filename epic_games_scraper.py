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

def build_url(genre):
    return f"https://store.epicgames.com/en-US/browse?sortBy=releaseDate&sortDir=DESC&tag={genre}&priceTier=tierDiscouted&category=Game&count=40&start=0"

def search_deals(genre):
    driver = setup_driver()
    deals = []
    
    try:
        
        url = build_url(genre)
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