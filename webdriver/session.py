from webdriver.driver import ChromeWebDriver

from settings.page import PageConfig
from settings.logs import LogerMessages

import time

from loguru import logger


class ChromeWebDriverSession(ChromeWebDriver):
    page_config = PageConfig.ACCESS_IS_LIMITED
    timeout = PageConfig.ERROR_TIMEOUT

    def open(self, url: str) -> None:
        self.driver.get(url)
        time.sleep(10)
        if self.page_config in self.driver.title:
            time.sleep(self.timeout)
            raise Exception("Перезапуск из-за блокировки по IP...")
        logger.info(LogerMessages.SUCCESSFUL_PAGE_LOAD)

    def close(self) -> None:
        self.driver.close()
        self.driver.quit()

