import netCDF4
from collections import OrderedDict as odict
import six

def copy_attributes(ncin, ncout,exclude=None, include=None):
    """Copy the global or variable attributes from the input to the output"""
    att_dict = odict()
    for attribute_name in ncin.ncattrs():
        if include is not None and attribute_name not in include:
            continue #if include is defined, and this attribute is not there
        if exclude is not None and attribute_name in exclude:
            continue #if exclude is defined, and this attribute is there
        att_dict[attribute_name]  = ncin.getncattr(attribute_name)
    ncout.setncatts(att_dict)

def copy_dimensions(ncin, ncout, exclude=None, include=None):
    """Copy the file dimensions from input to output"""
    for dimname, dimval in six.iteritems(ncin.dimensions):
        if include is not None and dimname not in include:
            continue #if include is defined, and this attribute is not there
        if exclude is not None and dimname in exclude:
            continue #if exclude is defined, and this attribute is there

        size = None if dimval.isunlimited() else len(dimval)
        ncout.createDimension(dimname, size=size)

def copy_variable_data(ncin, ncout, include=None, exclude=None):
    "Copy the variable information, but not the data, from input to output"
    
    for varname, variable in six.iteritems(ncin.variables):
        if include is not None and varname not in include:
            continue #if include is defined, and this attribute is not there
        if exclude is not None and varname in exclude:
            continue #if exclude is defined, and this attribute is there

        datatype = variable.dtype
        dimensions = variable.dimensions
        fill_value = None
        if "missing_value" in variable.ncattrs():
            fill_value = variable.getncattr("missing_value")
        if "_FillValue" in variable.ncattrs():
            fill_value = variable.getncattr("_FillValue")
        outvariable = ncout.createVariable(varname, datatype, dimensions, fill_value=fill_value)
        
        #get the attributes
        copy_attributes(variable, outvariable, exclude=["missing_value","_FillValue"])
        
def copy_variables(ncin, ncout,include=None, exclude=None):
    copy_variable_data(ncin, ncout, include=include, exclude=exclude)
    for varname, variable in six.iteritems(ncin.variables):
        if include is not None and varname not in include:
            continue #if include is defined, and this attribute is not there
        if exclude is not None and varname in exclude:
            continue #if exclude is defined, and this attribute is there

        ncout.variables[varname][:] = variable[:]
    
def copy_netcdf(input_filename, output_filename, *args, **kwargs):
    ncin = netCDF4.Dataset(input_filename)
    ncout = netCDF4.Dataset(output_filename, 'w',*args, **kwargs)
    
    copy_attributes(ncin, ncout)
    copy_dimensions(ncin, ncout)
    copy_variables(ncin, ncout)

    ncin.close()
    ncout.close()
    
def ensemble_define_variables(ncin, ncout, dimension_name="mode"):
    #create new dimension
    ncout.createDimension(dimension_name, 2)
    ensemble_variables = []
    for varname, variable in six.iteritems(ncin[0].variables):
        datatype = variable.dtype
        dimensions = variable.dimensions
        if len(dimensions) == 1 and varname in dimensions:
            #this is an axis dimension, skip the calculation.
            pass
        else:
            #not an axis dimension, save the name for later, add the dimension
            ensemble_variables.append(varname)
            dimensions = list(dimensions)
            dimensions.insert(1,dimension_name)
        fill_value = None
        if "missing_value" in variable.ncattrs():
            fill_value = variable.getncattr("missing_value")
        if "_FillValue" in variable.ncattrs():
            fill_value = variable.getncattr("_FillValue")
        outvariable = ncout.createVariable(varname, datatype, dimensions, fill_value=fill_value)
        #get the attributes
        copy_attributes(variable, outvariable, exclude=["missing_value","_FillValue"])
    
    iDenom = 1./len(ncin)
    for varname in ensemble_variables:
        data = ncin[0].variables[varname]
        if data.dtype == "S1":
            ncout.variables[varname][:,0] = data[:]
            continue
        #else
        m, v = data[:] * iDenom, data[:] * data[:] * iDenom
        if len(ncin) > 1:
            for nc in ncin[1:]:
                data = nc.variables[varname]
                m,v = m+data[:]*iDenom, v+data[:]*data[:]*iDenom
        v=v-m*m
        ncout.variables[varname][:,0] = m
        ncout.variables[varname][:,1] = v
        
def ensemble_mean_variance(input_filenames, output_filename, *args, **kwargs):
    ncin = [netCDF4.Dataset(f) for f in input_filenames]
    ncout = netCDF4.Dataset(output_filename, 'w',*args, **kwargs)
    
    copy_attributes(ncin[0], ncout)
    copy_dimensions(ncin[0], ncout)
    #add ensemble mean/variance dimension    
    ensemble_define_variables(ncin, ncout)
    
    for n in ncin:
        n.close()
    ncout.close()
