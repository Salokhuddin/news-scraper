import pandas as pd
from kunuz import kun_uz
from qalampir import qalampir
from daryo import daryo
from gazeta import gazeta
from podrobno import podrobno
from uznews import uznews
from itertools import chain
from selenium import webdriver
from datetime import datetime

def collect_news():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # Open the browser
    print('Opening browser')
    driver = webdriver.Chrome(options=options)
    print('Opened browser')
    # Maximize the browser to fullscreen
    driver.maximize_window()
    print('Maxed browser')
    # [uznews, podrobno, qalampir, daryo, kun_uz, gazeta]
    article_details = []
    for publisher in [qalampir]:
        article_details.append(collect(publisher, driver))
    article_details = list(chain.from_iterable(article_details))
    articles = pd.DataFrame(article_details)
    articles.to_csv("articles.csv", index=False)
    driver.close()

def collect(func, driver):
    return func(driver)