import os
import time
import csv
import asyncio
import threading
from bs4 import BeautifulSoup
from seleniumwire import webdriver
# from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from proxies.fake_proxy import FakeProxy
from sites.cian.config import ADDRESS, REGION
from sites.cian.html_scraping import Critical, Additional


def create_driver(proxy=False):
    # Chrome driver options:
    options = webdriver.ChromeOptions()
    # fake User-agent:
    user_agent = UserAgent().random
    # add options user-agent:
    options.add_argument(f"user-agent={user_agent}")
    # Chrome web-driver:
    if not proxy:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options, seleniumwire_options=FakeProxy().get_fake_proxy())

    return driver


def get_requests(driver, url):
    driver.get(url)
    driver.implicitly_wait(10)


def get_paginator(driver, url):
    get_requests(driver=driver, url=url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    paginator = soup.find("ul", attrs={"class": "_32bbee5fda--list--G2FoV"})

    return int(paginator.text[-1])


class CianParser:
    def __init__(self, address=ADDRESS, region=REGION):
        # address and region of url cian.ru:
        self.address = address
        self.region = REGION
        # data with ads info:
        self.data = []
        # count of pages:
        self.paginator = None

    def task_generator(self):
        tasks = [f"{self.address}{page}{self.region}" for page in range(1, self.paginator + 1)]
        return tasks

    def get_data(self, url):
        # create web-driver:
        driver = create_driver(proxy=False)
        # parse links with ads:
        get_requests(driver=driver, url=url)
        time.sleep(15)
        page_html = driver.page_source
        page_soup = BeautifulSoup(page_html, "html.parser")
        # parse links:
        links_content = page_soup.find_all("a", attrs={"data-name": "CommercialTitle"})
        links = [link["href"] for link in links_content]
        # parse ads:
        for i in range(len(links)):
            get_requests(driver=driver, url=links[i])
            time.sleep(5)
            ads_html = driver.page_source
            ads_soup = BeautifulSoup(ads_html, "html.parser")
            # critical ads data:
            critical = Critical(soup=ads_soup, url_list=links)
            asyncio.run(critical.parse_html(iterator=i))
            critical_data = critical.elements
            # additional ads data:
            additional = Additional(soup=ads_soup)
            asyncio.run(additional.parse_html())
            additional_data = additional.elements

            # append to 2D array:
            self.data.append([*critical_data, *additional_data])

        # save page ads to csv file:
        name_of_csv_file = "kommercheskaya"
        directory = r"C:\Users\andre\TyuiuProjectParser\TurboAsyncParser\data\cian\pages"
        current_dir = fr"{directory}\{name_of_csv_file}"

        with open(fr"{current_dir}_{url[-13]}.csv",
                  mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in self.data:
                writer.writerow(row)

        print(self.data)

    def start_parse(self):
        # create driver:
        driver = create_driver(proxy=False)
        # parse paginator:
        self.paginator = get_paginator(
            driver=driver,
            url=f"{self.address}{1}{self.region}"
        )

        tasks = self.task_generator()
        threads = [threading.Thread(target=self.get_data, args=(task,)) for task in tasks]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


parser = CianParser()
parser.start_parse()

