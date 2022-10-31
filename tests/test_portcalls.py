import pandas as pd
import pytest
from src.ais_analyzer.commands import portcalls

"""
The hardcoded column names in "portcalls" are assumed to be independent of data country origin
So we need to make sure any formatting/standardizing of the dataframes are done in the input_handler
"""


@pytest.fixture
def args_(tmp_path_factory):
    arguments = {
        'input_file': "tests/data/std_test_portcalls.csv",
        'output_file': (tmp_path_factory.mktemp('temp') / "output.csv").__str__()
    }
    yield arguments


@pytest.fixture
def none_input():
    yield {
        'lat': 69.0,
        'lon': None,
        'radius': None
    }


@pytest.fixture
def valid_input():
    yield {
        'lat': 42.0,
        'lon': 42.0,
        'radius': 500

    }


@pytest.fixture
def none_args(none_input, args_):
    args = args_
    inpt = none_input
    args.update(inpt)
    yield args


@pytest.fixture
def valid_args(valid_input, args_):
    args = args_
    inpt = valid_input
    args.update(inpt)
    yield args


@pytest.fixture
def port42df(valid_args):
    path = valid_args['input_file']
    port42 = pd.read_csv(path)
    yield port42


class TestCase:

    def test_input_fixtures(self, valid_args):
        assert valid_args['lat'] == 42.0

    def test_input_dataframe(self, port42df):
        test_col_names = ['timestamp_utc', 'mmsi', 'lat', 'lon', 'nav_status','sog','imo','callsign','ship_type','cargo_type', 'width', 'length', 'draught','dest']
        assert len(port42df.columns) == 14
        assert list(port42df.columns) == test_col_names
        assert port42df.shape[0] == 10

    def test_input_validation(self, none_args):
        # None
        with pytest.raises(KeyError) as exc_info:
            portcalls.validate_input_parameters(none_args)
        print(f"exc_info:{exc_info.value}")
        nones = ['lon', 'radius']
        assert str(exc_info.value) == f'"Missing arguments for portcalls: {nones}"'


    def test_portcalls(self, port42df, valid_args):
        portcalled = portcalls.portcalls(port42df, valid_args)

        assert portcalled.shape[0] == 1
