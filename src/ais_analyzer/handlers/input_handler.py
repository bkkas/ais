import pandas as pd
from .values import *


class InputHandler:

    def __init__(self, path=None, sep=None, columns=None, df=None, dtypes=None):
        self.dtypes = dtypes
        self.path = path
        self.sep = sep
        self.columns = columns
        self.df = df

    def check_csv_sep(self) -> None:
        sep = self.sep
        path = self.path
        if sep != ',':
            self.sep = sep
            return
        df = pd.read_csv(self.path, sep=self.sep, nrows=1)
        nr_col = df.shape[1]
        if nr_col == 1:  # norwegian data
            self.sep = ';'
        return

    def get_needed_cols(self) -> None:
        if self.sep == ';':
            self.columns = get_no_cols()
        if self.sep == ',':
            self.columns = get_dk_cols()

    def get_needed_dtypes(self) -> None:
        if self.sep == ';':
            self.dtypes = get_no_dtypes()
        if self.sep == ',':
            self.dtypes = get_dk_dtypes()

    def simple_down_sampler(self) -> None:
        groups = self.df.groupby(self.df.columns[1])
        dfs = []
        for name, group_df in groups:
            reduced_df = group_df[~group_df[self.columns[0]].dt.floor('30s').duplicated()]
            dfs.append(reduced_df)
        reduced_df = pd.concat(dfs).sort_index()
        self.df = reduced_df

    def read_from_csv(self, path, sep=",") -> pd.DataFrame:
        """
        :param sep: the separator, string
        :param path: the path to the csv file, string
        :return: a dataframe object
        """

        # TODO's:
        #  support for danish and norwegian datasets,
        #  colreduce, OK
        #  downsampling,
        #  downcasting, OK
        if not self.sep:
            self.sep = sep
        self.path = path
        self.check_csv_sep()
        self.get_needed_cols()
        self.get_needed_dtypes()

        self.df = pd.read_csv(self.path,
                              sep=self.sep,
                              usecols=self.columns,
                              dtype=self.dtypes,
                              parse_dates=[self.columns[0]])
        self.simple_down_sampler()
        return self.df

