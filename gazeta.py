# Scrapes the news info from daryo.uz
# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, csv, sys, psycopg2
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta



def daryo():
    # Calculate yesterday's date
    yesterday = datetime.now().date() - timedelta(days=1)

    # Declare categories
    
    
    # Set options (prevents the browser from closing after opening)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')

    # Open the browser
    print('Opening browser')
    driver = webdriver.Chrome(options=options)
    print('Opened browser')
    actions = ActionChains(driver)

    # Maximize the browser to fullscreen
    driver.maximize_window()
    print('Maxed browser')

    # Open the webpage
    driver.implicitly_wait(7)
    news_cards = []
    page_number = 1
    while True:
        driver.get(f"https://www.gazeta.uz/uz/list/news?page={page_number}")
        news_cards.append(driver.find_elements(By.CLASS_NAME, "nblock"))
        if news_cards[-1].find_element(By.CLASS_NAME, "ndt").text:
            pass


    # Collect info
    ### Load more 
