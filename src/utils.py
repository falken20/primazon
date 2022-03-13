# by Richi Rod AKA @richionline / falken20
import sys
import pandas as pd
from rich.console import Console

# Load .env file
# load_dotenv(find_dotenv())

# Create console object
console = Console()


def scrap_web(url):
    """
    Scrap a url web to extract different data

    Args:
        url (str): url web to scrap
    """
    try:
        url = "https://www.amazon.es/gp/product/B09JR6YL4B/ref=ox_sc_saved_title_6?smid=A1AT7YVPFBWXBL&psc=1"
        console.print(f"Starting process to scrap web: \n{url}", style="bold green")
        data = pd.read_html(url)
        print(data)

        console.print("[bold green]Process finished succesfully[/bold green]")

    except Exception as err:
        console.print(
            f"Error scrapping url web:" +
            f"\nLine {sys.exc_info()[2].tb_lineno} {type(err).__name__} " +
            f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} " +
            f"\n{format(err)}", style="red bold")


if __name__ == "__main__":
    url = str(sys.argv[1]) if len(sys.argv) > 1 else ""
    scrap_web(url)

