import pandas as pd


class OutputHandler:

    def __init__(self, path=None):
        self.path = path

    def output_terminal(self, dataframe: pd.DataFrame) -> None:
        """
        Outputs a dataframe to the terminal

        :param dataframe: the dataframe to be printed to terminal
        :return:
        """
        print(dataframe)

    def output_csv(self, dataframe: pd.DataFrame, sep=",") -> None:
        """
        Outputs the dataframe to a CSV file, if there is a desire to keep
        the data that was generated.

        :param dataframe: the input dataframe to convert to csv
        :param sep: the seperator
        """

        dataframe.to_csv(self.path, sep=sep, index=False)

