import netCDF4
import six

def open_netcdf(filename, mode='r', ncformat="NETCDF3_CLASSIC"):
    return netCDF4.Dataset(filename, mode, format=ncformat)
    
def close_netcdf(nc):
    nc.close()

def create_dimensions(nc, dimensions):
    """Iterates through the dictionary and creates the dimensions.
    """
    dim = dict()
    for dimname, dim in six.iteritems(dimensions):
        if not isinstance(dim,dict):
            dim[dimname] = nc.createDimension(dimname, dim)
        else:
            dimid = nc.createDimension(dimname, len(dim["array"]))
            dimvar = nc.createVariable( dimname, dim["type"], dim["dimensions"])
            dimvar[:] = dim["array"]
            dim[dimname] = dimid
    
def create_variables(nc, variables):
    """Iterates through the dictionary and creates the variables.
    Each variable item contains a dictionary containing
    keys of dimensions, type, optional data
    """
    var = dict()
    for varname in variables:
        if "extra" in variables[varname] and len(variables[varname]["extra"]):
            var[varname] = nc.createVariable(   varname, 
                                                variables[varname]["type"], 
                                                variables[varname]["dimensions"],
                                                **variables[varname]["extra"])
        else:
            var[varname] = nc.createVariable(   varname, 
                                                variables[varname]["type"], 
                                                variables[varname]["dimensions"])

        if "attributes" in variables[varname]:
            create_attributes(var[varname], variables[varname]["attributes"])
            
    return var
    
def create_attributes(nc, attributes):
    """Sets attributes on the main NC object (file or variable)"""
    
    for attname, attval in six.iteritems(attributes):
        setattr(nc, attname, attval)
        
    return

def output_chunk(filename, ncformat, dimensions_in, data, nlines_read, big_line_counter=0):
    """Loop through variables, and nlines_read, output new records of data"""
    nc = open_netcdf(filename, 'w',ncformat=ncformat)
#    dimensions_in["Time"]=nlines_read
    if "ephemeris_time_m" in data:
        dimensions_in["Time"] = dict(type=data["ephemeris_time_m"]["type"],
                                    dimensions=("Time",),
                                    array=data["ephemeris_time_m"]["array"][:nlines_read])
    elif "ephemeris_time" in data:
        dimensions_in["Time"] = dict(type=data["ephemeris_time"]["type"],
                                    dimensions=("Time",),
                                    array=data["ephemeris_time"]["array"][:nlines_read])
    else:
        raise Exception("No ephemeris time found, cannot proceed")

    dimensions = create_dimensions(nc, dimensions_in)
    variables = create_variables(nc, data)
    
    for col in six.iterkeys(data):
        variables[col][:] = data[col]["array"][:nlines_read]

    #now blank the data
    for d in data:
        data[d]["array"][:] = 0.0 #zero out the data

    big_line_counter += nlines_read
    close_netcdf(nc)
    return data, big_line_counter
