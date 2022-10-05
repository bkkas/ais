import pandas as pd


class OutputHandler:

    def __init__(self, path: str):
        self.path = path

        self.to_csv()

    def to_csv(self, sep=","):
        """
        :param sep: the seperator

        """

        df.to_csv(self.path, sep)

