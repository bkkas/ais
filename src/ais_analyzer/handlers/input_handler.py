import pandas as pd
from .values import *


class InputHandler:

    def __init__(self, path=None):
        self.path = path
        self.data = self._read_from_csv()

    def _infer_csv_sep(self, path) -> str:
        reader = pd.read_csv(path, sep=None, iterator=True, engine='python')
        sep = reader._engine.data.dialect.delimiter
        return sep

    def _get_needed_cols(self, sep) -> list:
        if sep == ';':
            return get_no_cols()
        if sep == ',':
            return get_dk_cols()

    def _standardize_cols(self, df) -> pd.DataFrame:
        col_std = get_standardized_cols()
        columns = list(df.columns)

        # replacing with standards
        for i, col in enumerate(columns):
            for key, value in col_std.items():
                if key in col:
                    columns[i] = value

        df.columns = columns

        return df

    def _get_needed_dtypes(self, sep) -> dict:
        if sep == ';':
            return get_no_dtypes()
        if sep == ',':
            return get_dk_dtypes()

    def _simple_down_sampler(self, df) -> None:
        groups = df.groupby(df.columns[1])
        dfs = []
        for name, group_df in groups:
            reduced_df = group_df[~group_df['timestamp_utc'].dt.floor('30s').duplicated()]
            dfs.append(reduced_df)
        reduced_df = pd.concat(dfs).sort_index()
        return reduced_df

    def _read_from_csv(self) -> pd.DataFrame:

        # TODO:
        #  standardize column names
        #  down sampling, make better strategy
        #       - remove all boat above/below certain values
        #       - ?
        #  chunking

        sep = self._infer_csv_sep(self.path)
        columns = self._get_needed_cols(sep=sep)
        dtypes = self._get_needed_dtypes(sep=sep)

        input_df = pd.read_csv(self.path,
                               sep=sep,
                               usecols=columns,
                               dtype=dtypes,
                               parse_dates=[columns[0]])

        input_df = self._standardize_cols(input_df)

        self._simple_down_sampler(input_df)
        return input_df

    def get_data(self):
        return self.data
