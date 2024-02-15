# Scrapes the news info from gazeta.uz
# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, csv, sys, psycopg2
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta


# Calculate yesterday's date
yesterday = datetime.now() - timedelta(days=1)

def gazeta():    
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
    
    
    article_urls = []
    page_number = 1
    while True:
        driver.get(f"https://www.gazeta.uz/uz/list/news?page={page_number}")
        news_cards = driver.find_elements(By.CLASS_NAME, "nblock")
        for card in news_cards:
            card_date = date_to_datetime(card.find_element(By.CLASS_NAME, "ndt").text.strip())
            if card_date.date() == yesterday.date():
                article_urls.append({"article_url": card.find_element(By.TAG_NAME, "a").get_attribute("href"),
                                    "publication_datetime": card_date})
        if card_date.date() < yesterday.date():
            print("Breaking here")
            break
        page_number += 1

    return collect_article_details(driver, article_urls)
   

    

def collect_article_details(driver, article_urls):
    article_details = []
    i = 0
    for article in article_urls:
        driver.get(article["article_url"])
        article_headline = driver.find_element(By.ID, "article_title").text.strip()
        article_thesis = driver.find_element(By.CLASS_NAME, "js-mediator-article").text.strip()
        thesis_length_words = len(article_thesis.split())
        thesis_length_chars = len(article_thesis.replace(" ", ""))
        try:
            number_of_views = driver.find_element(By.CLASS_NAME, "views-count").text.strip()
        except Exception as e:
            try:                       
                number_of_views = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[3]/div[1]/div[3]").text.split("\n")[0].split("»")[1].strip()
            except Exception as e:
                number_of_views = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[3]/div[1]/div[3]").text.split("\n")[0].split(".")[1].strip()
        category = driver.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text.strip()
        article_details.append({"article_url": article["article_url"], 
                                "headline": article_headline, 
                                "thesis_length_words": thesis_length_words, 
                                "thesis_length_chars": thesis_length_chars, 
                                "publication_datetime": article["publication_datetime"], 
                                "article_category": category, 
                                "number_of_views": int(number_of_views.replace(" ", "")), 
                                "article_source": "Gazeta.uz"})
    return article_details

def date_to_datetime(date):
    if "Кеча" in date:
        time = date.split(" ")[1]
        publication_datetime = f"{yesterday.date()} {time}"
        print(publication_datetime)
        publication_datetime = datetime.strptime(publication_datetime, "%Y-%m-%d %H:%M")
        return publication_datetime
    elif "Бугун" in date:
        return datetime.now()
    else:
        return datetime.now() - timedelta(days=2)

gazeta()