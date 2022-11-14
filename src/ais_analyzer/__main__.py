import logging
import time

from .handlers.output_handler import OutputHandler
from .handlers.input_handler import InputHandler
from .handlers.cli_handler import CommandLineInterfaceHandler
from .commands import statistics, portcalls
from .logger.log_init import log_init
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
    cli = CommandLineInterfaceHandler()
    user_arguments = cli.get_args(asdict=True)
    # Get the logging level and set the log-class to
    # custom logger
    _log_level = user_arguments["log"].upper()
    _log_cli = user_arguments["log_cli"]
    _log_cli = ensure_log_cli(_log_cli)
    logging.setLoggerClass(AisLogger)

    # Initiate a new logger, and set the format as desired
    log_init(_log_level, _log_cli)
    logger = logging.getLogger("main")

    # 2. Loading the data using input handler
    input_path = user_arguments['input_file']
    input_data = logger.time_info("Loading data", InputHandler(path=input_path).get_data)
    logger.log_memory(input_data)

    # 3. Calling the command on the data
    implemented_commands = {'statistics': statistics.statistics, 'portcalls': portcalls.portcalls}
    user_command = user_arguments['command']
    transformed_data = logger.time_info(f"Command: {user_command}",
                                        implemented_commands[user_command], # Command
                                        input_data,     # Arg for command
                                        user_arguments  # Arg for command
                                        )

    # 4. Output the transformed data
    output_path = user_arguments['output_file']
    if output_path:
        OutputHandler(output_path).output_csv(transformed_data)
    else:
        OutputHandler().output_terminal(transformed_data)


def ensure_log_cli(log_cli: str) -> bool:
    """
    Ensures log_cli is turned to a boolean value,
    and raise an error if it somehow is not.
    It should, however, not be possible to not be either true or false.

    :param log_cli:
    :return:
    """
    true = ["true", "cli"]
    false = ["false", "file"]
    if log_cli.lower() in true:
        return True
    if log_cli.lower() in false:
        return False
    raise RuntimeError(f"Value of --log-cli {log_cli} not a boolean value.\n"
                       + f"Value {log_cli.lower()} not in {true} or {false}")


if __name__ == "__main__":
    __main__()
