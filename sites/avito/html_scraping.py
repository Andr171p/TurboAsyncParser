from utils.preprocessing_data import replace_symbol, find_numbers
from utils.parse_dates import DatetimeConverter
from datetime import date
import re
import asyncio


class Critical:
    def __init__(self, soup, url_list):
        self.soup = soup
        self.elements = []
        self.url_list = url_list

    # this function return info of sector --> str:
    async def get_info(self):
        try:
            content = self.soup.find("h1", attrs={"data-marker": "item-view/title-info"})
            info = replace_symbol(content.text)
            self.elements.append(info)
        except Exception as _ex:
            print(_ex)
            self.elements.append(None)

    # this function return price per m^2 of sector --> int:
    async def get_price(self):
        content = self.soup.find("div", attrs={"class": "style-item-price-sub-price-_5RUD"})
        price = find_numbers(replace_symbol(content.text).replace(" ", ""))
        self.elements.append(int(price[0]))

    # this function return area of sector --> float:
    async def get_area(self):
        try:
            try:
                content = self.soup.find("li", attrs={"class": "params-paramsList__item-_2Y2O"})
                area = find_numbers(replace_symbol(content.text).replace(" ", ""))[0]
            except Exception as _ex:
                print(_ex)
                content = self.soup.find_all("ul", attrs={"class": "params-paramsList-_awNW"})
                area = find_numbers(content[0].text)[0]

            self.elements.append(float(area))
        except Exception as _ex:
            print(f"Объявдение снято с публикации: {_ex}")
            self.elements.append(None)

    # this function return location of sector --> str:
    async def get_location(self):
        try:
            content = self.soup.find("span", attrs={"class": "style-item-address__string-wt61A"})
            location = replace_symbol(content.text)
            self.elements.append(location)
        except Exception as _ex:
            print(f"Объявдение снято с публикации: {_ex}")
            self.elements.append(None)

    # this function return datetime of ads --> datetime object:
    async def get_datetime(self):
        converter = DatetimeConverter()
        try:
            content = self.soup.find("span", attrs={"data-marker": "item-view/item-date"})
            date_time = content.text
            self.elements.append(converter.current_date(date_time))
        except Exception as _ex:
            print(f"[WARNING] : {_ex}")
            self.elements.append(date.today())

    async def get_url(self, iterator):
        self.elements.append(self.url_list[iterator])

        if "avito" in self.url_list[iterator]:
            self.elements.append("avito")
        else:
            self.elements.append("cian")

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
        try:
            # links_collection = set()
            content = self.soup.find("div", attrs={"data-marker": "image-frame/image-wrapper"})
            for tag in content.find_all():
                # if "data-url" in tag.attrs:
                    # links_collection.add(tag["data-url"])
                if "src" in tag.attrs:
                    self.elements.append(str(tag["src"]))

            # self.elements.append(links_collection)

            return self.elements
        except Exception as _ex:
            print(f"Объявдение снято с публикации: {_ex}")

    async def get_cadastral_number(self):
        try:
            content = self.soup.find("div", attrs={"data-marker": "item-view/item-description"})
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
            return description
        except Exception as _ex:
            print(f"Не указан кадастровый номер: {_ex}")

    async def parse_html(self):
        await asyncio.gather(
            self.get_cadastral_number(),
            self.get_image_link()
        )

        return self.elements

