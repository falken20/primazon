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


class Log():
    @staticmethod
    def debug(message):
        try:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            level = Log.debug.__name__.upper()

            if level in LEVEL_LOG.upper():
                console.print(time, level, message, style=style_DEBUG)

        except Exception as err:
            Log.error("Error to print log", err, sys)

    def info(message):
        try:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            level = Log.info.__name__.upper()

            if level in LEVEL_LOG.upper():
                console.print(time, level, message, style=style_INFO)

        except Exception as err:
            Log.error("Error to print log", err, sys)

    def warning(message):
        try:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            level = Log.warning.__name__.upper()

            if level in LEVEL_LOG.upper():
                console.print(time, level, message, style=style_WARNING)

        except Exception as err:
            Log.error("Error to print log", err, sys)

    @staticmethod
    def error(message, err, sys):
        """
        Print error in terminal

        Args:
            message: Messsage to show
            err(Exception): Exception
            sys(sys): System var
        """
        try:
            time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            level = Log.error.__name__.upper()

            if level in LEVEL_LOG.upper():
                console.rule("ERROR")
                console.print(time, level, message,
                              f"\nLine: {sys.exc_info()[2].tb_lineno} {type(err).__name__} ",
                              f"\nMethod: {sys.exc_info()[2].tb_frame.f_code.co_name} ",
                              f"\nFile: {sys.exc_info()[2].tb_frame.f_code.co_filename} ",
                              f"\nError: {format(err)}",
                              style=style_ERROR)

        except Exception as err:
            Log.error("Error to print log", err, sys)
