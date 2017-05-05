import numpy as np
from . import wrf_exception

def mean(data,axis):
    """Calculates the mean of 'data' of a list of axis.
    Does this by calling mean repeatedly and passing each axis value in turn."""
    if isinstance(axis,list):
        ax=list(axis)
    else:
        ax=[axis]
    ax=[(a+data.ndim) % data.ndim for a in ax]
    ax.sort()
    ax=ax[::-1]
    outdata = data
    for a in ax:
        outdata = np.mean(outdata, axis=a)

    return outdata
    
def zonalmean(data):
    """Calculates the zonal mean of 'data', assuming longitude is the last axis"""
    return mean(data, -1)

def zonalandtimemean(data):
    """Calculates the mean in longitude and time"""
    return mean(data, [0,-1])

def timemean(data):
    """Calculate the time mean assuming time is the first axis."""
    return mean(data,0)
    
