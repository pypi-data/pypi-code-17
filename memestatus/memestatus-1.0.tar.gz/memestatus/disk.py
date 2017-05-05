# Setup
from memestatus import core
from math import floor

# Disk used (in GB)
def disk_used():
    return floor(apires['disk_used'])
# Total space (in GB)
def disk_total():
    return floor(apires['disk_total'])
# Disk used (in percentage)
def disk_percent():
    return floor(apires['disk_percent'])
