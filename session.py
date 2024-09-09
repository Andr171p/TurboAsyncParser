from webdriver.driver import ChromeWebDriver

from settings.page import PageConfig
from settings.logs import LogerMessages

import time

from loguru import logger


class ChromeWebDriverSession:
    page_config: str = PageConfig.ACCESS_IS_LIMITED
    timeout: int = PageConfig.ERROR_TIMEOUT
    logger_messages: LogerMessages

    def __init__(self, driver: ChromeWebDriver.driver) -> None:
        self.driver = driver

    def open(self, url: str) -> None:
        self.driver.get(url)
        if self.page_config in self.driver.title():
            time.sleep(self.timeout)
            raise Exception("Перезапуск из-за блокировки по IP...")
        logger.info(self.logger_messages.SUCCESSFUL_PAGE_LOAD)

    def close(self) -> None:
        self.driver.quit()
        self.driver.close()
