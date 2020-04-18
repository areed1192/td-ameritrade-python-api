import datetime

def milliseconds_since_epoch(dt_object: datetime.datetime) -> int:
    """converts a datetime object to milliseconds since 1970, as an integer
    
    Arguments:
    ----------
        dt_object {datetime.datetime} -- Python datetime object.
    
    Returns:
    --------
        [int] -- The timestamp in milliseconds since epoch.
    """

    return int(dt_object.timestamp() * 1000)

def datetime_from_milliseconds_since_epoch(ms_since_epoch: int, timezone: datetime.timezone = None) -> datetime.datetime:
    """Converts milliseconds since epoch to a datetime object.
    
    Arguments:
    ----------
        ms_since_epoch {int} -- Number of milliseconds since epoch.
    
    Keyword Arguments:
    --------
        timezone {datetime.timezone} -- The timezone of the new datetime object. (default: {None})
    
    Returns:
    --------
        datetime.datetime -- A python datetime object.
    """

    return datetime.datetime.fromtimestamp((ms_since_epoch / 1000), tz=timezone)
