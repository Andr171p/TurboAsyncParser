from bs4 import BeautifulSoup
from seleniumwire import webdriver
# from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
import datetime
from datetime import date
from utils.preprocessing_data import find_numbers, replace_symbol


def create_driver(proxy=False):
    # Chrome driver options:
    options = webdriver.ChromeOptions()
    # fake User-agent:
    user_agent = UserAgent().random
    # add options user-agent:
    options.add_argument(f"user-agent={user_agent}")
    # Chrome web-driver:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver


'''driver = create_driver()
driver.get("https://tyumen.cian.ru/sale/commercial/301637654/")
driver.implicitly_wait(10)
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

content = soup.find("span", attrs={"style": "letter-spacing:-0.2px"})
area = find_numbers(replace_symbol(content.text).replace(" ", ""))'''
area = ['1', '9']
print(float(".".join(area)))





