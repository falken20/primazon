# by Richi Rod AKA @richionline / falken20

import sys
import os
import re
import requests
import json
from selectorlib import Extractor
from bs4 import BeautifulSoup

from src.utils_logs import loggear

# Load .env file
# load_dotenv(find_dotenv())


headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36' +
    '(KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,' +
    'image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


def get_proxies():
    """
    Get list proxies to access amazon web and avoid blocked access

    Returns:
        set: List of free proxies
    """
    try:
        loggear("Method get_proxies to get free proxies...", "INFO")

        url = 'https://free-proxy-list.net/'
        headers_proxy = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36' +
            '(KHTML, like Gecko) Cafari/537.36'}

        source = str(requests.get(url, headers=headers_proxy, timeout=10).text)
        data = [list(filter(None, i))[0] for i in re.findall(
            '<td class="hm">(.*?)</td>|<td>(.*?)</td>', source)]

        groupings = [dict(zip(['ip', 'port', 'code', 'using_anonymous'], data[i:i+4]))
                     for i in range(0, len(data), 4)]

        # proxies = [{'full_ip':"{ip}:{port}".format(**i)} for i in groupings]
        proxies = ["{ip}:{port}".format(**i) for i in groupings]

        return proxies
    except Exception as err:
        loggear("Error in get_proxies method:", "ERROR", err, sys)


def scrap_by_selectorlib(page):
    """
    Scrap web using selectorlib library

    Args:
        page (str): Url to scrap

    Returns:
        dict: product data
    """
    try:
        loggear("Method scrap_by_selectorlib to scrap the Amazon page...", "INFO")
        extractor = Extractor.from_yaml_file(os.path.join(
            os.path.dirname(__file__), 'selectors.yml'))
        data_product = extractor.extract(page.text)

        # Get only the first image, its a string dict so that it is necessary
        # to use json.loads to get a dict, after that it takes the first image
        loggear(f"Amazon metadata product: {data_product}", "DEBUG")
        if data_product['images']:
            data_product['images'] = next(
                iter(json.loads(data_product['images'])))
        else:
            data_product['images'] = "/static/img/no_image.jpeg"

        return data_product
    except Exception as err:
        loggear("Error in scrap_by_selectorlib method:", "ERROR", err, sys)


def scrap_by_beautifulsoup(page):
    """
    Scrap web using beautifulsoup library

    Args:
        page (str): Url to scrap

    Returns:
        dict: product data
    """
    try:
        loggear("Method scrap_by_beautifulsoup to scrap the Amazon page...", "INFO")
        soup = BeautifulSoup(page.content, "html.parser")

        loggear(soup.find(id="productTitle").text.strip(), "DEBUG")  # By DOM element id
        # By DOM element class
        loggear(soup.find(class_="a-offscreen").text.strip(), "DEBUG")
        loggear(soup.find(class_="a-icon-alt").text.strip(), "DEBUG")
        loggear(soup.find(id="acrCustomerReviewText"), "DEBUG")
        loggear(soup.find(class_="a-dynamic-image"), "DEBUG")

        return True
        # ...continue

    except Exception as err:
        loggear("Error in scrap_by_beautifulsoup method:", "ERROR", err, sys)


def scrap_web(url):
    """
    Scrap a url web to extract different data

    Args:
        url (str): url web to scrap
    """
    try:
        loggear(f"Method scrap_web to scrap the url: {url}", "INFO")

        proxies = get_proxies() if os.environ['PROXY'] in ["Y", "y"] else None
        if proxies:
            loggear(
                f"Use proxy to access to Amazon: {proxies[0]}", "DEBUG")
            page = requests.get(url, headers=headers, proxies={
                                "http": proxies[0], "https": proxies[0]})
        else:
            loggear("Don't use proxy to access to Amazon", "DEBUG")
            page = requests.get(url, headers=headers)

        if page.status_code > 500:
            loggear("Page %s must have been blocked by Amazon as the status code was %d" % (
                url, page.status_code), "DEBUG")
            return None
        else:
            if "To discuss automated access to Amazon data please contact api-services-support@amazon.com" in page.text:
                raise Exception(
                    "Page was blocked by Amazon. Please try using better proxies or try later")

        loggear(f"Status code page: {page.status_code}", "DEBUG")
        data_product = scrap_by_selectorlib(page)
        scrap_by_beautifulsoup(page)

        loggear("Process scrap_web finished", "INFO")

        return data_product

    except Exception as err:
        loggear("Error scrapping url web:", "ERROR", err, sys)


if __name__ == "__main__":
    loggear("Starting primazon utils...")
    loggear("Select option:")
    loggear("1. Scrap url")
    loggear("2. Exit")
    option = input()
    if option == "1":
        url = str(sys.argv[1]) if len(sys.argv) > 1 else None
        loggear("Please entry the url to scrap:")
        url = input() if not url else ""
        scrap_web(url)

    loggear("Primazon utils finished")
