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


class TestCase:
    def test_something(self):
        assert True  # add assertion here


    # TODO:
    #      std col names
    #     - check number of occurances,(down sampler, 30 sec)
    #         - check with dk data
    #         - check with multiple vessels
    #     - check nan (remove unknowns)
        


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



    def test_down_sampler(self,
                          duplicate_data,
                          same_vessel_10_rows_1sec_increment_crossing_a_min_data,
                          same_vessel_30_sec_increments_data,
                          ):
        handler = input_handler.InputHandler(path=duplicate_data)
        handler.read_data()
        assert handler.get_data().shape[0] == 1
        handler = input_handler.InputHandler(path=same_vessel_10_rows_1sec_increment_crossing_a_min_data)
        handler.read_data()
        assert handler.get_data().shape[0] == 2
        handler = input_handler.InputHandler(path=same_vessel_30_sec_increments_data)
        handler.read_data()
        assert handler.get_data().shape[0] == 10
