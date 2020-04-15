import datetime


def milliseconds_since_epoch(dt_object):
    '''
        converts a datetime object to milliseconds since 1970, as an integer

        NAME: dt_object
        DESC: python datetime object
        TYPE: datetime.datetime
    '''
    return int( dt_object.timestamp() * 1e3 )


def datetime_from_milliseconds_since_epoch(ms_since_epoch,timezone=None):
    '''
        converts milliseconds since epoch to a datetime object

        NAME: ms_since_epoch
        DESC: milliseconds since epoch
        TYPE: Numbers.number
    '''

    return datetime.datetime.fromtimestamp(ms_since_epoch/1e3, tz=timezone)