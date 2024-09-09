from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from fake_useragent import UserAgent


class ChromeWebDriver:
    options = webdriver.ChromeOptions()
    user_agent = UserAgent().random
    options.add_argument(f"user-agent={user_agent}")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    @classmethod
    def request(cls, url, timeout) -> None:
        cls.driver.get(url=url)
        cls.driver.implicitly_wait(time_to_wait=timeout)
