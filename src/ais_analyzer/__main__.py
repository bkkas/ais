import logging
import time

from .handlers.output_handler import OutputHandler
from .handlers.input_handler import InputHandler
from .handlers.cli_handler import AISCLI
from .commands import statistics, portcalls


def __main__():
    """
    The application has three steps:
    1. Take arguments from the user via command line
    2. Load the data from the path specified in the CLI
    3. Apply the command specified in the CLI
    4. Output result of command to user (via a csv file for now)

    """
    logging_format = "{levelname}:{name} : {asctime}ms -- {message}"
    logging.basicConfig(
        filename='ais_log.log',
        encoding='utf-8',
        level=logging.DEBUG,
        format=logging_format,
        style='{'
    )
    # 1. Getting the user arguments from the command line
    # Instantiating the CLI and getting arguments
    cli = AISCLI()
    user_arguments = cli.get_args(asdict=True)
    # 2. Loading the data using input handler
    input_path = user_arguments['input_file']
    logging.info(f"Reads data using InputHandler from {input_path}")
    _start = time.time()
    input_data = InputHandler(path=input_path).get_data()
    _taken = time.time() - _start
    logging.info(f"InputHandler took {_taken:.4f}s")

    # 3. Calling the command on the data
    implemented_commands = {'statistics': statistics.statistics, 'portcalls': portcalls.portcalls}
    user_command = user_arguments['command']
    logging.info(f"Does command: {user_command}")
    _start = time.time()
    transformed_data = implemented_commands[user_command](input_data, user_arguments)
    _taken = time.time() - _start
    logging.info(f"InputHandler took {_taken:.4f}s")

    # 4. Output the transformed data
    output_path = user_arguments['output_file']
    if output_path:
        OutputHandler(output_path).output_csv(transformed_data)
    else:
        OutputHandler().output_terminal(transformed_data)


if __name__ == "__main__":
    __main__()
