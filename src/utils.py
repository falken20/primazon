# by Richi Rod AKA @richionline / falken20
import sys
import os
import re
from click import style
import requests
import json
from lxml.html import fromstring

from rich.console import Console
from selectorlib import Extractor
from bs4 import BeautifulSoup

# Load .env file
# load_dotenv(find_dotenv())

# Create console object
console = Console()

headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
        console.print(
            f"Method get_proxies to get free proxies...", style="blue")

        url = 'https://free-proxy-list.net/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}

        source = str(requests.get(url, headers=headers, timeout=10).text)
        data = [list(filter(None, i))[0] for i in re.findall(
            '<td class="hm">(.*?)</td>|<td>(.*?)</td>', source)]

        groupings = [dict(zip(['ip', 'port', 'code', 'using_anonymous'], data[i:i+4]))
                     for i in range(0, len(data), 4)]

        # proxies = [{'full_ip':"{ip}:{port}".format(**i)} for i in groupings]
        proxies = ["{ip}:{port}".format(**i) for i in groupings]

        return proxies
    except Exception as err:
        console.print(
            f"Error in get_proxies method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


def scrap_by_selectorlib(page):
    """
    Scrap web using selectorlib library

    Args:
        page (str): Url to scrap

    Returns:
        dict: product data
    """
    try:
        console.print(
            f"Method scrap_by_selectorlib to scrap the Amazon page...", style="blue")
        extractor = Extractor.from_yaml_file(os.path.join(
            os.path.dirname(__file__), 'selectors.yml'))
        data_product = extractor.extract(page.text)

        # Get only the first image, its a string dict so that it is necessary
        # to use json.loads to get a dict, after that it takes the first image
        console.print(f"Amazon metadata product: {data_product}", style="blue")
        if data_product['images']:
            data_product['images'] = next(
                iter(json.loads(data_product['images'])))
        else:
            data_product['images'] = "/static/img/no_image.jpeg"

        return data_product
    except Exception as err:
        console.print(
            f"Error in scrap_by_selectorlib method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


def scrap_by_beautifulsoup(page):
    """
    Scrap web using beautifulsoup library

    Args:
        page (str): Url to scrap

    Returns:
        dict: product data
    """
    try:
        console.print(
            f"Method scrap_by_beautifulsoup to scrap the Amazon page...", style="blue")
        soup = BeautifulSoup(page.content, "html.parser")

        print(soup.find(id="productTitle").text.strip())  # By DOM element id
        # By DOM element class
        print(soup.find(class_="a-offscreen").text.strip())
        print(soup.find(class_="a-icon-alt").text.strip())
        print(soup.find(id="acrCustomerReviewText"))
        print(soup.find(class_="a-dynamic-image"))

        return True
        # ...continue

    except Exception as err:
        console.print(
            f"Error in scrap_by_beautifulsoup method:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


def scrap_web(url):
    """
    Scrap a url web to extract different data

    Args:
        url (str): url web to scrap
    """
    try:
        console.print(
            f"Method scrap_web to scrap the url: {url}", style="blue")

        # proxies = get_proxies()
        proxies = None
        if proxies:
            page = requests.get(url, headers=headers, proxies={
                                "http": proxies[0], "https": proxies[0]})
        else:
            page = requests.get(url, headers=headers)            

        if page.status_code > 500:
            console. print("Page %s must have been blocked by Amazon as the status code was %d" % (
                    url, page.status_code), style="bold red")
            return None
        else:
            if "To discuss automated access to Amazon data please contact api-services-support@amazon.com" in page.text:
                raise Exception(
                    "Page was blocked by Amazon. Please try using better proxies or try later")

        console.print(f"Status code page: {page.status_code}", style="blue")
        data_product = scrap_by_selectorlib(page)
        scrap_by_beautifulsoup(page)

        console.print(
            "[bold green]Process scrap_web finished[/bold green]")

        return data_product

    except Exception as err:
        console.print(
            f"Error scrapping url web:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


if __name__ == "__main__":
    console.print(f"Starting primazon utils...", style="bold green")
    console.print("Select option:", style="yellow")
    console.print("1. Scrap url", style="yellow")
    console.print("2. Exit", style="yellow")
    option = input()
    if option == "1":
        url = str(sys.argv[1]) if len(sys.argv) > 1 else None
        console.print("Please entry the url to scrap:", style="yellow")
        url = input() if not url else ""
        scrap_web(url)

    console.print(f"Primazon utils finished", style="bold green")
