import pytest
from datetime import datetime

from ttr.aws.utils.s3.utils import parse_datetime
import pytz


def utc(*args, **kwargs):
    res = datetime(*args, **kwargs)
    return res.replace(tzinfo=pytz.UTC)


scenarios = [
    ["2015-01-01T00:00:00Z", "min", utc(2015, 1, 1, 0, 0, 0)],
    ["2015-01-01T00:00:00", "min", utc(2015, 1, 1, 0, 0, 0)],
    ["2015-01-01T00:00", "min", utc(2015, 1, 1, 0, 0, 0)],
    ["2015-01-01T00", "min", utc(2015, 1, 1, 0, 0, 0)],
    ["2015-01-01T", "min", utc(2015, 1, 1, 0, 0, 0)],
    ["2015-01-01", "min", utc(2015, 1, 1, 0, 0, 0)],
    ["2015-01", "min", utc(2015, 1, 1, 0, 0, 0)],
    ["2015", "min", utc(2015, 1, 1, 0, 0, 0)],
    ["2015-01-01T00:00:00Z", "max", utc(2015, 1, 1, 0, 0, 0)],
    ["2015-01-01T00:00:00", "max", utc(2015, 1, 1, 0, 0, 0)],
    ["2015-01-01T00:00", "max", utc(2015, 1, 1, 0, 0, 59)],
    ["2015-01-01T00", "max", utc(2015, 1, 1, 0, 59, 59)],
    ["2015-01-01T", "max", utc(2015, 1, 1, 23, 59, 59)],
    ["2015-01-01", "max", utc(2015, 1, 1, 23, 59, 59)],
    ["2015-01", "max", utc(2015, 1, 31, 23, 59, 59)],
    ["2015-02", "max", utc(2015, 2, 28, 23, 59, 59)],
    ["2000-02", "max", utc(2000, 2, 29, 23, 59, 59)],
    ["2004-02", "max", utc(2004, 2, 29, 23, 59, 59)],
    ["2008-02", "max", utc(2008, 2, 29, 23, 59, 59)],
    ["2012-02", "max", utc(2012, 2, 29, 23, 59, 59)],
    ["2012-0", "max", utc(2012, 9, 30, 23, 59, 59)],
    ["2012-1", "max", utc(2012, 12, 31, 23, 59, 59)],
    ["2012", "max", utc(2012, 12, 31, 23, 59, 59)],
]


def parse_id(scenario):
    text = scenario[0]
    padmode = scenario[1]
    return "{text}-{padmode}".format(text=text, padmode=padmode)


@pytest.mark.parametrize("scenario", scenarios, ids=parse_id)
def test_parsetime(scenario):
    text, padmode, expected = scenario
    res = parse_datetime(text, padmode)
    assert res == expected
