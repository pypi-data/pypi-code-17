from datetime import datetime, timedelta

DEFAULT_DATE_PATTERN = '%Y-%m-%d %H:%M:%S'

def round_date_to_minute_mark(date, resolution, round_up=False):
    """
    Round a datetime up or down to a minute mark
        date: Time to round
        resolution: minute bucket
        round_up: bool
    """
    newMinute = (date.minute // resolution + (1 if round_up else 0)) * resolution
    return date + timedelta(minutes=newMinute - date.minute, seconds=-date.second)

def round_date_to_last_hour(date):
    """
     Converts string to a datetime object for the Day
        date: Datetime to round
    :return: Day representation
    :rtype: datetime.datetime
    """
    return datetime(date.year, date.month, date.day, date.hour, 0, 0)