import re
import asyncio
import datetime
from datetime import date
from sites.cian.config import DATES_DICT
from utils.preprocessing_data import replace_symbol, find_numbers


class Critical:
    def __init__(self, soup, url_list):
        self.soup = soup
        self.elements = []
        self.url_list = url_list

    async def get_info(self):
        try:
            content = self.soup.find("h1", attrs={"class": "a10a3f92e9--title--vlZwT"})
            info = content.text
            self.elements.append(info)
        except Exception as _ex:
            print(f"[async def get_info()] : {_ex}")
            self.elements.append(None)

    async def get_price(self):
        content = self.soup.find_all("span", attrs={"class": "a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_5u--e6Sug a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_14px--reQMB a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5 a10a3f92e9--text_whiteSpace__nowrap--hJYYl"})
        price = find_numbers(content[1].text.replace(" ", ""))
        self.elements.append(int(price[0]))

    async def get_area(self):
        try:
            content = self.soup.find("span", attrs={"style": "letter-spacing:-0.2px"})
            area = find_numbers(replace_symbol(content.text).replace(" ", ""))
            self.elements.append(float(".".join(area)))
        except Exception as _ex:
            print(f"[async def get_area()] : {_ex}")
            self.elements.append(None)

    async def get_location(self):
        try:
            content = self.soup.find("div", attrs={"data-name": "AddressContainer"})
            location = "".join([char for char in content.text])
            self.elements.append(location)
        except Exception as _ex:
            print(f"[async def get_location()] : {_ex}")
            self.elements.append(None)

    async def get_datetime(self):
        content = self.soup.find("span", attrs={"class": "a10a3f92e9--color_gray40_100--qPi9J a10a3f92e9--lineHeight_5u--e6Sug a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_14px--reQMB a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5"})
        date_time = content.text.split()

        def str_to_time(time_string):
            time_datetime = datetime.datetime.strptime(time_string, "%H:%M").time()
            return round(float(time_datetime.hour) + float(time_datetime.minute) / 60, 2)

        def convert_to_datetime(year, month, day, time):
            date_string = f"{year}-{month}-{day} {int(time)}:{int((time - int(time)) * 60)}"
            date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M")
            return date_object

        def convert(arr):
            time = str_to_time(arr[-1])
            if arr[-2] == "сегодня,":
                today_date = date.today()
                year, month, day = today_date.year, today_date.month, today_date.day
                return convert_to_datetime(year, month, day, time)
            elif arr[-2] == "вчера,":
                today_date = date.today()
                yesterday_date = today_date - datetime.timedelta(days=1)
                yesterday_date.strftime('%Y-%m-%d')
                year, month, day = yesterday_date.year, yesterday_date.month, yesterday_date.day
                return convert_to_datetime(year, month, day, time)
            else:
                year = datetime.datetime.now().year
                number = int(arr[1])
                month = DATES_DICT[arr[2][:-1]]
                return convert_to_datetime(year, month, number, time)

        self.elements.append(convert(date_time))

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
            content = self.soup.find("li", attrs={"class": "a10a3f92e9--container--Havpv"})
            for tag in content.find_all():
                if "src" in tag.attrs:
                    self.elements.append(str(tag["src"]))
        except Exception as _ex:
            print(f"[async def get_image_link()] : {_ex}")
            self.elements.append("Не указан")

    async def get_cadastral_number(self):
        try:
            content = self.soup.find("span", attrs={"class": "a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5 a10a3f92e9--text_whiteSpace__pre-wrap--fXAax"})
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
