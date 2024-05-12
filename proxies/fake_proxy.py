import random
from proxies.proxy_auth import login, password, ip_port


class FakeProxy:
    def __init__(self):
        self.__login = login
        self.__password = password
        self.__ip_port = ip_port

    def __random_proxy(self):
        return random.choice(self.__ip_port)

    def get_fake_proxy(self):
        proxy = {
            "proxy": {
                "https": f"https://{self.__login}:{self.__password}@{self.__random_proxy()}"
            }
        }
        return proxy

