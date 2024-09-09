import time
from utils.preprocessing_data import check_empty_files
from sites.avito.config import AVITO_URLS
from sites.cian.config import CIAN_URL
from sites.sova.config import SOVA_URLS


def set_timer(hours, minutes, seconds):
    total = hours * 3600 + minutes * 60 + seconds
    time.sleep(total)


def check_restart(directory):
    num_of_file = check_empty_files(
        directory=directory
    )
    if len(num_of_file) != 0:
        return True
    else:
        return False


class SetParser:
    def __init__(self, source, restart):
        def get_urls(site_source):
            urls_dict = {
                "avito": list(AVITO_URLS.values()),
                "cian": [CIAN_URL],
                "sova": list(SOVA_URLS.values())
            }
            return urls_dict[site_source]

        self.source = source
        self.urls = get_urls(site_source=source)
        self.restart = restart

    def run(self):
        match self.source:
            case "avito":
                from sites.avito.parser import AvitoParser
                pass
            case "cian":
                from sites.cian.parser import CianParser
                pass
            case "sova":
                from sites.sova.parser import SovaParser

                for url in self.urls:
                    parser = SovaParser(url=url)
                    if self.restart:
                        parser.restart_parse()
                    else:
                        parser.start_parse()


parser = SetParser(
    source="sova",
    restart=False
)
parser.run()
