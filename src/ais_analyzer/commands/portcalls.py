import pandas as pd
import numpy as np
import geopy
import geopy.distance as gpd


def vessels_in_radius(df: pd.DataFrame, point: tuple, radius: float) -> pd.DataFrame:

    # 1. Create a latlon tuple-like column
    # TODO remove if not useful later
    df['latlon'] = list(zip(df.lat, df.lon))

    # 2.1 Check if within square (cheap).

    # First we get the N/E/S/W bounds of the square
    center = geopy.Point(point)
    # Use the `distance` method with a bearing of 0 degrees (which is north), 90 for east etc
    n_b = geopy.distance.distance(meters=radius).destination(center, bearing=0)
    e_b = geopy.distance.distance(meters=radius).destination(center, bearing=90)
    s_b = geopy.distance.distance(meters=radius).destination(center, bearing=180)
    w_b = geopy.distance.distance(meters=radius).destination(center, bearing=270)

    # Boolean masks
    n_mask = df['lat'] < n_b[0]
    e_mask = df['lon'] < e_b[1]
    s_mask = df['lat'] > s_b[0]
    w_mask = df['lon'] > w_b[1]

    mask_lat = np.logical_and(n_mask, s_mask)
    mask_lon = np.logical_and(w_mask, e_mask)
    mask = np.logical_and(mask_lat, mask_lon)

    # Get all entries within the square
    df = df[mask]

    # 2.2 If within, calculate if in radius
    #dist = geopy.distance.distance(pt1, pt2).km

    # 2. Calculate the distance to the center point
    # 3. Keep row if distance is less than radius


    #within_r = lambda p1: (geopy.distance.distance(point, p1).km)/1000 < radius

    # Create a mask of bools for rows that are within_r

    return df


def portcalls(input_df: pd.DataFrame, args: dict) -> pd.DataFrame:
    """Identifies vessels which have been idle in a given geographic area

    <Only supports geo point and radius, will support polygon in future>

    """
    # Ensure arguments
    # More arguments are easy to add
    _required_list = ['lat', 'lon', 'radius']
    _args_present = [input_df.get(arg) for arg in _required_list]
    if None in _args_present:
        _missing = [arg for arg, present in zip(_required_list, _args_present) if present]
        raise KeyError(f"Missing arguments for portcalls: {_missing}")


    # Step 1: Filter on ships that are in the radius
    # - Create inRadius function, apply to df and create boolean mask
    # - Apply mask to the df

    center_coord = (args['lat'], args['lon'])
    radius = args['radius']

    vessels = vessels_in_radius(input_df, center_coord, radius)

    # Step 2: Filter on the vessels that are idle at some point
    # - Threshold on speed? How long should the vessel be below speed threshold to consider "idle"/in port?
    # - Check if geo position stays within a certain area over certain amount of time?
    # -

    return input_df
