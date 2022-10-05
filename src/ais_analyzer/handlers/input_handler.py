import pandas as pd


class InputHandler:

    def __init__(self, path: str):
        self.path = path

    def read_csv(self, sep=",") -> pd.DataFrame:
        """
        :param sep: the seperator
        :return: a dataframe object
        """

        df = pd.read_csv(self.path, sep)
        return df
