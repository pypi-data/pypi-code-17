import numpy as np
from . import nc
from .wrf_exception import *
from . import dates
import six

def list_variables(fh, fil=None):
    """
    List the variables in a file, filtered for variables in list 'fil'
    """
    with nc.open_if_file_gen(fh) as use_fh:
        varlist = list(use_fh.variables.keys())
        if fil is not None:
            varlist = [fil.lower() in v.lower() for v in varlist]

    return varlist

def filter_indices(infh, year=None, ls=None):
    """Filter indices by looking for year
    """
    with nc.open_if_file_gen(infh) as fh:
        ls_file = fh.variables["L_S"][:]
        times_file = fh.variables["Times"][:]

    indices = np.arange(len(ls_file))
    truthiness=indices>-1
    #
    if year is not None:
        if isinstance(year,list):
            year_range = dates.find_year_range_in_file(times_file, year[0], year[1])
        else:
            year_range = dates.find_year_range_in_file(times_file, year[0], year[0])
        truthiness[0:year_range[0]]=False
        truthiness[year_range[1]:]=False

    ls_file=ls_file[:]
    if ls is not None:
        if isinstance(ls,list):
            truthiness = truthiness & (ls_file>=ls[0]) & (ls_file<ls[1])
        else:
            truthiness = truthiness & (ls_file==ls)

    indices = indices[truthiness]
    if len(indices) ==0:
        raise WRF_Exception("No elements found")

#    print indices
    if len(indices)==1:
        return indices
    elif np.max(np.diff(indices)) == 1 :
        return slice(indices[0],indices[-1]+1,1)
    else:
        return indices
        
            
    
def ls_range(fh):
    """return the start and end Ls range of the data"""
    with nc.open_if_file_gen(fh) as use_fh:
        ls = use_fh.variables["L_S"]
        a,b = ls[0],ls[-1]
    return a,b


def time_range(fh):
    """return the start and end Ls for each year of the data"""
    with nc.open_if_file_gen(fh) as use_fh:
        ls = use_fh.variables["L_S"][:]
        times = use_fh.variables["Times"][:]

    years = [dates.get_year(s) for s in times[:]]
    triplet = list(zip(years, ls,list(range(len(ls)))))
    rt = []
    rl = []
    re = []
    for p in triplet:
        if p[0] not in rt:
            rt.extend([p[0],p[0]])
            rl.extend([p[1],p[1]])
            re.extend([p[2],p[2]])
        elif p[0] in rt:
            rt[-1],rl[-1],re[-1]=p

    return rt, rl, re

def time_dict(fh):
    """ """
    rt,rl,re = time_range(fh)
    rl = [l % 360 for l in rl]
    return dict(year=rt,    ls=rl,    index=re)

def time_tuple(time,return_dict=False):
    """ Parse the time format from MarsWRF
        time format is YYYY-DDDDD_HH:MM:SS
    """
    time_format = "YYYY-DDDDD_HH:MM:SS"
    #              0123456789012345678
    if len(time)!=len(time_format):
        raise Exception("time string has wrong length: {0},({1}),({2})".format(time,len(time), len(time_format)))
    timedict = dict(year=slice(0,4),
                    day=slice(5,10),
                    hour=slice(11,13),
                    minute=slice(14,16),
                    second=slice(17,None))
    if return_dict:
        return dict((k,int(time[v])) for k,v in six.iteritems(timedict))
    else:
        return [int(time[timedict[k]])for k in ["year","day","hour","minute","second"]]

    
