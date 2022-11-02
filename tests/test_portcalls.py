import pandas as pd
import pytest
from src.ais_analyzer.commands import portcalls

"""
The hardcoded column names in "portcalls" are assumed to be independent of data country origin
So we need to make sure any formatting/standardizing of the dataframes are done in the input_handler
"""


@pytest.fixture
def none_args(tmp_path_factory):
    yield {
        'lat': 69.0,
        'lon': None,
        'radius': None,
        'input_file': "tests/data/std_test_portcalls.csv",
        'output_file': (tmp_path_factory.mktemp('temp') / "output.csv").__str__()
    }


@pytest.fixture
def valid_args(tmp_path_factory):
    """Used for test datasets"""
    yield {
        'lat': 42.0,
        'lon': 42.0,
        'radius': 500,
        'input_file': "tests/data/std_test_portcalls.csv",
        'output_file': (tmp_path_factory.mktemp('temp') / "output.csv").__str__()
    }


@pytest.fixture
def single_portcall(tmp_path_factory):
    df = pd.read_csv("data/std_single_portcall.csv")
    yield df

@pytest.fixture
def recurring_vessel_portcall(tmp_path_factory):
    df = pd.read_csv("data/std_double_portcall.csv")
    yield df


class TestCase:

    def test_input_fixtures(self, valid_args):
        assert valid_args['lat'] == 42.0

    def test_single_portcall_dataframe(self, single_portcall):
        df = single_portcall
        test_col_names = ['timestamp_utc', 'mmsi', 'lat', 'lon', 'nav_status', 'sog', 'imo', 'callsign', 'ship_type',
                          'cargo_type', 'width', 'length', 'draught', 'dest']
        assert len(df.columns) == 14
        assert list(df.columns) == test_col_names
        assert df.shape[0] == 10

    def test_double_portcall_dataframe(self, recurring_vessel_portcall):
        df = recurring_vessel_portcall
        test_col_names = ['timestamp_utc', 'mmsi', 'lat', 'lon', 'nav_status', 'sog', 'imo', 'callsign', 'ship_type',
                          'cargo_type', 'width', 'length', 'draught', 'dest']
        assert len(df.columns) == 14
        assert list(df.columns) == test_col_names
        assert df.shape[0] == 11

    def test_all_portcalls_dataframe(self, all_portcall):
        df = all_portcall
        test_col_names = ['timestamp_utc', 'mmsi', 'lat', 'lon', 'nav_status', 'sog', 'imo', 'callsign', 'ship_type',
                          'cargo_type', 'width', 'length', 'draught', 'dest']
        assert len(df.columns) == 14
        assert list(df.columns) == test_col_names
        assert df.shape[0] == 16

    def test_input_validation(self, none_args):
        # None
        with pytest.raises(KeyError) as exc_info:
            portcalls.validate_input_parameters(none_args)
        print(f"exc_info:{exc_info.value}")
        nones = ['lon', 'radius']
        assert str(exc_info.value) == f'"Missing arguments for portcalls: {nones}"'

    def test_one_portcall(self, single_portcall, valid_args):
        """
        Test simple synthetic portcall
        Will only show first and last visit to port
        Does not capture multiple visits

        """

        portcalled = portcalls.portcalls(single_portcall, valid_args)
        assert portcalled.shape[0] == 1

    def test_recurring_portcalls(self, recurring_vessel_portcall, valid_args):
        """
        Test recurring traffic to port

        Scenarios:
        - Vessel has at least two visits
        """

        portcalled = portcalls.portcalls(recurring_vessel_portcall, valid_args)
        assert portcalled.shape[0] == 2
