import marstime
from . import tes_time
import copy
import numpy
import dwell.climate as climate
from collections import OrderedDict as odict

def add_variables(data, nlines_read):
    """Add Model specific data, such as Ls, MSD, LMST, LTST"""
    
    if "ephemeris_time" in data:
        def from_ephem(data, function):
            res = copy.deepcopy(data["ephemeris_time"])
            et = data["ephemeris_time"]["array"]
            shp = et.shape
            et = numpy.reshape(et,et.size)
            res["array"][:] = numpy.reshape(function(et),shp)
            return res
            
    #mars solar date
        data["mars_solar_date"] = from_ephem(data, tes_time.convert_ephemeris_time_to_msd)
    #Ls
        data["mars_ls"] = from_ephem(data, tes_time.convert_ephemeris_time_to_Ls)
    #time axis
        data["Time"] = from_ephem(data, tes_time.convert_ephemeris_time_to_msd)
    return data, nlines_read

def convert_longitude_from_TES_to_MOLA(data, nlines_read):
    """This function convert the longitude form IAU1990 to IAU2000 
    by subtracting 0.271 degrees from the west longitude stored, and converts
    the longitude to from west longitude to east longitude [-180,180)"""
    
    if "longitude" in data:
        west_longitude_tes = data["longitude"]["array"]
        #convert to mola longitude
        east_longitude_mola = 360. - west_longitude_tes + 0.271
        #constrain to be > 0 less than 360
        east_longitude_mola = east_longitude_mola % 360.
        #shift to -180 to +180
        filter180 = east_longitude_mola > 180
        east_longitude_mola[filter180] = east_longitude_mola[filter180]-360.    
    elif "longitude_iau2000" in data:
        east_longitude_mola = data["longitude_iau2000"]["array"]
        #convert to mola longitude
        #east_longitude_mola = 360. - west_longitude_tes + 0.271
        #constrain to be > 0 less than 360
        #east_longitude_mola = east_longitude_mola % 360.
        #shift to -180 to +180
        #filter180 = east_longitude_mola > 180
        #east_longitude_mola[filter180] = east_longitude_mola[filter180]-360.
        data["longitude"] = data["longitude_iau2000"]
        data["longitude"]["array"] = east_longitude_mola
    return data, nlines_read
    
def aggregate_data(data, nlines_read, nxbins=121, nybins=61, longest_period_days=1./24/60.):
    """This function aggregates the buffer of data into horizontal boxes of 5 degrees 
    and a time of 60 minutes"""
    longest_period_days = 1./24 / 60.
    sel = slice(0,nlines_read,1)
    xbins = (numpy.arange(nxbins-1)+1) * (360./(nxbins-1))-180 #upper bounds on X
    ybins = (numpy.arange(nybins-1)+1) * (360./(nybins-1))-90 #upper bounds on Y
    
    #time
    msd = data["mars_solar_date"]["array"][sel]
    msd_int = numpy.floor(msd)
    msd_sec = numpy.floor((msd - msd_int)*86400.) #seconds
    
    msd_low = msd_int[0] + (numpy.ceil(msd_sec[0]/3600.))/24.
    msd_high = msd_int[-1] + (numpy.ceil(msd_sec[-1]/3600.))/24.
    msd_hours = numpy.arange(msd_low, msd_high+longest_period_days,longest_period_days)
