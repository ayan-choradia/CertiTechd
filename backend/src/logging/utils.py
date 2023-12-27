import logging.config

from .config import LOGGING_CONFIG


def configure_logging():
    """
    Configures logging using the provided logging configuration.

    The logging configuration is loaded from the `LOGGING_CONFIG` dictionary defined in the
    `config` module.

    Returns:
    --------
    None
    """
    logging.config.dictConfig(LOGGING_CONFIG)
