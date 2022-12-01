import pandas as pd
import numpy as np
import geopy
import geopy.distance as gpd
from shapely.geometry import Point, Polygon
from typing import Tuple
import logging
from ..logger.log_class import AisLogger

# Initiates a logger with a custom logger class
# Has to be called before the logger is constructed
logging.setLoggerClass(AisLogger)
logger_ = logging.getLogger("portcalls")


def validate_input_parameters(args):
    _required_list_rad = ['lat', 'lon', 'radius']
    _required_list_poly = ['polygon']

    _args_rad = [args[arg] for arg in _required_list_rad]
    _args_poly = [args[arg] for arg in _required_list_poly]

    # Check if polygon is not given
    if None in _args_poly:

        # Check if radius and center coordinates are given
        _missing = [arg for arg, present in zip(_required_list_rad, _args_rad) if not present]
        if _missing:
            # This could also mean there are no inputs for either radius or poly
            raise KeyError(f"Missing arguments for portcalls with radius option: {_missing}")

    else:
        # Polygon is given
        # Minimum number of geographical coordinates to make a polygon is three
        coords = args['polygon']
        if len(coords) < 3:
            raise KeyError(f"The minimum number of coordinates is three, {len(coords)} was given")

        # Check if order of coordinates makes up a valid polygon
        coords = [coord[::-1] for coord in coords]
        if Polygon(coords).is_valid is False:
            raise KeyError(f"The order of the coordinates given does not make up a valid polygon")

        # Only support for north-east hemisphere per now
        # The lat coordinates can be -90 to 90, longitude can be -180 to 180 (W and S is negative)
        for lat, lon in coords:
            if (lat > 90) or (lat < -90):
                raise KeyError(f"Latitude can not exceed 90 degrees")
            if (lon > 180) or (lon < -180):
                raise KeyError(f"Longitude can not exceed 180 degrees")


def vessels_in_radius(df: pd.DataFrame, point: tuple, radius: float) -> pd.DataFrame:
    """

    :param df: Input dataframe containing rows with coordinates
    :param point: a center coordinate point
    :param radius: a radius
    :return: A dataframe containing the rows within the specified circle
    """
    logger = logger_.getChild("vessels_in_radius")
    # 1.1 Check if within square (cheap).

    # First we get the N/E/S/W bounds of the square
    center = geopy.Point(*point)
    n_b = gpd.distance(meters=radius).destination(center, bearing=0)
    e_b = gpd.distance(meters=radius).destination(center, bearing=90)
    s_b = gpd.distance(meters=radius).destination(center, bearing=180)
    w_b = gpd.distance(meters=radius).destination(center, bearing=270)

    # Boolean masks
    n_mask = df['lat'] < n_b[0]
    e_mask = df['lon'] < e_b[1]
    s_mask = df['lat'] > s_b[0]
    w_mask = df['lon'] > w_b[1]

    mask_lat = np.logical_and(n_mask, s_mask)
    mask_lon = np.logical_and(w_mask, e_mask)
    mask = np.logical_and(mask_lat, mask_lon)

    # Get all entries within the square
    df = df.loc[mask]

    # 2.2 If within square, calculate if in radius (more expensive)
    def get_point_distance_center(_latlon: Tuple[float]) -> float:
        """
        :param _latlon:
        :return distance from center:
        """

        _point = geopy.Point(*_latlon)
        # As long as radius is provided in meter
        # Then this should be meter as well
        return gpd.distance(center, _point).m

    # Create a latlon tuple-like series and calculate a bool mask for vessels in radius
    latlon = pd.Series(zip(df.loc[:, 'lat'], df.loc[:, 'lon']))
    vessels_in_rad_bool = (latlon.map(get_point_distance_center) <= radius).tolist()
    df = df.loc[vessels_in_rad_bool]

    return df


def vessels_in_polygon(input_df: pd.DataFrame, coordinates: list) -> pd.DataFrame:
    """

    :param input_df: A dataframe containing input vessels
    :param coordinates: a list of tuples containing (latitude, longitude) coordinates making up a polygon
    :return: the vessels in the input dataframe which are within the given polygon
    """
    # FIRST PART
    # First we check if vessels within square (cheap)
    # We get the "bounding box" made up of the extreme in west-east-north-south directions
    n_bound = coordinates[0][0]
    s_bound = coordinates[0][0]
    w_bound = coordinates[0][1]
    e_bound = coordinates[0][1]

    for lat, lon in coordinates:
        if lat < s_bound:
            s_bound = lat
        if lat > n_bound:
            n_bound = lat
        if lon < w_bound:
            w_bound = lon
        if lon > e_bound:
            e_bound = lon

    # Boolean masks
    n_mask = input_df['lat'] < n_bound
    e_mask = input_df['lon'] < e_bound
    s_mask = input_df['lat'] > s_bound
    w_mask = input_df['lon'] > w_bound

    mask_lat = np.logical_and(n_mask, s_mask)
    mask_lon = np.logical_and(w_mask, e_mask)
    mask = np.logical_and(mask_lat, mask_lon)

    # Entries/rows within bounding box
    input_df = input_df[mask]

    # SECOND PART
    # Then we check if vessels within polygon

    # We work with a series containing the coordinates instead of the whole df. The indexing is all that matters
    latlon = pd.Series(zip(input_df.loc[:, 'lat'], input_df.loc[:, 'lon']), index=input_df.index)
    # The shapely Polygon object uses (x, y), which means we must reverse the coordinates so they are [(lon, lat)..]
    coordinates = [coord[::-1] for coord in coordinates]
    poly = Polygon(coordinates)


    def within_poly(coord: Tuple, polygon=poly) -> bool:
        # Reversing the coordinate tuple so that the format is (lon, lat)
        lonlat = coord[::-1]
        return Point(lonlat).within(polygon)

    within_mask = latlon.map(within_poly)
    df = input_df.loc[within_mask]

    return df