#    print msd_hours
    #now we assume that the following exists
    #latitude, longitude, msd (which we made)
    
    #This section builds the list of axis over which we grid our data, in this case
    #we want to grid over longitude, latitude, and time. 
    #adding these to the start of the list tells grid_data where to find the index data,
    #but these won't appear in the final results, so we add them again later with the
    #rest of the data
    stacked = []
    names = odict()
    req = [s for s in ["mars_solar_date","longitude","latitude"] if s in data]
    bindict = dict(zip(["mars_solar_date","longitude","latitude"],[msd_hours, xbins, ybins]))
    bins = [bindict[s] for s in req]

    #add required
    def within(a,b,e):
        return numpy.abs((a-b)) < e
        
    for r in req:
        #squeeze to remove the annoying '1' dimensions, mask the data with our missing data
        #value so that averages are correct and not screwed up by missing data
        #and transpose so that we can re-stack things later into two dimensions
        stacked.append(numpy.squeeze(
                        numpy.ma.array(
                                data[r]["array"],
                                mask=data[r]["array"]==data[r]["missing_value"]),
                                ).T)

    counter=0
    for r in [k for k in data.keys()]:
        #for later, we want to know which part of the results this corrsponds to
        #save the start and end points in the array in names[r]
        if numpy.ndim(numpy.squeeze(data[r]["array"])) > 1:
            length = data[r]["array"].shape[-1]
        else:
            length = 1
        names[r] = [counter,counter+length]
        counter+=length
        #perform the same squeeze,mask,transpose as before
        stacked.append(numpy.squeeze(
                            numpy.ma.array(
                                data[r]["array"],
                                mask=data[r]["array"]==data[r]["missing_value"]),
                                ).T)

    #now we have the data in a list, stack it into a 2D numpy variable
    stacked = numpy.ma.vstack(stacked).T
    #by default, grid_data produces an N dimension grid with boxes corresponding to 
    #each of the axis bins (xbins, ybins, msd_hours), but this makes a large structure
    #and we probably won't fill it up (ever) so we ask for sparse results
    #In sparse mode each filled box is returned as a single row, and no empty boxes
    #are returned, we added the axis values into the gridding array twice earlier so
    #that the second copy is treated as data and their mean/variance/count is also
    #returned
    sparse=True
    #mean, variance, count = climate.grid_data(stacked, [xbins, ybins, msd_hours], sparse=sparse)
    #msd_hours is first to make it the first sorting axis, rather than x or y
    mean, variance, count,forward_index = climate.grid_data(stacked, bins, sparse=sparse)
#nogridding
#    mean = stacked[:,3:]
#    variance = stacked[:,3:]*0.0
#    count = stacked[:,3:]*0.0
    #note the output from the grid_data function is not monotonic in msd_hours, it's monotonic in the
    #grid box index that starts (in this case) with ybins being monotonic and below the first ybins box
    #then xbins increments by a grid box threshold, and ybins resets. e.g. in some trivial world where we grid integers
    #the axis might look like
    # 0 0 0
    # ...
    # 0 0 9
    # 0 1 0 <- last bin changed by -9
    #...
    # 0 5 9 
    # 1 0 2 <- second bin change by -5, last by -7
    
    #In this gridding, the msd is the slowest varying, but it is erratic within it's defined (30 minute) windows 
    #so we need to sort. We use argsort here to calculate the indices of the unsorted array based on msd (linear in ephemeris time)
    #and apply it layer to data_segment
    
    inds = numpy.argsort(numpy.squeeze(mean[:,names["mars_solar_date"][0]]))

    #now we have the data aggregated, we need to rebuilt the output structure with new variables
    #as before, each dimension has a type, dimensions, and the extra dictionary containing the missing value
    #nothing changes here except the number of 'lines' we have. so we can reuse the old data structure
    #but we should create new variables for mean and var of each old variable
    #count is also unique for each variable, because of missing data, so we need 3 variables for each old variable
    new_data = odict()
    for n in names:
        sl = slice(names[n][0],names[n][1],1)
        data_segment = dict(m=mean[inds,sl], 
                        v=variance[inds,sl],
                        c=count[inds,sl])
        extra = dict(m=data[n]["extra"])
        for letter in ["m","v","c"]:
            new_name = "{0}_{1}".format(n,letter)
            new_data[new_name] = dict(type=data_segment[letter].dtype,
                            array=data_segment[letter],
                            dimensions = data[n]["dimensions"])
            if letter in extra:
                new_data[new_name]["extra"] = extra["m"]
    #at this point we have the data restructured in new_data, return that and the number of elements as mean.shape[0]
    
    return new_data, mean.shape[0]
