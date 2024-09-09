from bs4 import BeautifulSoup

from webdriver.driver import ChromeWebDriver

from settings.network import NetworkConfig
from settings.logs import LogerMessages

from utils import (
    clean_text,
    find_numbers,
    extract_number
)


class HTMLSource:
    from loguru import logger

    def __init__(
            self, driver: ChromeWebDriver.driver
    ) -> None:
        self.html = driver.page_source
        self.soup = BeautifulSoup(
            self.html,
            "html.parser"
        )


class HTMLPageParser(HTMLSource):
    def paginator(self) -> int:
        paginator = self.soup.find(
            name="li",
            attrs={
                "class": "styles-module-listItem-MKpTZ styles-module-listItem_last-RzX6e styles-module-listItem_notFirst-eZHpD"
            }
        )
        count = int(paginator.text)
        return count

    def urls(self) -> list:
        html = self.soup.find_all(
            name="a",
            attrs={
                "data-marker": "item-title"
            }
        )
        urls = [
            f"{NetworkConfig.AVITO_URL}" + url["href"] for url in html
        ]
        return urls


class HTMLDataParser(HTMLSource):
    async def info(self) -> str:
        try:
            html = self.soup.find(
                name="h1",
                attrs={
                    "data-marker": "item-view/title-info"
                }
            )
            info = html.text
            return info
        except Exception as _ex:
            self.logger.warning(_ex)
            return "Не указан"

    async def price(self) -> int:
        html = self.soup.find(
            name="div",
            attrs={
                "class": "style-item-price-sub-price-_5RUD"
            }
        )
        price = int(extract_number(text=html.text))
        return price

    async def area(self) -> float:
        try:
            try:
                html = self.soup.find(
                    name="li",
                    attrs={
                        "class": "params-paramsList__item-_2Y2O"
                    }
                )
                area = float(extract_number(text=html.text))
            except Exception as _ex:
                self.logger.info(_ex)
                html = self.soup.find(
                    name="ul",
                    attrs={
                        "class": "params-paramsList-_awNW"
                    }
                )
                area = float(extract_number(text=html[0].text))
            return area
        except Exception as _ex:
            self.logger.warning(_ex)
            self.logger.info(LogerMessages.NOT_ACTUAL_ADS)
            return 0

    async def location(self) -> str:
        try:
            html = self.soup.find(
                name="span",
                attrs={
                    "class": "style-item-address__string-wt61A"
                }
            )
            location = clean_text(text=html.text)
            return location
        except Exception as _ex:
            self.logger.warning(_ex)
            return "Не указан"

    async def datetime(self) -> str:
        try:
            html = self.soup.find(
                name="span",
                attrs={
                    "data-marker": "item-view/item-date"
                }
            )
            datetime = html.text
            return datetime
        except Exception as _ex:
            self.logger.warning(_ex)
            return "Не указан"
