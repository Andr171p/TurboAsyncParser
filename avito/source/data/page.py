from avito.source.html import HTMLSource

from settings.network import NetworkConfig


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