def remove_transiting_vessels(vessels: pd.DataFrame) -> pd.DataFrame:
    logger = logger_.getChild("remove_transiting_vessels")
    # First strategy: filter on speed (knots)
    # We set the threshold to account for drift (if ships are on anchor or similarly)
    speed_threshold = 2
    vessels_no_transits = vessels.loc[vessels['sog'] < speed_threshold]

    # Second strategy: filter on time
    # If vessel spend less than x time in area, remove all instances
    # But for now include all, independent of time in area
    vessels_no_transits.reset_index(drop=True, inplace=True)

    return vessels_no_transits


def add_arrival_and_departure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to transform rows indexed by timeseries to a single row for each visit of unique vessel

    Strategies
    We first group on mmsi (unique vessels)
    1. Visit determined by timedelta
    - Visit determined when timedelta between to rows are larger than a set value
    - vulnerable to irregularities in AIS reporting.
        - Vessels that are missing AIS data in an x time interval will be tagged as dep/arr
        - Vessels that are in port during the entire dataset will not be registered
    2. Visit determined by change in geographical position
    - Include a geo buffer zone in dataset, x*r (1.5 * r for example)
    - create bool mask of IN or OUT, transition from false->true is arrival, vice-versa is departure
    - more robust than timedelta

    Implementation is strategy 1
    """
    logger = logger_.getChild("add_arrival_and_departure")

    # When timedelta between two consecutive rows are larger than x time, there is a departure-arrival situation
    # We use the function diff() to get this timedelta
    # If a vessel is missing more than some timedelta of AIS data, the vessel is regarded as being departed
    td_value = pd.Timedelta(minutes=60)

    portcalls_df = pd.DataFrame()

    # If there are no portcalls, this loop is never entered
    # Therefore, portcalls_df is empty, and contains no "mmsi" column.
    gen = logger.time_info_generator("For loop unique mmsi")
    next(gen)
    for ident in df.mmsi.unique():
        # A dataframe with a unique ship
        gen.send(f"Iter {ident}")
        vessel = df.loc[df.mmsi == ident].reset_index(drop=True)

        # Calculating the timedelta of preceding row(s)
        diff = pd.to_datetime(vessel.timestamp_utc).diff()

        # If there is just a single row, the diff is empty
        if diff.empty:
            continue

        # If a preceding row has a timedelta more than td_value, it is regarded as an "arrival" row
        arr_bool = diff > td_value

        # The first row is always regarded as the arrival
        arr_bool.iloc[0] = True

        # The departure is the arrival shifted one value back, last value is always regarded as departure
        dep_bool = arr_bool.shift(periods=-1, fill_value=True)

        arr = vessel.loc[arr_bool].reset_index(drop=True).rename(columns={'timestamp_utc': 'arrival_utc'})
        dep = vessel.loc[dep_bool].timestamp_utc.reset_index(drop=True)

        arr.insert(1, "departure_utc", dep)

        portcalls_df = pd.concat([portcalls_df, arr], axis=0).reset_index(drop=True)
    next(gen)

    # If portcalls_df is empty, running any of the below code causes errors.
    # We return early if that is the case.
    if portcalls_df.empty:
        # Creates a new dataframe that has empty columns with the same names used in the
        # other returned dataframes to make it so that a call with no portcalls does not
        # crash a program
        portcalls_df = pd.DataFrame(columns=["arrival_utc", "departure_utc", "mmsi"])
        portcalls_df = portcalls_df.astype({"mmsi": 'float64'})
        return portcalls_df

    # We drop any columns which are not relevant
    cols_to_drop = ['timestamp_utc', 'lon', 'lat', 'sog', 'cog', 'true_heading', 'nav_status', 'message_nr', 'latlon']
    drop_in_df = [col for col in portcalls_df.columns if col in cols_to_drop]
    portcalls_df = portcalls_df.drop(columns=drop_in_df)

    # Rearrange column order
    first_cols = ["mmsi", "arrival_utc", "departure_utc"]
    rearranged = first_cols + [c for c in portcalls_df.columns if c not in first_cols]
    portcalls_df = portcalls_df[rearranged]

    #portcalls_df.reset_index(drop=True, inplace=True)

    return portcalls_df


def portcalls(input_df: pd.DataFrame, args: dict) -> pd.DataFrame:
    """
    Identifies vessels which have been idle in a given geographic area

    Supports both Polygon and Radius
    """
    # Creates logger
    logger = logger_.getChild("portcalls")
    # Input validation, throws keyerror if any required combination of user input is missing (None)
    validate_input_parameters(args)

    # Step 1: Remove the vessels that are transiting
    vessels_idle = logger.time_info("Remove transiting vessels", remove_transiting_vessels, input_df)

    # Step 2: Filter on ships that are in the specified radius/polygon
    center_coord = (args['lat'], args['lon'])
    radius = args['radius']

    polygon = args['polygon']
    if polygon is not None:
        vessels_in_area = vessels_in_polygon(vessels_idle, polygon)
    else:
        vessels_in_area = vessels_in_radius(vessels_idle, center_coord, radius)

    # Step 3: Add two columns to df: arrive and depart
    vessels_arrdep = add_arrival_and_departure(vessels_in_area)

    vessels_arrdep.sort_values(by=['arrival_utc', 'mmsi'])

    return vessels_arrdep
