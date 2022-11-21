import pandas as pd
import logging
from ..logger.log_class import AisLogger
from .values import *

logging.setLoggerClass(AisLogger)


class InputHandler:
    logger = logging.getLogger("InputHandler")

    def __init__(self, path=None):
        self.path = path
        self.data = self._read_from_csv()
        self.dk_data = False

    def _infer_csv_sep(self, path: str) -> str:
        reader = pd.read_csv(path, sep=None, iterator=True, engine='python')
        sep = reader._engine.data.dialect.delimiter
        return sep

    def _get_needed_cols(self, sep: str) -> list:
        if sep == ';':
            return get_no_cols()
        if sep == ',':
            self.dk_data = True
            return get_dk_cols()

    def _standardize_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        col_std = get_standardized_cols()
        columns = list(df.columns)

        # replacing with standards
        for i, col in enumerate(columns):
            for key, value in col_std.items():
                if key in col.lower():
                    columns[i] = value

        df.columns = columns

        return df

    def _get_needed_dtypes(self, sep: str) -> dict:
        if sep == ';':
            return get_no_dtypes()
        if sep == ',':
            self.dk_data = True
            return get_dk_dtypes()

    def _simple_down_sampler(self, df: pd.DataFrame) -> pd.DataFrame:
        groups = df.groupby(df.columns[1])
        dfs = []
        for name, group_df in groups:
            reduced_df = group_df[~group_df['timestamp_utc'].dt.floor('30s').duplicated()]
            dfs.append(reduced_df)
        reduced_df = pd.concat(dfs).sort_index()
        return reduced_df

    def _remove_unknown(self, df: pd.DataFrame, dtypes: dict) -> pd.DataFrame:
        map = {"Under way using engine": 0,
               "At anchor": 1,
               "Not under command": 2,
               "Restricted maneuverability": 3,
               "Constrained by her draught": 4,
               "Moored": 5,
               "Aground": 6,
               "Engaged in fishing": 7,
               "Under way sailing": 8,
               "Reserved for future amendment [HSC]": 9,
               "Reserved for future amendment [WIG]": 10,
               "Power-driven vessel towing astern": 11,
               "Power-driven vessel pushing ahead or towing alongside": 12,
               "Reserved for future use": 13,
               "AIS-SART (active)": 14,
               "Unknown value": 15
        }
        df["Navigational status"] = df["Navigational status"].replace(to_replace=map)
        return df.astype(dtypes)

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
        if self.dk_data:
            input_df = pd.read_csv(self.path,
                                   sep=sep,
                                   usecols=columns,
                                   parse_dates=[columns[0]])

            input_df = self._remove_unknown(input_df, dtypes)
        else:
                input_df = pd.read_csv(self.path,
                                       sep=sep,
                                       usecols=columns,
                                       dtype=dtypes,
                                       parse_dates=[columns[0]])
        # Log memory usage before sampling
        self.logger.log_memory(input_df, "input_df")

        input_df = self._standardize_cols(input_df)
        # TODO assert this is correct @Sara
        input_df = self._simple_down_sampler(input_df)

        # Log memory usage after down-sampling
        self.logger.log_memory(input_df, "input_df", "Size of input_df when down-sampled")
        return input_df

    def get_data(self):
        return self.data
