import pandas as pd


class InputHandler:

    def __init__(self, path=None):
        self.path = path

    def read_from_csv(self, path, sep=",") -> pd.DataFrame:
        """
        :param sep: the seperator
        :return: a dataframe object
        """

        df = pd.read_csv(path, sep)
        return df
