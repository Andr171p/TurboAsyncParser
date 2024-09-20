import re

from settings.data import DataConsts


def all_page_urls(url: str, paginator: int) -> list:
    urls = [f"{url}{page}" for page in range(1, paginator + 1)]
    return urls


def clean_text(text: str) -> str:
    chars: set = DataConsts.BAD_CHARS
    for char in chars:
        text = text.replace(char, "")
    return text


def find_numbers(text: str) -> list:
    numbers = re.findall(r"[-+]?\d+\.\d+|\d+", text)
    return numbers


def extract_number(text: str) -> str:
    number = find_numbers(text=clean_text(text=text).replace(" ", ""))[0]
    return number


def find_cadastral_number(text: str) -> str:
    pattern = r'\b\d{2}:\d{2}:\d{7}:\d{1,3}\b'
    match = re.search(pattern, text)
    return match.group() if match else "Не указан"
