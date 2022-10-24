import pandas as pd
from .values import *


def check_csv_sep(path, sep) -> str:
    if sep != ',':
        return sep
    df = pd.read_csv(path, sep=sep, nrows=1)
    nr_col = df.shape[1]
    if nr_col == 1:  # norwegian data
        sep = ';'
    return sep


def get_needed_cols(sep) -> list:
    if sep == ';':
        return get_no_cols()
    if sep == ',':
        return get_dk_cols()


def get_needed_dtypes(sep) -> dict:
    if sep == ';':
        return get_no_dtypes()
    if sep == ',':
        return get_dk_dtypes()


def simple_down_sampler(df) -> pd.DataFrame:
    groups = df.groupby(df.columns[1])
    dfs = []
    for name, group_df in groups:
        reduced_df = group_df[~group_df['# Timestamp'].dt.floor('30s').duplicated()]
        dfs.append(reduced_df)
    reduced_df = pd.concat(dfs).sort_index()
    return reduced_df


class InputHandler:

    def __init__(self, path=None, sep=None, columns=None, df=None, dtypes=None):
        self.dtypes = dtypes
        self.path = path
        self.sep = sep
        self.columns = columns
        self.df = df

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
        self.path = path
        sep = check_csv_sep(path, sep)
        self.sep = sep
        columns = get_needed_cols(sep)
        self.columns = columns
        dts = get_needed_dtypes(sep)
        self.dtypes = dts

        df = pd.read_csv(path, sep=sep, usecols=columns, dtype=dts, parse_dates=[columns[0]])
        df = simple_down_sampler(df)
        self.df = df
        return df

