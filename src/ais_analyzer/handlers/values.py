def get_no_cols() -> list:
    return ['date_time_utc', 'mmsi', 'nav_status', 'lat', 'lon', 'sog', 'length']


def get_dk_cols() -> list:
    return ['# Timestamp', 'MMSI', 'Navigational status', 'Latitude', 'Longitude', 'SOG', 'Length']


def get_no_dtypes() -> dict:
    dt = ['int32', 'int8', 'float32', 'float32', 'float16', 'float16']
    return dict(zip(get_no_cols()[1:], dt))


def get_dk_dtypes() -> dict:
    dt = ['int32', 'category', 'float32', 'float32', 'float16', 'float16']
    return dict(zip(get_dk_cols()[1:], dt))
