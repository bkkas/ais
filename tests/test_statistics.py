import pandas as pd
import pytest
from src.ais_analyzer.commands import statistics

@pytest.fixture
def args_country():
    yield {
        'full': False,
        'mmsi': False,
        'country': True,
        'complete': False,
    }

@pytest.fixture
def args_mmsi():
    yield {
        'full': False,
        'mmsi': True,
        'country': False,
        'complete': False,
    }

@pytest.fixture
def args_complete():
    yield {
        'full': False,
        'mmsi': False,
        'country': False,
        'complete': True,
    }

@pytest.fixture
def country_arg():
    yield {'args' : 'country'}

@pytest.fixture
def single_mmsi():
    df = pd.read_csv("tests/data/std_single_portcall.csv")
    yield df

@pytest.fixture
def stat_mmsi():
    df = pd.read_csv("tests/data/std_statistics_test.csv")
    yield df

class TestCase:
    def test_single_mmsi_country(self, single_mmsi, args_country):
        df = single_mmsi
        country_mmsi = statistics.statistics(df, args_country)
        assert len(country_mmsi) == 1
        assert country_mmsi.country[0] == "Denmark"
        assert country_mmsi.nr_unique_ships[0] == 1
        assert country_mmsi.nr_rows[0] == 44

    def test_single_mmsi_mmsi(self, single_mmsi, args_mmsi):
        df = single_mmsi
        mmsi_mmsi = statistics.statistics(df, args_mmsi)
        assert len(mmsi_mmsi) == 1
        assert mmsi_mmsi.mmsi[0] == 219016713
        assert str(mmsi_mmsi.first_oc[0]) == "2022-08-05 10:00:00"
        assert str(mmsi_mmsi.last_oc[0]) == "2022-08-05 14:05:00"
        assert mmsi_mmsi.length[0] == 100
        assert mmsi_mmsi.count_rows[0] == 44

    def test_single_mmsi_complete(self, single_mmsi, args_complete):
        df = single_mmsi
        mmsi_complete = statistics.statistics(df, args_complete)
        assert len(mmsi_complete) == 1
        assert mmsi_complete.avg_length[0] == 100
        assert mmsi_complete.max_length[0] == 100
        assert mmsi_complete.min_length[0] == 100
        assert str(mmsi_complete.start_date[0]) == "2022-08-05 10:00:00"
        assert str(mmsi_complete.end_date[0]) == "2022-08-05 14:05:00"
        assert mmsi_complete.median_lon[0] == 42
        assert mmsi_complete.median_lat[0] == 42

    def test_stat_mmsi_country(self, stat_mmsi, args_country):
        df = stat_mmsi
        country_mmsi = statistics.statistics(df, args_country)
        assert len(country_mmsi) == 5
        countries = ["Denmark", "France", "Ireland", "Malta", "Spain"]
        country_mmsi.country[0] == "Denmark"
        print(country_mmsi.head())
        for i in range(len(countries)):
            assert country_mmsi.country[i] == countries[i]
        assert country_mmsi.nr_unique_ships[0] == 2
        assert country_mmsi.nr_unique_ships[1] == 3
        assert country_mmsi.nr_unique_ships[2] == 1
        assert country_mmsi.nr_rows[0] == 24
        assert country_mmsi.nr_rows[1] == 3
        assert country_mmsi.nr_rows[2] == 70
    
    def test_single_mmsi_mmsi(self, stat_mmsi, args_mmsi):
        df = stat_mmsi
        mmsi_mmsi = statistics.statistics(df, args_mmsi)
        assert len(mmsi_mmsi) == 9
        assert mmsi_mmsi.mmsi[0] == 219016713
        assert str(mmsi_mmsi.first_oc[0]) == "2022-08-05 06:00:00"
        assert str(mmsi_mmsi.last_oc[0]) == "2022-08-06 05:00:00"
        assert str(mmsi_mmsi.first_oc[2]) == "2022-08-05 11:00:00"
        assert str(mmsi_mmsi.last_oc[2]) == "2022-08-05 11:00:00"
        assert mmsi_mmsi.length[0] == 100
        assert mmsi_mmsi.length[2] == 105
        assert mmsi_mmsi.count_rows[0] == 20
        assert mmsi_mmsi.count_rows[8] == 70

    def test_single_mmsi_complete(self, stat_mmsi, args_complete):
        df = stat_mmsi
        mmsi_complete = statistics.statistics(df, args_complete)
        assert len(mmsi_complete) == 1
        assert mmsi_complete.mmsi_count[0] == 9
        assert mmsi_complete.avg_length[0] == 117.33333333333333
        assert mmsi_complete.max_length[0] == 210
        assert mmsi_complete.min_length[0] == 100
        assert str(mmsi_complete.start_date[0]) == "2022-08-05 06:00:00"
        assert str(mmsi_complete.end_date[0]) == "2022-08-06 05:00:00"
        assert mmsi_complete.median_lat[0] == 50.5
        assert mmsi_complete.median_lon[0] == 50.5
