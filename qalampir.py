# Scrapes the news info from qalampir.uz
# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, csv, sys, psycopg2
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta



def qalampir():
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
    driver.get("https://www.qalampir.uz/latest")

    # Collect info
    show_more(driver, actions)
    news_cards = driver.find_elements(By.CLASS_NAME, "news-card")
    article_urls = []
    for card in news_cards:
        article_publication_date = card.find_element(By.CLASS_NAME, "date").text
        print(article_publication_date)
        if len(article_publication_date.split()) > 1:
            article_publication_date = convert_to_datetime(article_publication_date)
            if article_publication_date.day == yesterday.day:
                article_url = card.get_attribute("href")
                article_urls.append({"article_url": article_url,
                                    "article_publication_date": article_publication_date})
                print(len(article_urls))

    return collect_article_details(driver, article_urls)

def collect_article_details(driver, article_urls):
    article_details = []
    for article in article_urls:
        driver.get(article["article_url"])
        article_headline = driver.find_element(By.CLASS_NAME, "title").text
        number_of_views = driver.find_element(By.CLASS_NAME, "right").text.split("\n")[-1]
        category = driver.find_element(By.CLASS_NAME, "left").text
        article_details.append({"article_url": article["article_url"], 
                                "headline": article_headline, 
                                "publication_datetime": article["article_publication_date"], 
                                "article_category": category, 
                                "number_of_views": number_of_views, 
                                "article_source": "Qalampir.uz"})
        
    return article_details


def show_more(driver, actions):
    for i in range(1):
        load_more_button = driver.find_element(By.CLASS_NAME, "refresh-btn")       
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        time.sleep(1.3)
        load_more_button.click()
        # actions.move_to_element(load_more_button).perform()
        # time.sleep(2)
        time.sleep(3)

    

def convert_to_datetime(date):

    month_name_translation = {"Январь": "January",
                               "Февраль": "February",
                               "Март": "March",
                               "Апрель": "April",
                               "Май": "May",
                               "Июнь": "June",
                               "Июль": "July",
                               "Август": "August",
                               "Сентябрь": "September",
                               "Октябрь": "October",
                               "Ноябрь": "November",
                               "Декабрь": "December"}
    date_parts = date.split()
    date_month = month_name_translation[date_parts[1].capitalize()]
    current_year = datetime.now().year
    full_date = f"{date_parts[0]} {date_month} {current_year}"
    return datetime.strptime(full_date, "%d %B %Y")

qalampir()