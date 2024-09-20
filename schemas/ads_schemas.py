from pydantic import BaseModel

from typing import List


class ADSSchema(BaseModel):
    info: str
    price: int
    area: float
    location: str
    datetime: str
    image: List[str]
    cadastral: str
    source: List[str]
