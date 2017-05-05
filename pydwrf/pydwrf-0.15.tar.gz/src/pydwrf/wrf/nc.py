import netCDF4
import numpy as np
from contextlib import contextmanager
from pydwrf.wrf.wrf_exception import WRF_Exception

def sanitize_indices(indices):
    """Really bad sanitizing function. If there are no indices, return a slice object to index all the data"""
    if indices is None:
        indices=slice(None,None,None)
    return indices

from contextlib import contextmanager

@contextmanager
def open_if_file_gen(fh):
    """opens a file if the name is supplied, or transparently returns a filehandle"""
    if isinstance(fh,str):
        try: 
            ff=netCDF4.Dataset(fh) 
            yield ff
        finally:
            ff.close()
    elif isinstance(fh,netCDF4._netCDF4.Dataset):
        yield fh
    else:
        raise WRF_Exception("No filename or filehandle given {0}".format(fh))
    
def open_if_file(fh):
    """opens a file if the name is supplied, or transparently returns a filehandle"""
    if isinstance(fh,str):
        return netCDF4.Dataset(fh)
    elif isinstance(fh,netCDF4._netCDF4.Dataset):
        return fh
    raise WRF_Exception("No filename or filehandle given {0}".format(fh))