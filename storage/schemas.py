from pydantic import BaseModel

from typing import List


class PageUrlsSchema(BaseModel):
    urls: List[str]


class ADSDataSchema(BaseModel):
    info: str
    price: int
    area: float
    location: str
    datetime: str
    image: List[str] | list
    cadastral: str
    text: str
    source: List[str]


class ADSJsonSchema(BaseModel):
    data: List[ADSDataSchema]
