import json

from pathlib import Path

from loguru import logger


class JsonLoader:
    root_path = Path(__file__).resolve().parents[1]

    def __init__(
            self, data: dict, path: str, filename: str
    ) -> None:
        self.data = data
        self.path = path
        self.filename = filename

    def file_path(self) -> str:
        file_path = fr"{self.root_path}\storage\categories\{self.path}\{self.filename}.json"
        return file_path

    def json(self) -> str:
        _json = json.dumps(self.data, indent=4, ensure_ascii=False)
        return _json

    def save(self) -> None:
        _json = self.json()
        with open(
                file=self.file_path(),
                mode='w',
                encoding='utf-8'
        ) as file:
            json.dump(_json, file, ensure_ascii=False)
            logger.info("JSON ФАЙЛ УСПЕШНО СОХРАНЁН")
