import logging


def log_init(log_level: str) -> None:
    logging_format = "{levelname}:{name} : {asctime}ms -- {message}"
    logging.basicConfig(
        filename='ais_log.log',
        encoding='utf-8',
        level=log_level,
        format=logging_format,
        style='{'
    )
