# by Richi Rod AKA @richionline / falken20

import sys
import os
import re
import requests
import json
from selectorlib import Extractor
from bs4 import BeautifulSoup

from src.logger import Log, console

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
        Log.info("Method get_proxies to get free proxies...")

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
        Log.error("Error in get_proxies method:", err, sys)


def scrap_by_selectorlib(page):
    """
    Scrap web using selectorlib library

    Args:
        page (str): Url to scrap

    Returns:
        dict: product data
    """
    try:
        Log.info("Method scrap_by_selectorlib to scrap the Amazon page...")
        extractor = Extractor.from_yaml_file(os.path.join(
            os.path.dirname(__file__), 'selectors.yml'))
        data_product = extractor.extract(page.text)

        # Get only the first image, its a string dict so that it is necessary
        # to use json.loads to get a dict, after that it takes the first image
        Log.debug(f"Amazon metadata product: {data_product}")
        if data_product['images']:
            data_product['images'] = next(
                iter(json.loads(data_product['images'])))
        else:
            data_product['images'] = "/static/img/no_image.jpeg"

        return data_product
    except Exception as err:
        Log.error("Error in scrap_by_selectorlib method:", err, sys)


def scrap_by_beautifulsoup(page):
    """
    Scrap web using beautifulsoup library

    Args:
        page (str): Url to scrap

    Returns:
        dict: product data
    """
    try:
        Log.info("Method scrap_by_beautifulsoup to scrap the Amazon page...")
        soup = BeautifulSoup(page.content, "html.parser")

        # By DOM element id
        Log.debug(soup.find(id="productTitle").text.strip())
        # By DOM element class
        Log.debug(soup.find(class_="a-offscreen").text.strip())
        Log.debug(soup.find(class_="a-icon-alt").text.strip())
        Log.debug(soup.find(id="acrCustomerReviewText"))
        Log.debug(soup.find(class_="a-dynamic-image"))

        return True
        # ...continue

    except Exception as err:
        Log.error("Error in scrap_by_beautifulsoup method:", err, sys)


def scrap_web(url):
    """
    Scrap a url web to extract different data

    Args:
        url (str): url web to scrap
    """
    try:
        Log.info(f"Method scrap_web to scrap the url: {url}")

        proxies = get_proxies() if os.environ['PROXY'] in ["Y", "y"] else None
        if proxies:
            Log.debug(
                f"Use proxy to access to Amazon: {proxies[0]}")
            page = requests.get(url, headers=headers, proxies={
                                "http": proxies[0], "https": proxies[0]})
        else:
            Log.debug("Don't use proxy to access to Amazon")
            page = requests.get(url, headers=headers)

        if page.status_code > 500:
            Log.debug("Page %s must have been blocked by Amazon as the status code was %d" % (
                url, page.status_code))
            return None
        else:
            if "To discuss automated access to Amazon data please contact api-services-support@amazon.com" in page.text:
                raise Exception(
                    "Page was blocked by Amazon. Please try using better proxies or try later. " +
                    f"Page Status Code: {page.status_code}")

        # Log.debug(f"Amazon back page text: \n{page.text}")
        Log.info(f"Amazon status code page: {page.status_code}")
        data_product = scrap_by_selectorlib(page)
        # scrap_by_beautifulsoup(page)

        Log.info("Process scrap_web finished")

        return data_product

    except Exception as err:
        Log.error("Error scrapping url web:", err, sys)
        # raise Exception(err)
        return None


if __name__ == "__main__":
    console.rule("Primazon utils...")
    Log.info("Select option:")
    Log.info("1. Scrap url")
    Log.info("2. Exit")
    option = input()
    if option == "1":
        url = str(sys.argv[1]) if len(sys.argv) > 1 else None
        Log.info("Please entry the url to scrap:")
        url = input() if not url else ""
        scrap_web(url)

    Log.info("Primazon utils finished")
