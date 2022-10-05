import pandas as pd


class InputHandler:

    def __init__(self, path=None):
        self.path = path

    def read_from_csv(self, path, sep=",") -> pd.DataFrame:
        """
        :param sep: the seperator
        :return: a dataframe object
        """


        # TODO's:
        #  support for danish and norwegian datasets,
        #  colreduce,
        #  downsampling,
        #  downcasting

        df = pd.read_csv(path, sep)
        return df
