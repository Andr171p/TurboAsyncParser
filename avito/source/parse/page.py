from avito.source.html import HTMLSource
from avito.config import AvitoMainURLS

from settings.network import NetworkConfig


from typing import List


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

    @staticmethod
    def pages_urls(paginator: int) -> List[str]:
        avito_page_url = AvitoMainURLS.AVITO_URL_TEMPLATE
        urls = [
            avito_page_url + str(num) for num in range(1, paginator + 1)
        ]
        return urls

    def ads_urls(self) -> List[str]:
        print(self.soup)
        html = self.soup.find_all(
            name="a",
            attrs={
                "data-marker": "item-title"
            }
        )
        print(html)
        urls = [
            f"{NetworkConfig.AVITO_URL}" + url["href"] for url in html
        ]
        return urls
