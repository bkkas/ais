import pytest
from src.ais_analyzer.handlers import input_handler
import pandas as pd


@pytest.fixture
def norwegian_data():
    return "tests/data/no_test_data_vestland_10k_rows.csv"

@pytest.fixture
def danish_data():
    return "tests/data/dk_test_data_10k_rows.csv"

class TestCase:
    def test_something(self):
        assert True  # add assertion here

    '''
    TODO:      
        - col reduction
        - std col names
        - dtypes
        - check number of occurances,(down sampler, 30 sec)
        - check nan (remove unknowns)
        
    '''

    def test_infer_sep_no(self, norwegian_data):
        handler = input_handler.InputHandler()
        assert handler._infer_csv_sep(path=norwegian_data) == ';'

    def test_infer_sep_dk(self, danish_data):
        handler = input_handler.InputHandler()
        assert handler._infer_csv_sep(path=danish_data) == ','
