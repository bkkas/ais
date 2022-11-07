import pandas as pd
import numpy as np
import geopy
import geopy.distance as gpd
from typing import Tuple
import datetime as dt


def vessels_in_radius(df: pd.DataFrame, point: tuple, radius: float) -> pd.DataFrame:

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

    # 2.2 If within, calculate if in radius
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


def validate_input_parameters(args):
    _required_list = ['lat', 'lon', 'radius']
    _args_present = [args[arg] for arg in _required_list]

    if None in _args_present:
        _missing = [arg for arg, present in zip(_required_list, _args_present) if not present]
        raise KeyError(f"Missing arguments for portcalls: {_missing}")


def remove_transiting_vessels(vessels: pd.DataFrame) -> pd.DataFrame:
    # First strategy: filter on speed (knots)
    # We set the threshold to account for drift (if ships are on ancher or similarly)
    speed_threshold = 2
    vessels_no_transits = vessels.loc[vessels['sog'] < speed_threshold]

    # Second strategy: filter on time
    # If vessel spend less than x time in area, remove all instances
    # But for now include all, independent of time in area

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

    # When timedelta between two consecutive rows are larger than x time, there is a departure-arrival situation
    # We use the function diff() to get this timedelta
    # If a vessel is missing more than some timedelta of AIS data, the vessel is regarded as being departed
    td_value = 1

    portcalls_df = pd.DataFrame()

    # If there are no portcalls, this loop is never entered
    # Therefore, portcalls_df is empty, and contains no "mmsi" column.
    for ident in df.mmsi.unique():
        # A dataframe with a unique ship
        vessel = df.loc[df.mmsi == ident].reset_index(drop=True)

        # Calculating the timedelta of preceding row(s)
        diff = pd.to_datetime(vessel.timestamp_utc).diff()

        # If a preceding row has a timedelta more than td_value, it is regarded as an "arrival" row
        arr_bool = diff > pd.Timedelta(td_value, unit="hours")

        # The first row is always regarded as the arrival
        arr_bool.iloc[0] = True

        # The departure is the arrival shifted one value back, last value is always regarded as departure
        dep_bool = arr_bool.shift(periods=-1, fill_value=True)

        arr = vessel.loc[arr_bool].reset_index(drop=True).rename(columns={'timestamp_utc': 'arrival_utc'})
        dep = vessel.loc[dep_bool].timestamp_utc.reset_index(drop=True)

        arr.insert(1, "departure_utc", dep)

        portcalls_df = pd.concat([portcalls_df, arr], axis=0).reset_index(drop=True)

    # If portcalls_df is empty, running any of the below code causes errors.
    # We return early if that is the case.
    if portcalls_df.empty:
        # Creates a new dataframe that has empty columns with the same names used in the
        # other returned dataframes to make it so that a call with no portcalls does not
        # crash a program
        portcalls_df = pd.DataFrame(columns=["arrival_utc", "departure_utc", "mmsi"])
        portcalls_df = portcalls_df.astype({"mmsi": 'float64'})
        portcalls_df.set_index("mmsi", inplace=True)
        return portcalls_df

    # We drop the columns which are not relevant
    cols_to_drop = ['timestamp_utc', 'lon', 'lat', 'sog', 'cog', 'true_heading', 'nav_status', 'message_nr', 'latlon']
    drop_in_df = [col for col in portcalls_df.columns if col in cols_to_drop]
    portcalls_df = portcalls_df.drop(columns=drop_in_df).set_index('mmsi')

    return portcalls_df


def portcalls(input_df: pd.DataFrame, args: dict) -> pd.DataFrame:
    """Identifies vessels which have been idle in a given geographic area

    <Only supports geo point and radius, will support polygon in future>

    """
    # Input validation
    validate_input_parameters(args)

    # Step 1: Filter on ships that are in the radius
    center_coord = (args['lat'], args['lon'])
    radius = args['radius']
    vessels_rad = vessels_in_radius(input_df, center_coord, radius)

    # Step 2: Filter on vessels that are idle at some point - remove the vessels that are transiting
    # - Threshold on speed? How long should the vessel be below speed threshold to consider "idle"/in port?
    # - Check if geo position stays within a certain area over certain amount of time?
    vessels_idle = remove_transiting_vessels(vessels_rad)

    # Step 3: Add two columns to df: arrive and depart
    # This is the first and last rows of a grouping on MMSI
    vessels_arrdep = add_arrival_and_departure(vessels_idle)

    return vessels_arrdep
