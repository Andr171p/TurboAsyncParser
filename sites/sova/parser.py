import time

import asyncio
import threading

from bs4 import BeautifulSoup

from webdriver.driver import create_driver, get_requests

from sites.sova.html_scraping import Critical, Additional
from sites.sova.config import get_csv_file_name

from misc.utils import data_to_csv, check_empty_files


def get_soup(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    return soup


def get_paginator(driver, url):
    get_requests(driver=driver, url=url)
    time.sleep(10)
    soup = get_soup(driver=driver)
    paginator = soup.find("div", attrs={"parse-newurl": "/kupit/kommercheskaya/proiz-vo--baza--ferma"})

    return int(paginator.text.split("\n")[-3])


def parse_links(driver, url):
    get_requests(
        driver=driver,
        url=url
    )
    time.sleep(15)
    soup = get_soup(driver=driver)
    content = soup.find_all("a", attrs={"class": "pl-realty__page-link-visited"})
    links = ["https://www.sova72.ru" + link["href"] for link in content]

    return links


class SovaParser:
    def __init__(self, url):
        # sova72.ru page:
        self.url = url
        # parse with ads info:
        self.data = []
        # count of pages:
        self.paginator = None

    def task_generator(self):
        tasks = [f"{self.url}{page}" for page in range(1, self.paginator + 1)]
        return tasks

    def get_data(self, url):
        # create web-driver:
        driver = create_driver()
        # parse links:
        links = parse_links(
            driver=driver,
            url=url
        )
        # parse ads:
        for i in range(len(links)):
            get_requests(
                driver=driver,
                url=links[i]
            )
            time.sleep(5)
            soup = get_soup(driver=driver)
            # critical ads parse:
            critical = Critical(soup=soup, url_list=links)
            asyncio.run(critical.parse_html(iterator=i))
            critical_data = critical.elements
            # additional ads parse:
            additional = Additional(soup=soup)
            asyncio.run(additional.parse_html())
            additional_data = additional.elements

            # append to 2D array:
            self.data.append([*critical_data, *additional_data])

        # save page of ads in csv file:
        file_name = get_csv_file_name(url=self.url)
        directory = r"C:\Users\andre\TyuiuProjectParser\TurboAsyncParser\data\sova\pages"
        current_dir = fr"{directory}\{file_name}"
        data_to_csv(
            data=self.data,
            current_dir=current_dir,
            name_of_csv_file=file_name,
            url=url
        )

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
        file_name = get_csv_file_name(url=self.url)
        directory = r"C:\Users\andre\TyuiuProjectParser\TurboAsyncParser\data\sova\pages"
        current_dir = fr"{directory}\{file_name}"

        empty_pages = check_empty_files(
            directory=fr"{current_dir}"
        )

        tasks = [f"{self.url}{page}" for page in empty_pages]

        threads = [threading.Thread(target=self.get_data, args=(task,)) for task in tasks]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


from sites.sova.config import SOVA_URLS


parser = SovaParser(
    url=SOVA_URLS["kommercheskaya"]
)
parser.get_data("https://www.sova72.ru/kupit/uchastok/kommercheskoe?page=6")

