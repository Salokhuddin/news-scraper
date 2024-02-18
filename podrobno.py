# Scrapes the news info from podrobno.uz
# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, csv, sys, psycopg2
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys


# Calculate yesterday's date
yesterday = datetime.now().date() - timedelta(days=1)

def podrobno():


    # Declare categories
    categories = [{"url_directory": "politic", "name": "Политика"},
                {"url_directory": "economic", "name": "Экономика"},
                {"url_directory": "obchestvo", "name": "Общество"},
                {"url_directory": "proisshestviya", "name": "Происшествия"},
                {"url_directory": "tehnp", "name": "Технологии"},
                {"url_directory": "podrobno", "name": "Туризм"},
                {"url_directory": "calche", "name": "Культура"},
                {"url_directory": "sport", "name": "Спорт"},
                {"url_directory": "world", "name": "Мир"},
                {"url_directory": "uzbekistan-i-kitay-klyuchi-ot-budushchego", "name": "Узбекистан и Китай: ключи от будущего"},
                {"url_directory": "uzbekistan-i-rossiya-dialog-partnerov-", "name": "Узбекистан - Россия: диалог партнеров"},
                {"url_directory": "audio", "name": "Аудио"},
                {"url_directory": "stories", "name": "Истории"},
                {"url_directory": "releases", "name": "Пресс-релизы"},
                {"url_directory": "razbor", "name": "Разбор"},
                {"url_directory": "uzbekistan-fakty-sobytiya-litsa", "name": "Узбекистан. Факты, события, лица"}]

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
    article_urls = []
    # Open the link
    article_details = []
    for category in categories:
        driver.implicitly_wait(5)
        driver.get(f'https://podrobno.uz/cat/{category["url_directory"]}/')
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1.3)
        scroll_smoothly(driver, height=1800)
        news_cards = driver.find_elements(By.TAG_NAME, "article")
        if date_to_datetime(news_cards[1].find_element(By.CLASS_NAME, "entry-date.published.updated").text.strip()).date() >= yesterday:
            while True:
                total_height = int(driver.execute_script("return document.body.scrollHeight"))
                scroll_smoothly(driver, total_height)
                time.sleep(1.3)
                news_cards = driver.find_elements(By.TAG_NAME, "article")
                if date_to_datetime(news_cards[-1].find_element(By.CLASS_NAME, "entry-date.published.updated").text.strip()).date() < yesterday:
                    print(date_to_datetime(news_cards[-1].find_element(By.CLASS_NAME, "entry-date.published.updated").text.strip()).date())
                    break
                show_more(driver, actions)
            for card in news_cards:
                publication_date = date_to_datetime(card.find_element(By.CLASS_NAME, "entry-date.published.updated").text.strip())
                if publication_date.date() == yesterday:
                    article_url = card.find_element(By.CLASS_NAME, "post-title.entry-title a").get_attribute("href")
                    article_headline = card.find_element(By.CLASS_NAME, "post-title.entry-title").text.strip()
                    number_of_views = card.find_element(By.CLASS_NAME, "post-read-time").text.strip()
                    article_details.append({"article_url": article_url, 
                                            "headline": article_headline, 
                                            "publication_datetime": publication_date, 
                                            "article_category": category["name"], 
                                            "number_of_views": int(number_of_views.replace(" ", "")), 
                                            "article_source": "Podrobno.uz"})
    
    return article_details


def scroll_smoothly(driver, height):
    
    for i in range(1, height, 5):
        driver.execute_script("window.scrollTo(0, {});".format(i))

def show_more(driver, actions):
    load_more_button = driver.find_element(By.CLASS_NAME, "btn.btn-load-more.js-btn-load-more")  
    facebook_button = driver.find_element(By.CLASS_NAME, "a-facebook.have-description")    
    driver.execute_script("arguments[0].scrollIntoView(true);", facebook_button)
    time.sleep(2.3)
    load_more_button.click()
    time.sleep(3)

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
        day, month, year, time = tuple(date.split(" "))
        publication_datetime = f"{year.strip(',')}-{month_name_translation[month]}-{day} {time}"
        publication_datetime = datetime.strptime(publication_datetime, "%Y-%m-%d %H:%M")
        return publication_datetime
    except Exception as e:
        return datetime.now() - timedelta(days=2)


podrobno()