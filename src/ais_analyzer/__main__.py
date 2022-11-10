import logging
import time

from .handlers.output_handler import OutputHandler
from .handlers.input_handler import InputHandler
from .handlers.cli_handler import AISCLI
from .commands import statistics, portcalls
from .logger.log_init import log_init
from .logger.time_log import time_info_gen
from .logger.time_log import time_info_call
from .logger.memory_log import log_memory
from .logger.log_class import logger
from .logger.log_class import AisLogger


def __main__():
    """
    The application has three steps:
    1. Take arguments from the user via command line
    2. Load the data from the path specified in the CLI
    3. Apply the command specified in the CLI
    4. Output result of command to user (via a csv file for now)

    """

    # 1. Getting the user arguments from the command line
    # Instantiating the CLI and getting arguments
    cli = AISCLI()
    user_arguments = cli.get_args(asdict=True)
    _log_level = user_arguments["log"].upper()
    log_init(_log_level)
    #logger.log_init(_log_level)
    #logger = AisLogger("a")
    logger.getChild("main")

    # 2. Loading the data using input handler
    input_path = user_arguments['input_file']
    input_handler = InputHandler(path=input_path)
    input_data = logger.time_info("Test 1", InputHandler(path=input_path).get_data)
    input_data = logger.time_info("Test 2", InputHandler.get_data, input_handler)
    log_memory(logger, input_data)
    """"
    timer = time_info_gen(logger, msg="Test") #logging.info(f"Reads data using InputHandler from {input_path}")
    next(timer)
    input_data = InputHandler(path=input_path).get_data()
    next(timer)
    """

    # 3. Calling the command on the data
    implemented_commands = {'statistics': statistics.statistics, 'portcalls': portcalls.portcalls}
    user_command = user_arguments['command']
    logger.info(f"Command: {user_command}")
    _start = time.time()
    transformed_data = implemented_commands[user_command](input_data, user_arguments)
    _taken = time.time() - _start
    logger.info(f"Command \"{user_command}\" took {_taken:.4f}s")

    # 4. Output the transformed data
    output_path = user_arguments['output_file']
    if output_path:
        OutputHandler(output_path).output_csv(transformed_data)
    else:
        OutputHandler().output_terminal(transformed_data)


if __name__ == "__main__":
    __main__()
