# Setup
from memestatus import core
from math import floor

init = core.core()
def used():
    """memestatus.disk.used()

    Returns used disk space in GB."""
    return floor(init.apires['disk_used'])
def total():
    """memestatus.disk.total()

    Returns total disk space available in GB."""
    return floor(init.apires['disk_total'])
def percent():
    """memestatus.disk.percent()

    Returns percentage of disk used."""
    return floor(init.apires['disk_percent'])
