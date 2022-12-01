import logging
import time
from typing import Callable, Generator
from pandas import DataFrame, Series


class AisLogger(logging.getLoggerClass()):
    """
    A custom logging class made for the ais-analyzer package.
    It needs to be set by using `logging.setLoggerClass(AisLogger)` to get access to its functionality.
    This means that anywhere this class is intended to be used, this code should be run first:
    >>> logging.setLoggerClass(AisLogger)
    >>> logger = logging.getLogger(__name__)  # Or other name that is desired
    IDE-s are generally not clever enough to autocomplete the new functions, so
    knowing what they can do beforehand is a great advantage.

    Implements:
    time_info(msg: str, func: Callable, *args, **kwargs) -> what Callable returns
    time_info_generator(msg: str) -> Generator
    log_memory(df: [DataFrame, Series], df_name: str, msg: str, deep: Bool, agg: Bool) -> None
    """

    def __init__(self, name: str):
        logging.Logger.__init__(self, name)

    def get_logger(self, name: str):
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

    def time_info_generator(self, msg: str) -> Generator:
        """
        The same as time_info, but does not need to call the function itself.
        Can be used around a for loop or similar, instead of having to move the
        loop into a separate function.
        Also supports timeing each iteration of a loop.

        Usage:
        gen = logger.time_info_generator("msg")
        next(gen)
        # Function call or loop or execution to time
        next(gen)
        #### or
        gen = logger.time_info_generator("msg")
        next(gen)
        for item in something:
            ...
            gen.send(something)
            ...
        next(gen)


        :param msg:
        :return:
        """
        # TODO possible expansion to x = yield?
        self.info(msg)
        start = time.time()
        y_msg = yield
        while y_msg:
            taken = time.time() - start
            self.debug(f"Message sent: {y_msg}\n" +
                       f"{' '*10}" +
                       f"{msg} time taken so far: {taken:.4f}s")
            y_msg = yield
        taken = time.time() - start
        self.info(f"{msg} took {taken:.4f}s")
        yield

    def log_memory(self, df: [DataFrame, Series], df_name="", msg="", deep=False, agg=True) -> None:
        # For better readability in logging a series of memory
        spacing = 25 * '-'

        # If debugging, automatically search deep, and do not aggregate
        debug = False
        if self.getEffectiveLevel() == logging.DEBUG:
            deep = True
            agg = False
            debug = True

        if type(df) == DataFrame:
            # Aggregate into a single number
            mem = df.memory_usage(deep=deep).sum()
            # If debugging, show how much memory is used by each index
            if not agg:
                mem_series = df.memory_usage(deep=deep)
        else:
            # A series does not have any indexes,
            # and is equivalent with memory_usage.sum()
            # for a dataframe
            mem = df.memory_usage(deep=deep)

        # Bytes to kilo-bytes
        mem = mem / 1000
        postfix = "KB"
        # If in megabyte-size
        if mem % 1000 < mem:
            mem = mem / 1000
            postfix = "MB"

        # A not deep search does not give the whole
        # truth of memory usage, and this is shown with the '+'
        sign = " "
        if not deep:
            sign = "+ "

        if agg or (type(df) == Series):
            # If a message is provided, print the message instead
            if msg:
                self.debug(f"{msg} {mem:.3f} {postfix}")
            else:
                self.debug(f"Memory usage usage {df_name}: {mem:.3f} {postfix}")
            if not debug:
                if msg:
                    self.info(f"{msg} {mem:.3f}{sign}{postfix}")
                else:
                    self.info(f"Memory usage {df_name}: {mem:.3f}{sign}{postfix}")
        try:
            mem_series
            if msg:
                self.debug(
                    f"{msg}\n"
                    f"Memory usage {df_name}:\n"
                    f"{spacing} \n"
                    f"{mem_series} \n"
                    f"Total mem: {mem:.3f} {postfix}\n"
                    f"{spacing}"
                )
            else:
                self.debug(
                    f"Memory usage {df_name}:\n"
                    f"{spacing} \n"
                    f"{mem_series} \n"
                    f"Total mem: {mem:.3f} {postfix}\n"
                    f"{spacing}"
                )
        except NameError:
            # If mem_series is not defined
            # then pass
            pass
