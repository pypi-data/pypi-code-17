# Setup
from memestatus import core
from math import floor

init = core.core()

def percent():
    """memestatus.mem.percent()

    Returns memory used in percentage."""
    return floor(init.apires['mem_percent'])
def free():
    """memestatus.mem.free()

    Returns memory free in bytes."""
    return init.apires['mem_free']
def total():
    """memestatus.mem.total()

    Returns memory total in bytes."""
    return init.apires['mem_max']

