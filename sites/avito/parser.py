import os
import time
import csv
import asyncio
from bs4 import BeautifulSoup
from seleniumwire import webdriver
# from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from sites.avito.config import AVITO_URLS
import threading
from sites.avito.html_scraping import Critical, Additional
from proxies.fake_proxy import FakeProxy


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
    paginator = soup.find("li", attrs={"class": "styles-module-listItem-MKpTZ styles-module-listItem_last-RzX6e styles-module-listItem_notFirst-eZHpD"})
    return int(paginator.text)


class AvitoParser:
    def __init__(self, url, filter="svobodnogo_naznacheniya", driver_version="122.0.6261.95"):
        # avito.ru page:
        self.url = url
        # data with ads info:
        self.data = []
        # count of pages:
        self.paginator = None
        # list with filter words:
        self.filter = [filter]

    def task_generator(self):
        tasks = [f"{self.url}{page}" for page in range(1, self.paginator + 1)]
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
        links_content = page_soup.find_all("a", attrs={"data-marker": "item-title"})
        links = [f"https://www.avito.ru" + link["href"] for link in links_content if self.filter[0] not in link]
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
        try:
            name_of_csv_file = url.split("/")[6].split("-")[0]
        except IndexError:
            name_of_csv_file = "kommercheskaya"

        directory = r"C:\Users\andre\TyuiuProjectParser\TurboAsyncParser\data\avito\pages"
        current_dir = fr"{directory}\{name_of_csv_file}"

        with open(fr"{current_dir}\{name_of_csv_file}_{url[-1]}.csv",
                  mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in self.data:
                writer.writerow(row)

        print(self.data)

    def start_parse(self):
        # parse paginator:
        driver = create_driver(proxy=False)
        self.paginator = get_paginator(
            driver=driver,
            url=f"{self.url}{1}"
        )

        tasks = self.task_generator()
        threads = [threading.Thread(target=self.get_data, args=(task,)) for task in tasks]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def restart_parse(self):
        directory = r"C:\Users\andre\TyuiuProjectParser\TurboAsyncParser\data\avito\pages"

        try:
            name_of_csv_file = self.url.split("/")[6].split("-")[0]
        except IndexError:
            name_of_csv_file = "kommercheskaya"

        empty_pages = check_empty_files(
            directory=fr"{directory}\{name_of_csv_file}"
        )

        tasks = [f"{self.url}{page}" for page in empty_pages]

        threads = [threading.Thread(target=self.get_data, args=(task,)) for task in tasks]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        return empty_pages


def check_empty_files(directory):
    empty_files = []
    files = os.listdir(directory)
    for file in files:
        with open(os.path.join(directory, file),
                  mode="r", encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file)
            rows = list(csv_reader)
            if len(rows) == 0:
                empty_files.append(file.split(".")[0][-1])
            else:
                print("[+] file not empty")

    return empty_files


url_page = AVITO_URLS[1]
parser = AvitoParser(url=url_page)
parser.restart_parse()

