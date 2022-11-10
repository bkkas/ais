import logging
import time
from typing import Callable


class AisLogger(logging.getLoggerClass()):
    #def __init__(self, name):
    #    super(AisLogger, self).__init__(name)
    def __init__(self, name):
        super(AisLogger, self).__init__(name)
        logging.getLogger('root')


    def log_init(self, log_level):
        logging_format = "{levelname}:{name} : {asctime}ms -- {message}"
        logging.basicConfig(
            filename='ais_log.log',
            encoding='utf-8',
            level=log_level,
            format=logging_format,
            style='{'
        )

    def get_logger(self, name):
        return self.getChild(name)

    def time_info(self, msg: str, func: Callable, *args, **kwargs):
        """
        Logger is the logger defined when doing "logging.getLogger(__name__)"
        for the root or main, this is just the imported "logging" module.
        Msg is the message that is to be printed.
        Generally, this should reference the name of the function.
        Function is the called object, and *args are the arguments passed to func

        :param msg:
        :param func:
        :param args:
        :return:
        """
        self.info(msg)
        start = time.time()
        ret_val = func(*args, **kwargs)
        taken = time.time() - start
        self.info(f"{msg} took {taken:.4f}s")
        return ret_val



logger = AisLogger()