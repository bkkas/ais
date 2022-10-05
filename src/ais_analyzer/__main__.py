import my_ais_cli as cli
import my_ais_handler as ais_handler

import csv
import pandas as pd


def __main__():

    # Instantiating the CLI and getting arguments
    mycli = cli.MyAISCLI()
    args = mycli.get_args(asdict=True)

    # Instantiating an AIS handler and passing the CLI argument
    myais = ais_handler.MyAISHandler()
    myais.eval_args(args)

    # Getting the loaded data from the handler
    data = myais.get_data()


if __name__ == "__main__":
    __main__()
