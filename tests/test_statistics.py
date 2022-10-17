import pytest
import pandas as pd
from src.ais_analyzer.commands import statistics as st


# Read danish dataset
@pytest.fixture
def read_dk() -> pd.DataFrame:
    path = "tests/data/dk_test_data_10k_rows.csv"
    yield pd.read_csv(path)


# Read norwegian dataset
@pytest.fixture
def read_no() -> pd.DataFrame:
    path = "tests/data/no_test_data_vestland_10k_rows.csv"
    yield pd.read_csv(path, sep=';')


class TestCaseNorwegian:

    # Test that the full statistics method is equivalent with .describe
    def test_statistics_no(self, read_no):
        assert st.statistics(read_no, {'full': True}).equals(read_no.describe(include="all"))


class TestCaseDanish:

    # Test that the full statistics method is equivalent with .describe
    def test_something(self, read_dk):
        assert st.statistics(read_dk, {'full': True}).equals(read_dk.describe(include="all"))
