import logging
from rich.console import Console
import sys
import os
from datetime import datetime

console = Console()

COLOR_DEBUG = "blue"
COLOR_INFO = "green"
COLOR_WARNING = "orange bold"
COLOR_ERROR = "red bold"

# Min log level to print
LEVEL=os.environ["LEVEL"]

def loggear(message="", level="INFO", err=Exception, sys=sys):
    color = eval("COLOR_" + level)
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    if level in ["ERROR"]:
        console.print(time, level, message,
                      f"\nLine: {sys.exc_info()[2].tb_lineno} {type(err).__name__} ",
                      f"\nMethod: {sys.exc_info()[2].tb_frame.f_code.co_name} ",
                      f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} ",
                      f"\nError: {format(err)}", style=color)
    else:
        console.print(time, level, message, style=color)


"""
FORMAT = '%(asctime)s %(levelname)s %(lineno)d %(filename)s %(funcName)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)


def loggear_logging(message="", level="INFO"):
    logging.info(message, exc_info=True)
"""
