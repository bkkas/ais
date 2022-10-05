import my_ais_cli as cli
import my_ais_handler as ais_handler
from src.ais_analyzer.handlers import input_handler, output_handler

from commands import statistics


def __main__():
    """
    Our application has three rough steps:
    1. Take arguments from the user via command line
    2. Load the data from the path specified in the CLI
    3. Apply the command specified in the CLI
    4. Output result of command to user (via a csv file for now)

    """

    # 1. Getting the user arguments from the command line
    # Instantiating the CLI and getting arguments
    mycli = cli.MyAISCLI()
    args = mycli.get_args(asdict=True)

    # 2. Loading the data using ais handler
    # Instantiating an AIS handler and passing the CLI argument
    myais = ais_handler.MyAISHandler()
    myais.eval_args(args)

    # 2.* Loading the data using input handler
    my_data = input_handler.InputHandler(args['path'])

    # 3. Calling the command on my data
    # TODODO: Proper input validation
    commands = {'statistics': statistics}
    command = args['commmand']
    params = args['full']

    if command in commands.keys():
        # Statistics is the only command, so we call the statistics method on the data
        res = commands[command](my_data, params)

    # 4. Output the transformed data
    output_handler.OutputHandler(args['output'])


if __name__ == "__main__":
    __main__()
