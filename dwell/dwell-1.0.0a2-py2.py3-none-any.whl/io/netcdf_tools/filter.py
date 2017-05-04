import numpy as np
import netCDF4
from .boolfilter import boolfilter
import logging
import dwell.io.netcdf as netcdf

def filter_time(time, start_date, end_date):
    if start_date is None:
        start_date = -9e36
    if end_date is None:
        end_date = 9e36
    return (time >=start_date)&(time<end_date)
    
def find_indices_to_extract(ncin, time_axis, start_date=None, end_date=None, 
                            filter_condition=None, filenames=None, log=None,
                            keep_duplicates=False):
    """This function finds the indices to extract from each NetCDF filehandle in ncin 
    using the start_date and end_date."""
    if log is None:
        log = logging.getLogger("pydwell")
    
    indices=[]
    times=[]
    count=0
    fcount=0
    for nc in ncin:
        log.debug("Filtering file {0} of {1}".format(fcount,len(ncin)))
        time = nc.variables[time_axis][:]
        if filter_condition is None:
            w=np.where(filter_time(time,start_date, end_date))
        else:
            w=np.where(boolfilter(nc, filter_condition))
        
        if len(w[0]):
            indices.append(w[0]) #return w[0]
            times.append(time[w[0]])
            count=count+len(w[0])
        else:
            indices.append([]) #return []
        fcount = fcount + 1
    #print(count, time_axis)
    if count > 0:
        indices, ncin, count, redundant_ncin = filter_duplicate_times(ncin, time_axis, indices, count, filenames=None, keep_duplicates=keep_duplicates)
    return indices, ncin, count, redundant_ncin

def filter_duplicate_times(ncin, time_axis, indices, count, filenames = None, time_threshold=1.0, log=None, keep_duplicates=False):
    """
        Filter the times from ncin to find duplicates.
        1. Starts by finding the minimum and maximum times in each of the available files.
        2. Sorts these files based on the start_time.
        3. For each of the available files, collect as many indices from the file
        using the early file in preference to later files such that overlapping data 
        from early files is taken instead of later files, and overlapped data in 
        later files is ignored.
    """
    if filenames is None:
        filenames = [""]*len(ncin)
    if log is None:
        log = logging.getLogger("pydwell")
    #first of all, find the min and max valid times from each files
    time_range=[]
    for nc, ind in zip(ncin, indices):
        if len(ind):
            time = nc.variables[time_axis][ind]
            time_range.append( [time[0], time[-1]] )
        else:
            time_range.append( [] )
    #The time_range array either has an empty list for each file, or the start and end times of each file.
    #now we sort files based on min_time -> time_range[][0]
    #sort function is the first element of the first element of the tuple.
    #i.e. we provide a tuple of elements to sort, the first is the time range tuple.
    sort_function = lambda tup: tup[0][0]
    new_time, new_nc, new_ind, new_filenames = list(zip(*sorted(zip(time_range,ncin, indices,filenames))))
    result = []
    #Now we're sorted, iterate through the files, creating the results list which contains
    #a list corresponding to the files
    #where each entry is a list of indices, netcdf filehandle, filename, and times in epoch format
    #the last of these entries is the time, where the first element is the first element taken from the file
    #the last element is the last element from the file (confusing no..)
    redundant_ncin=[]
    for t, nc, ind,f in zip(new_time, new_nc, new_ind,new_filenames):
        if len(t) ==0: #no new data, don't do anything
            redundant_ncin.append(nc)
            continue
        #at the start we are empty
        if len(result): #have some data already in the list
            #This element (the last of the last of the last) is
            #the last element of the time element of the previous file
            last_time = result[-1][-1][-1] 
            new_file_time = nc.variables[time_axis][ind]
            #keep data that is later than this observation by at least time_threshold seconds
            filter_func = lambda tup: tup[0] > (last_time+time_threshold/86400.)
            if keep_duplicates:
                filter_func = lambda x: True
            
            new_data = list(filter(filter_func, list(zip(new_file_time, ind))))
            if len(new_data):
                new_time, new_ind = list(zip(*new_data))
                result.append([np.array(new_ind),nc,f,t])
            else: #no data to append
                redundant_ncin.append(nc)
                pass
        else:
            result.append([ind, nc, f, t])
            
    #finish the loop
    count = sum([len(x[0]) for x in result])
    newind, newnc, newfilenames, newtime = list(zip(*result))
    return newind, newnc, count, redundant_ncin
    
def select_data(var, newtime):
    """select the new data from var corresponding to indices given in newtime"""
    #if index of time is 0 only
    #thats annnnoying
    if len(var.shape) >= 2:
        return var[newtime]
    elif len(var.shape) ==1: 
        #print var[newtime]
        return var[newtime]
    else:
        raise Exception("Bugger, I have no clue why this happened")

