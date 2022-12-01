import pandas as pd
import pytest

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
        assert country_mmsi.country == "Denmark"
        assert country_mmsi.nr_unique_ships == 1
        assert country_mmsi.nr_rows == 45
