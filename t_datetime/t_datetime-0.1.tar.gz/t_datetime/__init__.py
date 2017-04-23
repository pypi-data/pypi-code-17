#!/usr/bin/env python

import datetime
import time

def get_seconds_since_epoch():
    return time.time()

def datetime_to_seconds_since_epoch(_datetime):
    return _datetime.timestamp()

def get_utc_datetime():
    return datetime.datetime.utcnow()
