# Scrapes the news info from uznews.uz
# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, csv, sys, psycopg2
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta


# Calculate yesterday's date
yesterday = datetime.now().date() - timedelta(days=1)

def uznews():
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
    driver.get("https://uznews.uz/")
    while True:
        news_cards = []
        news_cards.append(driver.find_element(By.XPATH, "/html/body/div[2]/main/section/div[1]"))
        news_cards = news_cards + driver.find_element(By.CLASS_NAME, "flex.flex-col.gap-5").find_elements(By.CLASS_NAME, "flex.flex-col.justify-between")
        card_date = news_cards[-1].find_element(By.CLASS_NAME, "font-medium.text-black.opacity-70.text_13").text.strip()
        
        if date_to_datetime(card_date).date() < yesterday:
            print("Breaking here")
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.7)

    special_news_cards = news_cards[0:1] + news_cards[4:7] + news_cards[10:13]
    news_cards = news_cards[1:4] + news_cards[7:10] + news_cards[13:]

    article_details = []
    for article in news_cards:
        try:
            card_date = article.find_element(By.CLASS_NAME, "font-medium.text-black.opacity-70.text_13").text.strip()
        except Exception:
            pass
        print(card_date)
        publication_datetime = date_to_datetime(card_date)
        if publication_datetime.date() == yesterday:
            time.sleep(1.5)
            article_url = article.find_element(By.TAG_NAME, "a").get_attribute("href").strip()
            article_headline = article.find_element(By.TAG_NAME, "h3").text.strip()
            article_thesis = article.find_element(By.CLASS_NAME, "height_2_ellips.text-sm.mb-2.description").text.strip()
            thesis_length_words = len(article_thesis.split())
            thesis_length_chars = len(article_thesis.replace(" ", ""))
            number_of_views = article.find_elements(By.TAG_NAME, "div")[3].text.split("\n")[1].strip()
            category = article.find_element(By.CLASS_NAME, "text-xs.text-gray-800.font-medium").text.strip()
            article_details.append({"article_url": article_url, 
                                    "headline": article_headline, 
                                    "thesis_length_words": thesis_length_words, 
                                    "thesis_length_chars": thesis_length_chars, 
                                    "publication_datetime": publication_datetime, 
                                    "article_category": category, 
                                    "number_of_views": int(number_of_views.replace(" ", "")), 
                                    "article_source": "Uznews.uz"})

    article_urls = []
    for article in special_news_cards:
        if "/posts/" in article.find_element(By.TAG_NAME, "a").get_attribute("href").strip():
            article_urls.append({"article_url": article.find_element(By.TAG_NAME, "a").get_attribute("href").strip()})
        else:
            article_urls.append({"article_url": article.find_elements(By.TAG_NAME, "a")[2].get_attribute("href").strip()})

    for article_url in article_urls:
        driver.get(article_url["article_url"])
        article = driver.find_element(By.CLASS_NAME, "p-4.grid.gap-2")
        try:
            card_date = article.find_elements(By.TAG_NAME, "time")[1].text.strip()
        except Exception:
            card_date = article.find_element(By.TAG_NAME, "time").text.strip()
        publication_datetime = date_to_datetime(card_date)
        if publication_datetime.date() == yesterday:
            article_headline = article.find_element(By.TAG_NAME, "h1").text.strip()
            article_thesis = article.find_element(By.TAG_NAME, "p").text.strip()
            thesis_length_words = len(article_thesis.split())
            thesis_length_chars = len(article_thesis.replace(" ", ""))
            number_of_views = article.find_element(By.XPATH, "/html/body/div[2]/main/section/div[1]/div/div[2]/div/div[1]/span[1]/span[1]").text.strip()
            category = article.find_element(By.CLASS_NAME, "text-sm.text-gray-800.font-medium").text.strip()
            article_details.append({"article_url": article_url["article_url"], 
                                    "headline": article_headline, 
                                    "thesis_length_words": thesis_length_words, 
                                    "thesis_length_chars": thesis_length_chars, 
                                    "publication_datetime": publication_datetime, 
                                    "article_category": category, 
                                    "number_of_views": int(number_of_views.replace(" ", "")), 
                                    "article_source": "Uznews.uz"})
    
    return article_details
    

def date_to_datetime(date):
    month_name_translation = {"января": "01",
                               "февраля": "02",
                               "марта": "03",
                               "апреля": "04",
                               "мая": "05",
                               "июня": "06",
                               "июля": "07",
                               "августа": "08",
                               "сентября": "09",
                               "октября": "10",
                               "ноября": "11",
                               "декабря": "12"}
    if "Сегодня" in date:
        return datetime.now()
    try:
        day, month, time = tuple(date.split(" "))
        publication_datetime = f"{yesterday.year}-{month_name_translation[month.strip(',')]}-{day} {time}"
        print(publication_datetime)
        publication_datetime = datetime.strptime(publication_datetime, "%Y-%m-%d %H:%M")
        return publication_datetime
    except Exception:
        return datetime.now() - timedelta(days=2)
    
uznews()
