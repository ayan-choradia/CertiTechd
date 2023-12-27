import http
import logging
import sys
from copy import copy
from typing import Optional

import click

TRACE_LOG_LEVEL = 5


class CustomFormatter(logging.Formatter):
    """
    A custom logging formatter that formats log records with ANSI color escape sequences.

    Attributes:
    -----------
    level_name_colors: Dict
        A dictionary that maps log levels to color functions for coloring the level name.
    """
    level_name_colors = {
        TRACE_LOG_LEVEL: lambda level_name: click.style(str(level_name), fg="blue"),
        logging.DEBUG: lambda level_name: click.style(str(level_name), fg="cyan"),
        logging.INFO: lambda level_name: click.style(str(level_name), fg="green"),
        logging.WARNING: lambda level_name: click.style(str(level_name), fg="yellow"),
        logging.ERROR: lambda level_name: click.style(str(level_name), fg="red"),
        logging.CRITICAL: lambda level_name: click.style(
            str(level_name), fg="bright_red"
        ),
    }

    def __init__(
        self,
        fmt: Optional[str] = None,
        datefmt: Optional[str] = None,
        style: str = "%",
    ):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def color_level_name(self, level_name: str, level_no: int) -> str:
        """
        Colors the level name with ANSI color escape sequences based on the log level.

        Arguments:
        ----------
        level_name: str
            The name of the log level.
        level_no: int
            The numeric value of the log level.

        Returns:
        --------
        str: The colored level name with ANSI color escape sequences.
        """
        def default(level_name: str) -> str:
            return str(level_name)  # pragma: no cover

        func = self.level_name_colors.get(level_no, default)
        return func(level_name)

    def formatMessage(self, record: logging.LogRecord) -> str:
        """
        Formats a log record with ANSI color escape sequences.

        Arguments:
        ----------
        record: logging.LogRecord
            The log record to format.
        
        Returns:
        --------
        str: The formatted log message with ANSI color escape sequences.
        """
        recordcopy = copy(record)
        levelname = recordcopy.levelname
        recordcopy.__dict__["asctime"] = click.style(
            recordcopy.asctime, fg="bright_magenta"
        )
        recordcopy.__dict__["filename"] = click.style("File ", fg="blue") + click.style(
            "'" + recordcopy.filename + "'", fg="bright_cyan"
        )
        recordcopy.__dict__["funcName"] = click.style(
            recordcopy.funcName, fg="red"
        ) + click.style("():", fg="red")

        recordcopy.__dict__["message"] = click.style(
            recordcopy.message, fg="bright_red"
        )
        seperator = " " * (8 - len(recordcopy.levelname))
        levelname = self.color_level_name(levelname, recordcopy.levelno)
        recordcopy.__dict__["levelprefix"] = levelname + ":" + seperator
        recordcopy.__dict__["line"] = (
            click.style("line", fg="green")
            + " "
            + click.style(recordcopy.lineno, "green")
        )
        recordcopy.__dict__["in_func"] = click.style("in func", fg="yellow")
        return super().formatMessage(recordcopy)


class AccessFormatter(CustomFormatter):
    """
    Custom log formatter for access logs.

    Attributes:
    -----------
    status_code_colours: dict[int, Callable[[int], str]]
        A mapping of HTTP status code prefixes (100s, 200s, etc.) to functions that return
        styled representations of the status codes.
    """
    status_code_colours = {
        1: lambda code: click.style(str(code), fg="bright_white"),
        2: lambda code: click.style(str(code), fg="green"),
        3: lambda code: click.style(str(code), fg="yellow"),
        4: lambda code: click.style(str(code), fg="red"),
        5: lambda code: click.style(str(code), fg="bright_red"),
    }

    def get_status_code(self, status_code: int) -> str:
        """
        Returns a styled representation of the provided HTTP status code.

        Arguments:
        ----------
        status_code: int
            The HTTP status code to style.

        Returns:
        --------
        str: A styled representation of the provided HTTP status code.
        """
        try:
            status_phrase = http.HTTPStatus(status_code).phrase
        except ValueError:
            status_phrase = ""
        status_and_phrase = "%s %s" % (status_code, status_phrase)

        def default(code: int) -> str:
            return status_and_phrase  # pragma: no cover

        func = self.status_code_colours.get(status_code // 100, default)
        return func(status_and_phrase)

    def formatMessage(self, record: logging.LogRecord) -> str:
        """
        Formats the log message using the provided LogRecord instance.

        Arguments:
        ----------
        record: logging.LogRecord
            The log record to format.

        Returns:
        --------
        str: The formatted log message.
        """
        try:
            recordcopy = copy(record)
            (
                client_addr,
                method,
                full_path,
                http_version,
                status_code,
            ) = recordcopy.args
            status_code = self.get_status_code(int(status_code))
            request_line = click.style(f"{method} {full_path}", bold=True)
            recordcopy.__dict__.update(
                {
                    "client_addr": click.style(client_addr, fg="bright_cyan"),
                    "request_line": click.style(request_line, fg="yellow"),
                    "status_code": status_code,
                }
            )
        except:
            pass
        return super().formatMessage(recordcopy)
