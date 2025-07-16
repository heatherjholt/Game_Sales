import requests
import os
import time

page_num = 0
URL = f"https://www.cheapshark.com/img/stores/icons/{page_num}.png"

os.makedirs("images", exist_ok = True)

MAX_PAGES = 34

while page_num < MAX_PAGES:
    url = f"https://www.cheapshark.com/img/stores/icons/{page_num}.png"
    print(f"Downloading image {url}...")
    res = requests.get(url)
    res.raise_for_status()
    
    image = open(os.path.join("images", os.path.basename(url)), "wb")
    
    for chunk in res.iter_content(100000):
        image.write(chunk)
    image.close()
    
    page_num += 1
    
    time.sleep(1)
    
print("Done")