from avito.source.parse.page import HTMLPageParser
from avito.source.parse.ads import HTMLADSParser
from avito.get import GetADSData

from webdriver.session import ChromeWebDriverSession

from storage.loader import JsonLoader
from storage.reader import JsonReader
from storage.tamplates import (
    page_urls_dict,
    ads_data_dict
)

from loguru import logger
from typing import List


class URLPageParser:
    session = ChromeWebDriverSession()

    def __init__(
            self, url: str, exists_path: str, filename: str
    ) -> None:
        self.url = url
        self.exists_path = exists_path
        self.filename = filename

    def urls(self) -> None:
        self.session.open(url=self.url)
        page_parser = HTMLPageParser(driver=self.session.driver)
        paginator = page_parser.paginator()
        urls = page_parser.pages_urls(paginator=paginator)
        self.session.close()
        data = page_urls_dict(urls=urls)
        logger.info("ССЫЛКИ СТРАНИЦ УСПЕШНО ПОЛУЧЕНЫ!")
        logger.info(data)
        JsonLoader(
            data=data,
            path=self.exists_path,
            filename=self.filename
        ).save()


class ADSParser:
    session = ChromeWebDriverSession()

    @classmethod
    def urls(cls, url: str) -> List[str]:
        cls.session.open(url=url)
        urls = HTMLPageParser(driver=cls.session.driver).ads_urls()
        # cls.session.close()
        return urls

    @classmethod
    async def data(cls, url: str) -> dict:
        cls.session.open(url=url)
        ads_parser = HTMLADSParser(driver=cls.session.driver)
        data = await GetADSData(dataParser=ads_parser).parse(url=url)
        # cls.session.close()
        return data


class AvitoParser:
    from avito.config import (
        AvitoMainURLS,
        AvitoCategories
    )

    def __init__(self, category_name: str) -> None:
        self.category_name = category_name
        self.category_url = self.AvitoCategories.CATEGORIES[self.category_name]
        logger.info("AVITO PARSER ГОТОВ К РАБОТЕ...")

    def get_pages_urls(self) -> None:
        URLPageParser(
            url=self.AvitoMainURLS.AVITO_URL_TEMPLATE,
            exists_path=self.category_name,
            filename='urls'
        ).urls()

    def get_ads_urls(self) -> List[str]:
        urls = ADSParser.urls(url=self.category_url)
        return urls

    async def get_ads_data(self) -> None:
        data = []
        urls = self.get_ads_urls()
        logger.info(f"ОБЪЯВЛЕНИЯ НА СТРАНИЦЕ: {urls}")
        for url in urls:
            logger.info(f"ОТКРЫТА СТРАНИЦА: {url}")
            ads = await ADSParser.data(url=url)
            data.append(ads)
        logger.info(f"ДАННЫЕ УСПЕШНО ПОЛУЧЕНЫ: {data}")
        JsonLoader(
            data=ads_data_dict(ads=data),
            path=self.category_name,
            filename='data_3'
        ).save()
        logger.info("ДАННЫЕ УСПЕШНО СОХРАНЕНЫ")


import asyncio

avito = AvitoParser(category_name='land_plots')
asyncio.run(avito.get_ads_data())
