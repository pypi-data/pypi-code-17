# Setup
from memestatus import core
from math import floor

init = core.core()
def cpu():
    """memestatus.cpu()

    Returns CPU in percentage."""
    return floor(init.apires['cpu_percent'])