def extract_field(ncin, newtime, varname, aslist=False, log=None):
    """Extract the var with name=varname from the ncin NetCDF files, using the corresponding
    time axis stored in newtime"""
    if log is None:
        log = logging.getLogger("pydwell")
    data=[]
    #do we have the appropriate dimensions to filter this code
#    if ncin[0].variables[vari
    for nc, nt in zip(ncin, newtime):
        if len(nt) > 0:
            data.append(select_data(nc.variables[varname], nt))
    if not aslist:
        data = np.concatenate(data,0)#-1)
    return data


def create_dimensions(ncout, time_axis, canonical_ncin, log=None):
    """Create all of the necessary dimensions in ncout using the canonical_ncin as a template"""
    if log is None:
        log = logging.getLogger("pydwell")
#    log.debug("Creating Dimensions in NetCDF")
    dim={}
    obs_variables = [x for x in list(canonical_ncin.dimensions.keys()) if not x.startswith(time_axis)]
                
    
    for dname in obs_variables:
        dval = canonical_ncin.dimensions[dname]
#        log.debug("Obs Dimension {0} has size {1}".format(dname, len(dval)))
        dim[dname] = ncout.createDimension(dname, len(dval))
    
    return dim

def create_variables(ncout, time_axis, canonical_ncin, ncin, newtime, log=None, zlib=False, filter_variables=None):
    """Create the necessary variables from the canonical_ncin NetCDF file, then extract
    the data from each of the ncin files as needed and save the data in the output variable.
    """
    if log is None:
        log = logging.getLogger("pydwell")
#    pbar = progressbar.ProgressBar(len(canonical_ncin.variables.keys())).start()
    counter=0
    variables = canonical_ncin.variables
    #filter out data with prefixes
    #filter out data with no time index as the first index.
    #filter(lambda x: canonical_ncin.variables[x].dimensions[0] == time_axis, variables)
    use_variables = [x for x in variables if canonical_ncin.variables[x].dimensions[0] == time_axis]
    #filter(lambda x: time_axis not in canonical_ncin.variables[x].dimensions, variables)
    copy_variables = [x for x in variables if time_axis not in canonical_ncin.variables[x].dimensions]
    netcdf.copy_variables(canonical_ncin, ncout, include=copy_variables)
    if filter_variables is not None:
        #use_variables = filter(lambda x: x in filter_variables,use_variables)
        use_variables = [x for x in use_variables if x in filter_variables]
    
    for varname in use_variables:
        log.debug("Variable {0}".format(varname))
        canonical_var = canonical_ncin.variables[varname]
#        pbar.update(counter)
        counter=counter+1
        #collect data for this variable
        data=extract_field(ncin, newtime, varname)
        mydim = canonical_var.dimensions
        #att = dict(
        #            map(
        #                lambda x: (x, getattr(canonical_var,x)),canonical_var.ncattrs()
        #                )
        #        )
        att = [(x,getattr(canonical_var,x)) for x in canonical_var.ncattrs()]
        mytype = canonical_var.dtype
        if "_FillValue" in canonical_var.ncattrs():
            newvar = ncout.createVariable(varname, mytype, mydim, fill_value = getattr(canonical_var, "_FillValue"), zlib=zlib)#
        else:
            newvar = ncout.createVariable(varname, mytype, mydim, zlib=zlib)#
        newvar[:] = data[:] # attributes=att)
        for attname, attval in six.iteritems(att):
            if attname != "_FillValue":
                setattr(newvar,attname, attval)

  
def filter_netcdf(input_files, output_file, time_axis="Time", low_time=None, high_time=None, filter_condition=None, zlib=False, filter_variables=None,log=None,keep_duplicates=False):
    """Filter the NetCDF input files based on the time_axis entry from 'low' to 'high' and create
    a new file out of the input files and restrictions. Default values for 0<=time<=9e36 ."""
    infiles = [netCDF4.Dataset(input,'r') for input in input_files]
    output = netCDF4.Dataset(output_file,'w')

    if filter_condition is None and low_time is None:
        low_time = -9e36
    if filter_condition is None and high_time is None:
        high_time = 9e36
    
    indices, ncin, count, redundant = find_indices_to_extract(infiles, time_axis, start_date=low_time, end_date=high_time, 
                                                              filter_condition=filter_condition, filenames=input_files,log=log, keep_duplicates=keep_duplicates)
    
    output.createDimension(time_axis, count)
    #create dimensions from first input
    create_dimensions(output, time_axis, ncin[0],log=log)
    create_variables(output, time_axis, ncin[0], ncin, indices, zlib=zlib, filter_variables=filter_variables,log=log)
    for x in redundant:
        x.close()
    for x in ncin:
        x.close()
    output.close()
        
