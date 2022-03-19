# by Richi Rod AKA @richionline / falken20
import sys
import os
from click import style
import requests

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


def scrap_web(url):
    """
    Scrap a url web to extract different data

    Args:
        url (str): url web to scrap
    """
    try:
        url = "https://www.amazon.es/gp/product/B09JR6YL4B"

        page = requests.get(url, headers=headers)
        if page.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in page.text:
                console.print(
                    "Page %s was blocked by Amazon. Please try using better proxies\n" % url, style="bold red")
            else:
                console. print("Page %s must have been blocked by Amazon as the status code was %d" % (
                    url, page.status_code), style="bold red")
                return None

        soup = BeautifulSoup(page.content, "html.parser")
        print(soup.find(id="productTitle").text.strip())  # By DOM element id
        # By DOM element class
        print(soup.find(class_="a-offscreen").text.strip())

        extractor = Extractor.from_yaml_file(os.path.join(
            os.path.dirname(__file__), 'selectors.yml'))
        print(extractor.extract(page.text))

        console.print("[bold green]Process finished succesfully[/bold green]")

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
