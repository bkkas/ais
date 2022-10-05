from tabnanny import check
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
        sep = self.check_csv_sep(path,sep)

        df = pd.read_csv(path, sep=sep)
        return df

    def check_csv_sep(self, path,sep) -> str:
        if sep!=',':
            return sep
        df= pd.read_csv(path, sep=sep, nrows=1)
        nr_col = df.shape[1]
        if nr_col==1:   #norwegian data
            sep=';'
        return sep
