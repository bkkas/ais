import pytest
from src.ais_analyzer.handlers import input_handler
import pandas as pd


@pytest.fixture
def handler():
    return input_handler.InputHandler()


@pytest.fixture
def norwegian_data():
    return "tests/data/no_test_data_vestland_10k_rows.csv"


@pytest.fixture
def danish_data():
    return "tests/data/dk_test_data_10k_rows.csv"


@pytest.fixture
def duplicate_data():
    return "tests/data/duplicate_rows.csv"


@pytest.fixture
def same_vessel_10_rows_1sec_increment_crossing_a_min_data():
    return "tests/data/same_vessle_1sec_increments.csv"


@pytest.fixture
def same_vessel_30_sec_increments_data():
    return "tests/data/30_sec_gap_same_vessel.csv"


@pytest.fixture
def two_vessels_v1_4times_v2_3times_data():
    return "tests/data/2_vessels_v1_4occurances_v2_3occurances.csv"


@pytest.fixture
def dk_2_vessels_v1_2occurances_v2_4occurances():
    return "tests/data/dk_2_vessels_v1_2occurances_v2_4occurances.csv"


class TestCase:
    def test_something(self):
        assert True  # add assertion here


    def test_infer_sep_no(self, norwegian_data, handler):
        assert handler._infer_csv_sep(path=norwegian_data) == ';'

    def test_infer_sep_dk(self, danish_data, handler):
        assert handler._infer_csv_sep(path=danish_data) == ','

    def test_get_needed_cols(self, handler):
        assert handler._get_needed_cols(';') == input_handler.get_no_cols()
        assert not handler.dk_data
        assert handler._get_needed_cols(',') == input_handler.get_dk_cols()
        assert handler.dk_data

    def test_get_needed_dtypes(self, handler):
        assert handler._get_needed_dtypes(';') == input_handler.get_no_dtypes()
        assert not handler.dk_data
        assert handler._get_needed_dtypes(',') == input_handler.get_dk_dtypes()
        assert handler.dk_data

    def test_std_col_names_no(self, norwegian_data):
        handler = input_handler.InputHandler(path=norwegian_data)
        handler.read_data()
        std_cols = ['timestamp_utc', 'mmsi', 'imo', 'lat', 'lon', 'nav_status', 'dest', 'length',
                    'draught', 'width', 'sog', 'ship_type', 'cargo_type', 'name', 'callsign', 'cog']
        df = handler.get_data()
        print('no', df.columns)
        for col in df.columns:
            assert col in std_cols
        assert len(df.columns) == 7
        assert list(df.columns) == ['mmsi', 'length', 'timestamp_utc', 'lon', 'lat', 'sog', 'nav_status']

    def test_std_col_names_dk(self, danish_data):
        handler = input_handler.InputHandler(path=danish_data)
        handler.read_data()
        std_cols = ['timestamp_utc', 'mmsi', 'imo', 'lat', 'lon', 'nav_status', 'dest', 'length',
                    'draught', 'width', 'sog', 'ship_type', 'cargo_type', 'name', 'callsign', 'cog']
        df = handler.get_data()
        print('dk', df.columns)
        for col in df.columns:
            assert col in std_cols
        assert len(df.columns) == 16
        assert list(df.columns) == ['timestamp_utc', 'mmsi', 'lat', 'lon', 'nav_status', 'sog', 'cog',
                                    'imo', 'callsign', 'name', 'ship_type', 'cargo_type', 'width', 'length',
                                    'draught', 'dest']


    def test_down_sampler_duplicates_no(self, duplicate_data):
        df = pd.read_csv(duplicate_data, sep=';')
        assert df.shape[0] == 10
        handler = input_handler.InputHandler(path=duplicate_data)
        handler.read_data()
        assert handler.get_data().shape[0] == 1

    def test_down_sampler_change_minute_no(self, same_vessel_10_rows_1sec_increment_crossing_a_min_data):
        df = pd.read_csv(same_vessel_10_rows_1sec_increment_crossing_a_min_data, sep=';')
        assert df.shape[0] == 10
        handler = input_handler.InputHandler(path=same_vessel_10_rows_1sec_increment_crossing_a_min_data)
        handler.read_data()
        assert handler.get_data().shape[0] == 2

    def test_down_sampler_one_row_a_min_no(self, same_vessel_30_sec_increments_data):
        df = pd.read_csv(same_vessel_30_sec_increments_data, sep=';')
        assert df.shape[0] == 10
        handler = input_handler.InputHandler(path=same_vessel_30_sec_increments_data)
        handler.read_data()
        assert handler.get_data().shape[0] == 10

    def test_down_sampler_v1_4times_v2_3times_no(self, two_vessels_v1_4times_v2_3times_data):
        df = pd.read_csv(two_vessels_v1_4times_v2_3times_data, sep=';')
        assert df.shape[0] == 19
        handler = input_handler.InputHandler(path=two_vessels_v1_4times_v2_3times_data)
        handler.read_data()
        df = handler.get_data()
        assert df.shape[0] == 4 + 3
        v1 = df.loc[df.mmsi == 257786980]
        v2 = df.loc[df.mmsi == 257812000]
        assert v1.shape[0] == 4
        assert v2.shape[0] == 3

    def test_down_sampler_v1_2times_v2_4times_dk(self, dk_2_vessels_v1_2occurances_v2_4occurances):
        df = pd.read_csv(dk_2_vessels_v1_2occurances_v2_4occurances)
        assert df.shape[0] == 18
        handler = input_handler.InputHandler(path=dk_2_vessels_v1_2occurances_v2_4occurances)
        handler.read_data()
        df = handler.get_data()
        assert df.shape[0] == 2 + 4
        v1 = df.loc[df.mmsi == 219007225]
        v2 = df.loc[df.mmsi == 219024000]
        assert v1.shape[0] == 2
        assert v2.shape[0] == 4
