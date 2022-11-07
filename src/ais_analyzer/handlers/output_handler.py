import pandas as pd


class OutputHandler:

    def __init__(self, path=None):
        self.path = path


    def output_csv(self, dataframe, sep=","):
        """
        :param dataframe: the input dataframe to convert to csv
        :param sep: the seperator

        """

        dataframe.to_csv(self.path, sep=sep, index=False)

