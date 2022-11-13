import logging
import sys


def log_init(log_level: str, log_cli: bool) -> None:
    """
    Sets the logger to log in a specific format.
    It cannot both write to stream and to file at the same time, sadly.

    :param log_level:
    :param log_cli:
    :return:
    """
    logging_format = "{levelname}:{name} : {asctime}ms -- {message}"
    if log_cli:
        logging.basicConfig(
            stream=sys.stdout,
            encoding='utf-8',
            level=log_level,
            format=logging_format,
            style='{'
        )
        return
    logging.basicConfig(
        filename='ais_log.log',
        encoding='utf-8',
        level=log_level,
        format=logging_format,
        style='{'
    )
