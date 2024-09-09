from avito.source.html import HTMLSource

from settings.logs import LogerMessages
from settings.network import NetworkConfig

from utils import (
    clean_text,
    extract_number,
    find_cadastral_number
)


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

    async def image(self) -> list:
        urls = []
        try:
            html = self.soup.find(
                name="div",
                attrs={
                    "data-marker": "image-frame/image-wrapper"
                }
            )
            for tag in html.find_all():
                if "src" in tag.attrs:
                    urls.append(str(tag["src"]))
            return urls
        except Exception as _ex:
            self.logger.warning(_ex)
            self.logger.warning(LogerMessages.NOT_ACTUAL_ADS)
            empty = []
            return empty

    async def cadastral(self) -> str:
        html = self.soup.find(
            name="div",
            attrs={
                "data-marker": "item-view/item-description"
            }
        )
        text = clean_text(text=html.text)
        cadastral = find_cadastral_number(text=text)
        return cadastral

    async def text(self) -> str:
        html = self.soup.find(
            name="div",
            attrs={
                "data-marker": "item-view/item-description"
            }
        )
        text = clean_text(text=html.text)
        return text

    @staticmethod
    async def source(url: str) -> list:
        source = [url, NetworkConfig.SOURCE_NAME]
        return source
