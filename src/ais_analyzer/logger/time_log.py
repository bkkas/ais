import logging
import time
from typing import Callable


def time_info_gen(logger: logging.Logger, msg: str):
    if logger:
        logger.info(msg)
    else:
        logging.info(msg)
    start = time.time()
    yield
    taken = time.time() - start
    if logger:
        logger.info(f"{msg} took {taken}s")
    else:
        logging.info(f"{msg} took {taken}s")
    yield


def time_info_call(logger: logging.Logger, msg: str, func: Callable, *args, **kwargs):
    """
    Logger is the logger defined when doing "logging.getLogger(__name__)"
    for the root or main, this is just the imported "logging" module.
    Msg is the message that is to be printed.
    Generally, this should reference the name of the function.
    Function is the called object, and *args are the arguments passed to func

    :param logger:
    :param msg:
    :param func:
    :param args:
    :return:
    """
    logger.info(msg)
    start = time.time()
    ret_val = func(*args, **kwargs)
    taken = time.time() - start
    logger.info(f"{msg} took {taken:.4f}s")
    return ret_val
