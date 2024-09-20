from bs4 import BeautifulSoup

from webdriver.driver import ChromeWebDriver


class HTMLSource:
    def __init__(
            self, driver: ChromeWebDriver.driver
    ) -> None:
        self.element = driver.find_element("xpath", "//*")
        self.html = self.element.get_attribute("outerHTML")
        self.soup = BeautifulSoup(
            self.html,
            "html.parser"
        )
