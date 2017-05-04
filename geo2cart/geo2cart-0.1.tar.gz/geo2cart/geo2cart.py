

import math

def cartesian(lat,lon, elevation):
    cosLat = math.cos(lat * math.pi / 180.0)
    sinLat = math.sin(lat * math.pi / 180.0)
    cosLon = math.cos(lon * math.pi / 180.0)
    sinLon = math.sin(lon * math.pi / 180.0)
    rad = 6378137.0 + elevation
    f = 1.0 / 298.257224
    C = 1.0 / math.sqrt(cosLat * cosLat + (1 - f) * (1 - f) * sinLat * sinLat)
    S = (1.0 - f) * (1.0 - f) * C
    h = 0.0
    x = (rad * C + h) * cosLat * cosLon
    y = (rad * C + h) * cosLat * sinLon
    z = (rad * S + h) * sinLat
    return x, y, z