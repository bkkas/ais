import pandas as pd
import pytest
from src.ais_analyzer.commands import portcalls


@pytest.fixture
def none_args(tmp_path_factory):
    yield {
        'lat': 69.0,
        'lon': None,
        'radius': None,
        'input_file': "tests/data/std_single_portcall.csv",
        'output_file': (tmp_path_factory.mktemp('temp') / "output.csv").__str__()
    }


@pytest.fixture
def valid_args(tmp_path_factory):
    """Used for test datasets"""
    yield {
        'lat': 42.0,
        'lon': 42.0,
        'radius': 500,
        'input_file': "tests/data/std_single_portcall.csv",
        'output_file': (tmp_path_factory.mktemp('temp') / "output.csv").__str__()
    }


@pytest.fixture
def single_portcall():
    df = pd.read_csv("tests/data/std_single_portcall.csv")
    yield df


@pytest.fixture
def recurring_portcall():
    df = pd.read_csv("tests/data/std_double_portcall.csv")
    yield df


@pytest.fixture
def all_portcalls():
    df = pd.read_csv("tests/data/std_all_portcalls.csv")
    yield df


@pytest.fixture
def no_portcalls():
    df = pd.read_csv("tests/data/std_no_portcall.csv")
    yield df


class TestPortcalls:

    def test_input_fixtures(self, valid_args):
        assert valid_args['lat'] == 42.0

    def test_single_portcall_dataframe(self, single_portcall):
        df = single_portcall
        test_col_names = ['timestamp_utc', 'mmsi', 'lat', 'lon', 'nav_status', 'sog', 'imo', 'callsign', 'ship_type',
                          'cargo_type', 'width', 'length', 'draught', 'dest']
        assert len(df.columns) == 14
        assert list(df.columns) == test_col_names
        assert df.shape[0] == 44

    def test_double_portcall_dataframe(self, recurring_portcall):
        df = recurring_portcall
        test_col_names = ['timestamp_utc', 'mmsi', 'lat', 'lon', 'nav_status', 'sog', 'imo', 'callsign', 'ship_type',
                          'cargo_type', 'width', 'length', 'draught', 'dest']
        assert len(df.columns) == 14
        assert list(df.columns) == test_col_names

    def test_all_portcalls_dataframe(self, all_portcalls):
        df = all_portcalls
        test_col_names = ['timestamp_utc', 'mmsi', 'lat', 'lon', 'nav_status', 'sog', 'imo', 'callsign', 'ship_type',
                          'cargo_type', 'width', 'length', 'draught', 'dest']
        assert len(df.columns) == 14
        assert list(df.columns) == test_col_names

    def test_input_validation(self, none_args):
        # None
        with pytest.raises(KeyError) as exc_info:
            portcalls.validate_input_parameters(none_args)
        print(f"exc_info:{exc_info.value}")
        nones = ['lon', 'radius']
        assert str(exc_info.value) == f'"Missing arguments for portcalls: {nones}"'

    def test_one_portcall(self, single_portcall, valid_args):
        """
        Test on input dataframe with one vessel making one portcall
        MMSI: 6969
        """

        portcalled = portcalls.portcalls(single_portcall, valid_args)
        assert portcalled.shape[0] == 1
        assert portcalled.mmsi.iloc[0] == 6969

    def test_double_portcalls(self, recurring_portcall, valid_args):
        """
        Test recurring traffic to port. One vessel, two portcalls
        MMSI: 9999
        """

        portcalled = portcalls.portcalls(recurring_portcall, valid_args)
        assert portcalled.shape[0] == 2

    def test_all_portcalls(self, all_portcalls, valid_args):
        """
        There should be three portcalls.
        Two vessels, one having two portcalls (MMSI: 9999)
        """
        portcalled = portcalls.portcalls(all_portcalls, valid_args)
        assert portcalled.shape[0] == 3

    def test_no_portcalls(self, no_portcalls, valid_args):
        """
        When there are no portcalls there should be an empty dataframe (with sensible columns)
        Input dataframe contains vessel that transits the area
        """
        portcalled = portcalls.portcalls(no_portcalls, valid_args)
        assert portcalled.empty
