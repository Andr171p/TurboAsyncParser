SOVA_URLS = {
    "uchastok": "https://www.sova72.ru/kupit/uchastok/kommercheskoe?page=",
    "kommercheskaya": "https://www.sova72.ru/kupit/kommercheskaya/proiz-vo--baza--ferma?page=",
}


def get_csv_file_name(url):
    if url == SOVA_URLS["uchastok"]:
        return "uchastok"
    elif url == SOVA_URLS["kommercheskaya"]:
        return "kommercheskaya"

