import pytest
from datetime import datetime
import pytz
from ttr.aws.utils.s3.utils import check_from_to


def utc(*args, **kwargs):
    res = datetime(*args, **kwargs)
    return res.replace(tzinfo=pytz.UTC)


scenarios = [
    ["2015-08-15T00:00:00Z", "2015-09-15T00:00:00Z",
     (utc(2015, 8, 15, 0, 0, 0),
      utc(2015, 9, 15, 0, 0, 0))],
    ["", "", (None, None)],
    ["", "2015-09-15T00:00:00Z", (None, utc(2015, 9, 15, 0, 0, 0))],
    ["2015-08-15T00:00:00Z", "", (utc(2015, 8, 15, 0, 0, 0),
                                  None)],
    pytest.mark.xfail(
        ["2015-09-15T00:00:00Z", "2015-08-15T00:00:00Z",
         (utc(2015, 8, 15, 0, 0, 0),
          utc(2015, 9, 15, 0, 0, 0))],
        raises=ValueError), ]


def scen_id(scenario):
    from_txt = scenario[0]
    to_txt = scenario[1]
    return "{from_txt}-{to_txt}".format(from_txt=from_txt,
                                        to_txt=to_txt)


@pytest.mark.parametrize("scenario", scenarios, ids=scen_id)
def test_from_to(scenario):
    from_time, to_time, expected = scenario
    res = check_from_to(from_time, to_time)
    assert res == expected
