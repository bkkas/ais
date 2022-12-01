import pandas as pd
import pytest
from src.ais_analyzer.commands import portcalls


@pytest.fixture
def none_radius_args(tmp_path_factory):
    yield {
        'lat': 69.0,
        'lon': None,
        'radius': None,
        'polygon': None,
        'input_file': "tests/data/std_single_portcall.csv",
        'output_file': (tmp_path_factory.mktemp('temp') / "output.csv").__str__()
    }


@pytest.fixture
def valid_radius_args(tmp_path_factory):
    """Used for test datasets"""
    yield {
        'lat': 42.0,
        'lon': 42.0,
        'radius': 500,
        'polygon': None,
        'input_file': "tests/data/std_single_portcall.csv",
        'output_file': (tmp_path_factory.mktemp('temp') / "output.csv").__str__()
    }


@pytest.fixture
def missing_polygon_args(tmp_path_factory):
    """Too few coordinates"""
    yield {
        'lat': None,
        'lon': None,
        'radius': None,
        'polygon': [(41.999, 41.999), (42.001, 41.999)],
        'input_file': "tests/data/std_single_portcall.csv",
        'output_file': (tmp_path_factory.mktemp('temp') / "output.csv").__str__()
    }


@pytest.fixture
def invalid_polygon_args(tmp_path_factory):
    """Invalid polygon, lines drawn between points intersects"""
    yield {
        'lat': None,
        'lon': None,
        'radius': None,
        'polygon': [(41.999, 41.999), (42.001, 41.999), (41.999, 42.001), (42.001, 42.001)],
        'input_file': "tests/data/std_single_portcall.csv",
        'output_file': (tmp_path_factory.mktemp('temp') / "output.csv").__str__()
    }


@pytest.fixture
def valid_polygon_args(tmp_path_factory):
    """A valid polygon which contains (42, 42) """
    yield {
        'lat': None,
        'lon': None,
        'radius': None,
        'polygon': [(41.999, 41.999), (42.001, 41.999), (42.001, 42.001), (41.999, 42.001)],
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

    def test_input_fixtures(self, valid_radius_args):
        assert valid_radius_args['lat'] == 42.0
        assert valid_radius_args['polygon'] is None

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

    def test_input_validation_none(self, none_radius_args):
        """None args given """

        # For the radius+coordinate option
        with pytest.raises(KeyError) as exc_info:
            portcalls.validate_input_parameters(none_radius_args)
        nones = ['lon', 'radius']
        assert str(exc_info.value) == f'"Missing arguments for portcalls with radius option: {nones}"'

    def test_input_validation_polygon(self, missing_polygon_args, invalid_polygon_args):
        # Too few coordinates
        with pytest.raises(KeyError) as exc_info:
            portcalls.validate_input_parameters(missing_polygon_args)
        nr_given = 2
        assert str(exc_info.value) == f"'The minimum number of coordinates is three, {nr_given} was given'"

        # Invalid order of coordinates
        with pytest.raises(KeyError) as exc_info:
            portcalls.validate_input_parameters(invalid_polygon_args)

        assert str(exc_info.value) == "'The order of the coordinates given does not make up a valid polygon'"

    def test_one_portcall(self, single_portcall, valid_radius_args, valid_polygon_args):
        """
        Test on input dataframe with one vessel making one portcall
        MMSI: 6969
        """

        # Testing the radius input
        portcalled_rad = portcalls.portcalls(single_portcall, valid_radius_args)
        assert portcalled_rad.shape[0] == 1
        assert portcalled_rad.mmsi.iloc[0] == 6969

        # Testing the polygon input
        portcalled_poly = portcalls.portcalls(single_portcall, valid_polygon_args)
        assert portcalled_poly.shape[0] == 1
        assert portcalled_poly.mmsi.iloc[0] == 6969

    def test_double_portcalls(self, recurring_portcall, valid_radius_args, valid_polygon_args):
        """
        Test recurring traffic to port. One vessel, two portcalls
        MMSI: 9999
        """

        portcalled_rad = portcalls.portcalls(recurring_portcall, valid_radius_args)
        assert portcalled_rad.shape[0] == 2

        portcalled_poly = portcalls.portcalls(recurring_portcall, valid_polygon_args)
        assert portcalled_poly.shape[0] == 2

    def test_all_portcalls(self, all_portcalls, valid_radius_args, valid_polygon_args):
        """
        There should be three portcalls.
        Two vessels, one having two portcalls (MMSI: 9999)
        """
        portcalled_rad = portcalls.portcalls(all_portcalls, valid_radius_args)
        assert portcalled_rad.shape[0] == 3

        portcalled_poly = portcalls.portcalls(all_portcalls, valid_polygon_args)
        assert portcalled_poly.shape[0] == 3

    def test_no_portcalls(self, no_portcalls, valid_radius_args, valid_polygon_args):
        """
        When there are no portcalls there should be an empty dataframe (with sensible columns)
        Input dataframe contains vessel that transits the area
        """
        portcalled_rad = portcalls.portcalls(no_portcalls, valid_radius_args, )
        assert portcalled_rad.empty

        portcalled_poly = portcalls.portcalls(no_portcalls, valid_polygon_args)
        assert portcalled_poly.empty
