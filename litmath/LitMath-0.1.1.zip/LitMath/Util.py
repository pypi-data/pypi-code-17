import math
EPSILON = 0.00001

def isEqualZero(value):
    return abs(value) < EPSILON
    
def isEqual(x, y):
    return isEqualZero(x - y)
    
def degreeToRadian(x):
    return x * math.pi / 180.0
    
def radianToDegree(x):
    return x * 180.0 / math.pi
    
def clamp(value, minv, maxv):
    return max(min(value, maxv), minv)