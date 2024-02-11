# Scrapes the news info from kun.uz
# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, csv, sys, psycopg2
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta



def kun_uz():
    # Calculate yesterday's date
    yesterday = datetime.now().date() - timedelta(days=1)

    # Yesterday's first second (00:00:00)
    f = datetime.combine(yesterday, datetime.min.time())
    f = int(f.timestamp())

    # Yesterday's last second (23:59:59)
    next = datetime.combine(yesterday, datetime.max.time())
    next = int(next.timestamp())

    # Declare categories
    categories = [{"url_directory": "uzbekiston", "name": "ЎЗБЕКИСТОН"},
                {"url_directory": "jahon", "name": "ЖАҲОН"},
                {"url_directory": "iktisodiet", "name": "ИҚТИСОДИЁТ"},
                {"url_directory": "jamiyat", "name": "ЖАМИЯТ"},
                {"url_directory": "tehnologia", "name": "ФАН-ТЕХНИКА"},
                {"url_directory": "sport", "name": "СПОРТ"},
                {"url_directory": "nuqtai-nazar", "name": "НУҚТАЙИ НАЗАР"}]
    
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
    articles = []
    # Open the link
    for category in categories:
        driver.implicitly_wait(10)
        driver.get(f'https://kun.uz/news/category/{category["url_directory"]}?f={f}&next={next}')

        # Collect articles URLs
        news_cards = driver.find_elements(By.CLASS_NAME, "col-md-4.mb-25.l-item")
        for card in news_cards:
            publication_date = card.find_element(By.CLASS_NAME, "news-meta").text.strip()
            # Parse the string into a datetime object
            publication_date = datetime.strptime(publication_date, "%H:%M / %d.%m.%Y")

            # Convert datetime object to a Unix timestamp
            publication_date_timestamp = int(publication_date.timestamp())

            # Save article url and publication date 
            if publication_date_timestamp >= f:
                article_url = card.find_element(By.CLASS_NAME, "news__title").get_attribute("href")
                articles.append({"article_category": category["name"],
                                 "publication_datetime": publication_date,
                                 "article_url": article_url})
    save(articles)
    article_details = []
    for article in articles:
        driver.get(article["article_url"])
        article_headline = driver.find_element(By.CLASS_NAME, "single-header__title").text
        article_thesis = driver.find_element(By.CLASS_NAME, "single-content").find_element(By.XPATH, "*[1]").text
        thesis_length_words = len(article_thesis.split())
        thesis_length_chars = len(article_thesis.replace(" ", ""))
        number_of_views = driver.find_element(By.CLASS_NAME, "view").text
        article_details.append({"article_url": article["article_url"], 
                                "headline": article_headline, 
                                "thesis_length_words": thesis_length_words, 
                                "thesis_length_chars": thesis_length_chars, 
                                "publication_datetime": article["publication_datetime"], 
                                "article_category": article["article_category"], 
                                "number_of_views": number_of_views, 
                                "article_source": "Kun.uz"})
        
    return article_details
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(3)
        # driver.find_element(By.CLASS_NAME, "load-more__link").click()
        # time.sleep(3)
        # Execute JavaScript to scroll the element into view
        # actions.move_to_element(load_more_button).perform()        
        # load_more_button.click()


def save(articles):
    with open('article_urls.csv', 'a') as file:
        writer = csv.DictWriter(file, fieldnames=["article_url", "article_category", "publication_datetime"])
        writer.writeheader()
        for article in articles:
            writer.writerow({"article_url": article["article_url"],
                             "article_category": article["article_category"], 
                             "publication_datetime": article["publication_datetime"]})



kun_uz()