import sys
import os
from rich.console import Console
from rich.style import Style
from datetime import datetime

# Create console object for logs
console = Console()

style_DEBUG = Style(color="cyan")  # style_debug = "red bold"
style_INFO = Style(color="green")
style_WARNING = Style(color="orange3", bold=True)
style_ERROR = Style(color="red", bgcolor="white", bold=True)

# Min log level to print
LEVEL_LOG = os.environ["LEVEL_LOG"]


def loggear(message="", level="INFO", err=Exception, sys=sys):
    try:
        time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        color = eval("style_" + level)

        if level in ["ERROR"]:
            console.print(time, level, message,
                        f"\nLine: {sys.exc_info()[2].tb_lineno} {type(err).__name__} ",
                        f"\nMethod: {sys.exc_info()[2].tb_frame.f_code.co_name} ",
                        f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} ",
                        f"\nError: {format(err)}",
                        style=color)
        elif level in LEVEL_LOG:
            console.print(time, level, message, style=color)

    except Exception as err:
        console.print(time, level, message, f"\nError: {format(err)}", style=style_ERROR)




"""
import logging

FORMAT = '%(asctime)s %(levelname)s %(lineno)d %(filename)s %(funcName)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)


def loggear_logging(message="", level="INFO"):
    logging.info(message, exc_info=True)
"""
