from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4
import time

# Steam uses ids to represent their genres
# Will be used to query for specific genres when scraping
GENRE_TAGS = {
    "action": 19,
    "indie": 492,
    "rpg": 122,
    "Simulation": 599,
    "Sports": 701,
    "Early Access": 493,
    "horror": 1667
}

STEAM_CSV_FILE = "steam.csv"
RESULTS_PER_PAGE = 25

# Developed by Garrett: Setup the driver for Chrome 
# Run in headless mode
def setup_driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

# Developed by Garrett: Get the genre to search for by the user
def get_genre():
    print("Available Genres: ")
    for genre in GENRE_TAGS.keys():
        print(f"- {genre}")
        
    genre_opt = input("Choose your genre you want to search: ")
    while genre_opt not in GENRE_TAGS.keys():
        genre_opt = input("Please choose a valid genre: ")
        
    return genre_opt

# Developed by Garrett: Returns url string of genre and next page
def build_url(genre, page):
    return f"https://store.steampowered.com/search/?specials=1&tags={genre}&page={page}"

def search_deals(genre, driver):
    deals = []
    pass

def main():
    genre = get_genre()
    url = build_url(genre, 3)
    driver = setup_driver()
    driver.get(url)
    print(driver.current_url)
    time.sleep(3)
    driver.quit()
    print("Driver Closed.")
    
if __name__ == "__main__":
    main()