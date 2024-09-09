import re
import asyncio
from datetime import date
from utils.preprocessing_data import find_numbers, replace_symbol


class Critical:
    def __init__(self, soup, url_list):
        self.soup = soup
        self.elements = []
        self.url_list = url_list

    async def get_info(self):
        try:
            content = self.soup.find("h1", attrs={"class": "pl-realty__page-header"})
            info = content.text
            self.elements.append(info)
        except Exception as _ex:
            print(_ex)
            self.elements.append(None)

    async def get_price(self):
        content = self.soup.find("div", attrs={"class": "pl-realty-search__item-price-kv"})
        price = find_numbers(replace_symbol(content.text).replace(" ", ""))
        self.elements.append(int(price[0]))

    async def get_area(self):
        content = self.soup.find_all("div", attrs={"class": "pl-realty__page-attributes-value"})
        area = find_numbers(content[1].text)[0]
        self.elements.append(float(area))

    async def get_location(self):
        content = self.soup.find("h1", attrs={"class": "pl-realty__page-header"})
        location = content.text.split(",")[2:]
        self.elements.append(" ".join(location))

    async def get_datetime(self):
        self.elements.append(date.today())

    async def get_url(self, iterator):
        self.elements.append(self.url_list[iterator])
        self.elements.append("sova")

    async def parse_html(self, iterator):
        await asyncio.gather(
            self.get_info(),
            self.get_price(),
            self.get_area(),
            self.get_location(),
            self.get_datetime(),
            self.get_url(iterator=iterator)
        )

        return self.elements


class Additional:
    def __init__(self, soup):
        self.soup = soup
        self.elements = []

    async def get_image_link(self):
        content = self.soup.find("li", attrs={"data-slidetype": "image"})
        for tag in content.find_all():
            if "src" in tag.attrs:
                self.elements.append(str(tag["src"]))

    async def get_cadastral_number(self):
        try:
            content = self.soup.find("p")
            description = replace_symbol(content.text)

            def check_number(text):
                pattern = r'\b\d{2}:\d{2}:\d{7}:\d{1,3}\b'
                match = re.search(pattern, text)
                if match:
                    return match.group()
                else:
                    return "Не указан"

            cadastral_number = check_number(text=description)
            self.elements.append(cadastral_number)
        except Exception as _ex:
            print(_ex)
            self.elements.append("Не указан")

    async def parse_html(self):
        await asyncio.gather(
            self.get_cadastral_number(),
            self.get_image_link()
        )

        return self.elements

