import pandas as pd
import pytest
from src.ais_analyzer.commands import statistics

@pytest.fixture
def country_arg():
    return 'country'

@pytest.fixture
def single_mmsi():
    df = pd.read_csv("tests/data/std_single_portcall.csv")
    yield df

class TestCase:
    def test_single_mmsi(self, single_mmsi, country_arg):
        df = single_mmsi
        country_mmsi = statistics.statistics(single_mmsi, country_arg)
        assert len(df.rows) == 1
        assert country_mmsi.country[0] == "Denmark"
        assert country_mmsi.nr_unique_ships[0] == 1
        assert country_mmsi.nr_rows[0] == 45
