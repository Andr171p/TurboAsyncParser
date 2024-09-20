from typing import List


def page_urls_dict(urls: List[str]) -> dict:
    data = {
        'urls': urls
    }
    return data


def ads_data_dict(ads: List[dict]) -> dict:
    data = {
        'data': ads
    }
    return data
