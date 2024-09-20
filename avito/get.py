from avito.source.parse.ads import HTMLADSParser


class GetADSData:
    ads = {}

    def __init__(self, dataParser: HTMLADSParser) -> None:
        self.dataParser = dataParser

    async def parse(self, url: str) -> dict:
        self.ads = {
            "info": await self.dataParser.info(),
            "price": await self.dataParser.price(),
            "area": await self.dataParser.area(),
            "location": await self.dataParser.location(),
            "datetime": await self.dataParser.datetime(),
            "image": await self.dataParser.image(),
            "cadastral": await self.dataParser.cadastral(),
            "text": await self.dataParser.text(),
            "source": await self.dataParser.source(url=url)
        }
        return self.ads