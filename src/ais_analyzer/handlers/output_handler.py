import pandas as pd


class OutputHandler:

    def __init__(self):

        self.to_csv()

    def to_csv(self, path, dataframe, sep=","):
        """
        :param sep: the seperator

        """

        dataframe.to_csv(self.path, sep)

