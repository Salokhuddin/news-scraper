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
    driver.get("https://daryo.uz/k/yangiliklar")

    # Collect info
    ### Load more 
    show_more(driver, actions)

    time.sleep(1)
    news_cards = driver.find_elements(By.CLASS_NAME, "l-post.grid-post.grid-base-post.mini__article")
    article_urls = []
    for card in news_cards:
        if "КЕЧА" in card.find_element(By.CLASS_NAME, "post-date").text:
            article_url = card.find_element(By.CSS_SELECTOR, ".is-title.post-title a").get_attribute("href")
            publication_date = convert_to_datetime(card.find_element(By.CLASS_NAME, "post-date").text.strip())
            article_urls.append({"article_url": article_url,
                                "publication_datetime": publication_date})


    return collect_article_details(driver, article_urls)

def collect_article_details(driver, article_urls):
    article_details = []
    for article in article_urls:
        driver.get(article["article_url"])
        article_headline = driver.find_element(By.CLASS_NAME, "is-title.post-title").text.strip()
        article_thesis = driver.find_element(By.CLASS_NAME, 
                                             "post-content.post-content-custom.cf.entry-content.content-spacious.default__section.border.post-content-voice").find_element(By.TAG_NAME, "p").text.strip()
        thesis_length_words = len(article_thesis.split())
        thesis_length_chars = len(article_thesis.replace(" ", ""))
        number_of_views = driver.find_element(By.CLASS_NAME, "meta-item.post-views.has-icon.rank-hot").text.strip()
        category = driver.find_element(By.CLASS_NAME, "meta-item.cat-labels a").text.strip()
        article_details.append({"article_url": article["article_url"], 
                                "headline": article_headline, 
                                "thesis_length_words": thesis_length_words, 
                                "thesis_length_chars": thesis_length_chars, 
                                "publication_datetime": article["publication_datetime"], 
                                "article_category": category, 
                                "number_of_views": number_of_views, 
                                "article_source": "Daryo.uz"})

    return article_details
        

def show_more(driver, actions):
    for i in range(3):
        load_more_button = driver.find_element(By.ID, "load-more")       
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
        time.sleep(1.3)
        load_more_button.click()
        # actions.move_to_element(load_more_button).perform()
        # time.sleep(2)
        time.sleep(3)
    
def convert_to_datetime(date):
    publication_time = date.split(", ")[1]
    publication_date = str(datetime.now() - timedelta(days=1)).split()[0]
    publication_datetime = f"{publication_date} {publication_time}"
    return datetime.strptime(publication_datetime, "%Y-%m-%d %H:%M")

daryo()