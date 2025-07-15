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
import urllib.parse

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