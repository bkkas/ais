import logging
import time

from .handlers.output_handler import OutputHandler
from .handlers.input_handler import InputHandler
from .handlers.cli_handler import AISCLI
from .commands import statistics, portcalls
from .logger.log_init import log_init
from .logger.time_log import time_info_gen
from .logger.time_log import time_info_call


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

    # 2. Loading the data using input handler
    input_path = user_arguments['input_file']
    input_handler = InputHandler(path=input_path)
    input_data = time_info_call(logging, "call test", InputHandler(path=input_path).get_data)
    input_data = time_info_call(logging, "call test second", InputHandler.get_data, input_handler)
    """
    timer = time_info_gen(logging, msg="Test") #logging.info(f"Reads data using InputHandler from {input_path}")
    next(timer)
    input_data = InputHandler(path=input_path).get_data()
    next(timer)
    """

    # 3. Calling the command on the data
    implemented_commands = {'statistics': statistics.statistics, 'portcalls': portcalls.portcalls}
    user_command = user_arguments['command']
    logging.info(f"Command: {user_command}")
    _start = time.time()
    transformed_data = implemented_commands[user_command](input_data, user_arguments)
    _taken = time.time() - _start
    logging.info(f"Command \"{user_command}\" took {_taken:.4f}s")

    # 4. Output the transformed data
    output_path = user_arguments['output_file']
    if output_path:
        OutputHandler(output_path).output_csv(transformed_data)
    else:
        OutputHandler().output_terminal(transformed_data)


if __name__ == "__main__":
    __main__()
