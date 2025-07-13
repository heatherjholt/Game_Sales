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

def main():
    driver = setup_driver()
    time.sleep(3)
    driver.quit()
    
if __name__ == "__main__":
    main()