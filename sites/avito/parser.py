import time
import csv
import asyncio
from bs4 import BeautifulSoup
import threading
from sites.avito.config import filter
from sites.avito.html_scraping import Critical, Additional
from webdriver.driver import create_driver, get_requests
from misc.utils import check_empty_files

from sites.avito.config import AVITO_URLS


def get_paginator(driver, url):
    get_requests(driver=driver, url=url)
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    paginator = soup.find("li", attrs={"class": "styles-module-listItem-MKpTZ styles-module-listItem_last-RzX6e styles-module-listItem_notFirst-eZHpD"})
    return int(paginator.text)


class AvitoParser:
    def __init__(self, url):
        # avito.ru page:
        self.url = url
        # parse with ads info:
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
        driver = create_driver()
        # parse links with ads:
        get_requests(driver=driver, url=url)
        time.sleep(15)
        page_html = driver.page_source
        page_soup = BeautifulSoup(page_html, "html.parser")
        # parse links:
        links_content = page_soup.find_all("a", attrs={"parse-marker": "item-title"})
        links = [f"https://www.avito.ru" + link["href"] for link in links_content if self.filter not in link]
        # parse ads:
        for i in range(len(links)):
            get_requests(driver=driver, url=links[i])
            time.sleep(5)
            ads_html = driver.page_source
            ads_soup = BeautifulSoup(ads_html, "html.parser")
            # critical ads parse:
            critical = Critical(soup=ads_soup, url_list=links)
            asyncio.run(critical.parse_html(iterator=i))
            critical_data = critical.elements
            # additional ads parse:
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
        driver = create_driver()
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


url_page = AVITO_URLS["kommercheskaya"]
parser = AvitoParser(url=url_page)
parser.start_parse()

