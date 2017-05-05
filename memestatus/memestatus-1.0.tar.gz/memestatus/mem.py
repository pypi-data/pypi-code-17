# Setup
from memestatus import core
from math import floor

# Memory used (in percentage)
def mem_percent():
    return floor(apires['mem_percent'])
# Memory free (in bytes6)
def mem_free():
    return apires['mem_free']
# Total RAM
def mem_total():
    return apires['mem_max']

