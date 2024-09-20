import json

from pathlib import Path

from loguru import logger


class JsonReader:
    root_path = Path(__file__).resolve().parents[1]

    def __init__(self, path: str, filename: str) -> None:
        self.path = path
        self.filename = filename

    def __file_path(self) -> str:
        file_path = fr"{self.root_path}\storage\categories\{self.path}\{self.filename}.json"
        return file_path

    @staticmethod
    def __dict(_json: str) -> dict:
        _dict = json.loads(_json)
        return _dict

    def read(self) -> dict:
        with open(
            file=self.__file_path(),
            mode='r',
            encoding='utf-8'
        ) as file:
            _json = json.load(file)
            _dict = self.__dict(_json=_json)
            logger.info("ДАННЫЕ УСПЕШНО ПОЛУЧЕНЫ ИЗ JSON ФАЙЛА")
            return _dict
