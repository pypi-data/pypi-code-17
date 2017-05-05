from . import nc
from . import special_variables
import numpy as np

def get(infh, varname, indices=None,latitude=None,return_dimensions=False,*args,**kwargs):
    """ Tries to get the data from file. If the variable exists in the file it's accessed directory.
    If not, the variable name is searched for in the special_variables file and that code is called.
    """
    fh = nc.open_if_file(infh)
    with nc.open_fi_file_gen(infh) as fh:
        indices = nc.sanitize_indices(indices)
        if varname in fh.variables:
            var = fh.variables[varname][indices]
            dims = fh.variables[varname].dimensions
            if return_dimensions:
                var=var,dims
        else:
            varfunc=getattr(special_variables, varname)
            var = varfunc(fh, indices=None, return_dimensions=return_dimensions,*args, **kwargs)

    return var


def att(infh, attname):
    """Returns the attribute from a netCDF file"""
    with nc.open_if_file_gen(infh) as fh:
        attval = getattr(fh,attname)
    return attval
        
def coordinates(infh,variable,indices=None):
    with nc.open_if_file_gen(infh) as fh:
        indices = nc.sanitize_indices(indices)
        v = fh.variables[variable]
        coord_names = v.coordinates.split(" ")
        coords=list()

        for c in coord_names:
            coords.append(fh.variables[c][0])

    return coords

def axis_ls(infh,indices=None):
    """Returns Ls values in continuously growing form"""
    with nc.open_if_file_gen(infh) as fh: 
        indices = nc.sanitize_indices(indices)
        ls = fh.variables["L_S"][indices]
    return continuous_ls(ls)

def continuous_ls(ls):
    """Tries to convert Ls values to be continuous.
    Does this by looking for negative changes in Ls values and assumes that's the next year of data"""
    loop=-1
    old=360.
    for i,v in enumerate(ls):
        if v < old+1e-5:
            loop+=1
        ls[i]+=loop*360.
        old=v
    return ls

def split_ls(x,y):
    """Find the locations of negative changes in Ls and returns a tuple of Ls and 'data' split into the Ls groups"""
    start=0
    xx=[]
    yy=[]
    for i in range(x.size-1):
        if x[i+1]<x[i]:
           xx.append(x[start:i+1])
           yy.append(y[start:i+1])
           start=i+1

    xx.append(x[start:])
    yy.append(y[start:])
    return xx,yy

def monotonic(data,return_slices=True):
    """Alternate Ls splitter. Looks for negative differences in 'data' and returns the data sliced into a list.
    optionally (return_slices=True, default) returns the slices too."""
    diffs=np.diff(data)
    w=np.where(diffs<0)
    slices=[]
    res=[]
    if len(w)==0:
        res= [data]
        slices.append(slice(None,None,None))
    elif len(w[0])==0:
        res= data
        slices.append(slice(None,None,None))
    else:
        points = w[0]
        l=0
        for p in points:
            res.append(data[l:p+1])
            slices.append(slice(l,p+1))
            l=p+1
    
        if l != len(data)-1:
            res.append(data[l:])
            slices.append(slice(l,None))

    if return_slices:
        return res,slices
    else:
        return res
