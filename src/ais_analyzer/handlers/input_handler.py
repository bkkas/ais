import pandas as pd
import values


def check_csv_sep(path, sep) -> str:
    if sep != ',':
        return sep
    df = pd.read_csv(path, sep=sep, nrows=1)
    nr_col = df.shape[1]
    if nr_col == 1:  # norwegian data
        sep = ';'
    return sep


class InputHandler:

    def __init__(self, path=None, value=None):
        self.path = path
        self.value = values()

    def read_from_csv(self, path, sep=",") -> pd.DataFrame:
        """
        :param sep: the separator, string
        :param path: the path to the csv file, string
        :return: a dataframe object
        """

        # TODO's:
        #  support for danish and norwegian datasets,
        #  colreduce,
        #  downsampling,
        #  downcasting
        sep = check_csv_sep(path, sep)
        columns = self.get_needed_cols(sep)

        df = pd.read_csv(path, sep=sep, usecols=columns)
        return df

    def get_needed_cols(self, sep) -> list:

        if sep == ';':
            return self.value.get_no_cols()
        if sep == ',':
            return self.value.get_dk_cols()
