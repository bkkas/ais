import logging
from pandas import DataFrame, Series


def log_memory(logger: logging.Logger, df: [DataFrame, Series], df_name="", msg="", deep=False, agg=True) -> None:
    # For better readability in logging a series of memory
    spacing = 25 * '-'

    # If debugging, show more info
    debug = False
    if logger.getEffectiveLevel() == logging.DEBUG:
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
            logger.debug(f"{msg} {mem:.3f} {postfix}")
        else:
            logger.debug(f"Memory usage usage {df_name}: {mem:.3f} {postfix}")
        if not debug:
            if msg:
                logger.info(f"{msg} {mem:.3f}{sign}{postfix}")
            else:
                logger.info(f"Memory usage {df_name}: {mem:.3f}{sign}{postfix}")
    try:
        mem_series
        logger.debug(
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
