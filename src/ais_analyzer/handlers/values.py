def get_no_cols() -> list:
    return ['date_time_utc', 'mmsi', 'nav_status', 'lat', 'lon', 'sog', 'length']


def get_dk_cols() -> list:
    return ['# Timestamp', 'MMSI', 'Latitude', 'Longitude', 'Navigational status', 'SOG', 'COG', 'IMO', 'Callsign',
            'Name', 'Ship type', 'Cargo type', 'Width', 'Length', 'Draught', 'Destination']


def get_standardized_cols() -> dict:
    lookup_cols = ['time', 'mmsi', 'imo', 'lat', 'lon', 'nav', 'dest', 'len', 'draught', 'width', 'sog', 'ship type',
                   'cargo type', 'name', 'callsign', 'cog']
    std_cols = ['timestamp_utc', 'mmsi', 'imo', 'lat', 'lon', 'nav_status', 'dest', 'length', 'draught', 'width', 'sog',
                'ship_type', 'cargo_type', 'name', 'callsign', 'cog']
    return dict(zip(lookup_cols, std_cols))


def get_no_dtypes() -> dict:
    dt = ['int32', 'int32', 'float32', 'float32', 'float32', 'float32']
    return dict(zip(get_no_cols()[1:], dt))


def get_dk_dtypes() -> dict:
    dt = ['int32', 'category', 'float32', 'float32', 'float32', 'float32']
    return dict(zip(get_dk_cols()[1:], dt))
