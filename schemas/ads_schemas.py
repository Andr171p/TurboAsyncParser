from pydantic import BaseModel


class ADSSchema(BaseModel):
    info: str
    price: int
    area: float
    location: str
    datetime: str
    image: list
    cadastral: str
    source: list
