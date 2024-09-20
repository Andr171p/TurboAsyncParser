# import undetected_chromedriver as uc

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager


class ChromeWebDriver:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
