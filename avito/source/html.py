from bs4 import BeautifulSoup

from webdriver.driver import ChromeWebDriver


class HTMLSource:
    from loguru import logger

    def __init__(
            self, driver: ChromeWebDriver.driver
    ) -> None:
        self.html = driver.page_source
        self.soup = BeautifulSoup(
            self.html,
            "html.parser"
        )
