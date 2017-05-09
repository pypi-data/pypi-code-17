import gzip
import datetime
import pytz
from StringIO import StringIO


def gunzip_data(data):
    '''Decomress data from string using gzip method.

    :type data: string
    :param data: string to be decompressed

    :rtype: string
    :return: decompressed string
    '''
    buf = StringIO(data)
    gzipper = gzip.GzipFile(fileobj=buf)
    data = gzipper.read(data)
    gzipper.close()
    # todo, check for possible memory leak, shall I close the buf?
    return data


def check_from_to(from_txt, to_txt):
    if from_txt:
        from_time = parse_datetime(from_txt, "min")
    else:
        from_time = None

    if to_txt:
        to_time = parse_datetime(to_txt, "max")
    else:
        to_time = None

    if (from_time and to_time):
        if not from_time < to_time:
            msg = "from ({from_txt}) must be smaller then -to ({to_txt})"
            raise ValueError(msg.format(from_txt=from_txt, to_txt=to_txt))
    return from_time, to_time


def parse_datetime(text, padmode):
    padmodes = ["min", "max"]
    if padmode not in padmodes:
        raise ValueError('padmode must be `"min"` or `"max"`')
    padtxts = {"min": ["0000-01-01T00:00:00Z"],
               "max": ["9999-99-31T23:59:59Z",
                       "9999-99-30T23:59:59Z",
                       "9999-99-29T23:59:59Z",
                       "9999-99-28T23:59:59Z",

                       "9999-12-31T23:59:59Z",
                       "9999-12-30T23:59:59Z",
                       "9999-12-29T23:59:59Z",
                       "9999-12-28T23:59:59Z"
                       ]
               }[padmode]
    fmt = "%Y-%m-%dT%H:%M:%S"
    for padtxt in padtxts:
        ftext = text + padtxt[len(text):]
        try:
            res = datetime.datetime.strptime(ftext[:19], fmt)
            res = res.replace(tzinfo=pytz.UTC)
            return res
        except ValueError as e:
            # expect e.message "day is out of range for month"
            pass
    raise e
