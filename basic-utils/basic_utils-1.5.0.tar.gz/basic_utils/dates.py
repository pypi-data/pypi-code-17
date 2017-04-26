from datetime import datetime, timedelta
from itertools import starmap
from typing import Iterator, NamedTuple, NewType, Tuple

__all__ = ['dates_between', 'date_ranges_overlap']


DatePair = NewType('DatePair', Tuple[datetime, datetime])

DateRange = NamedTuple('DateRange', [('start', datetime), ('end', datetime)])

# [TODO] Document functions


def dates_between(start: datetime, end: datetime) -> Iterator[datetime]:
    """Returns lazy sequence of dates between a start/end point"""
    while start <= end:
        yield start
        start += timedelta(days=1)


def date_ranges_overlap(datesX: DatePair, datesY: DatePair) -> bool:
    r1, r2 = starmap(DateRange, (datesX, datesY))
    # Determine latest of two start dates the earliest of the two end dates
    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)
    overlap = (earliest_end - latest_start).days + 1
    # Determine if timedelta is positive
    return overlap > 0
