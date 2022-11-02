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
    def get_point_distance_center(latlon: Tuple[float]) -> float:
        """
        :param latlon:
        :return distance from center:
        """

        _point = geopy.Point(latlon)
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

    # Group on MMSI
    mmsi_grouping = df.groupby('mmsi')

    # Arrivals - the first entry of mmsi grouping
    arrivals = mmsi_grouping.head(1)

    # Departures - the last entry
    departures = mmsi_grouping.tail(1)

    # New columns: time of arrival and departure
    arrivals_utc = arrivals[['mmsi', 'timestamp_utc']].set_index('mmsi').rename(
        columns={'timestamp_utc': 'arrival_utc'})
    departures_utc = departures[['mmsi', 'timestamp_utc']].set_index('mmsi').rename(
        columns={'timestamp_utc': 'departure_utc'})
    arr_dep = arrivals_utc.merge(departures_utc, left_index=True, right_index=True)

    # We drop the columns which are not relevant
    cols_to_drop = ['timestamp_utc', 'lon', 'lat', 'sog', 'cog', 'true_heading', 'nav_status', 'message_nr', 'latlon']
    drop_in_df = [col for col in arr_dep.columns if col in cols_to_drop]
    vessels_info = arrivals.drop(columns=drop_in_df).set_index('mmsi')

    vessels_info = arr_dep.merge(vessels_info, left_index=True, right_index=True)
    vessels_info

    return vessels_info


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
