class Values:

    def __init__(self) -> None:
        pass

    def get_no_cols() ->list:
        return['mmsi', 'date_time_utc', 'nav_status','lat','lon', 'sog','length']

    def get_dl_cols() -> list:
        return['MMSI','# Timestamp','Navigational status','Latitude','Longitude','SOG','Length']