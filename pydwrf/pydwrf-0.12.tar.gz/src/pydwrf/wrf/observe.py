# from argh import ArghParser
# import dwell.rad.terminal as terminal
# import netCDF4
# import dwell.climate as climate
# import numpy as np
# from . import variables
# import itertools
# import cPickle
# import progressbar
# import info
# import pydwrf.tes.nc as tesnc
# import logging
# from . import postprocess
# 
# def surface_temperature(observation_file,atmosphere_file):
#     pass
# 
# def mtc_decimal(tt):
#     #calculates Mars Coordinated Time from the Times string
#     days_in_year = 669.
#     date_to_days = [days_in_year,1.,1./24,1./(24.*60),1./(24*60*60.)]
#     #sum(a*b for a,b in zip(tt,date_to_days))
#     hour = 24.*sum(a*b for a,b in zip(tt[2:],date_to_days[2:]))
#     return hour
# 
# def mtc_time(atmosfile):
#     return np.array([mtc_decimal(info.time_tuple("".join(t))) for t in atmosfile.variables["Times"][:]])
# 
# def inrange(a,b):
#         return (a>=min(b)) & (a<max(b))
# 
# def bin_axis(axis,data_segment):
#     bins = dict(zip(["mean","var","count",
#                      "forward_index",
#                     "reverse_index","reverse_index_count"],
#                     climate.grid_data(np.vstack([data_segment]).T, 
#                                        [axis],
#                                        reverse_indices=True,
#                                        sparse=True)))
#         
#     inverse_map = np.empty(len(data_segment),dtype=int)
#     for f,r in zip(bins["forward_index"],bins["reverse_index"]):
#         inverse_map[r]=f
#     return bins, inverse_map
# 
# def observe(observation_file, atmosphere_file, output_filename=None,
#     obsx="LONGITUDE",obsy="LATITUDE",obstime="SOLAR_LONGITUDE",
#     obsvar=None,
#     atmosx="XLONG",atmosy="XLAT",atmostime="L_S",
#     atmosvar=None, extremely_verbose=False
#     ):
#     log = logging.getLogger("observe")
#     #load the files
#     atmosfile = netCDF4.Dataset(atmosphere_file)
#     obsfile = netCDF4.Dataset(observation_file)
# 
#     #get the obs locations from the obs file
#     ss=slice(None,None,1)
#     obs=dict(x=obsfile.variables[obsx][ss].squeeze(),
#                  y=obsfile.variables[obsy][ss].squeeze(),
#                  time=obsfile.variables[obstime][ss].squeeze(),
#                  localtime=obsfile.variables["local_time_m"][ss].squeeze(),
#                  data=obsfile.variables[obsvar][ss].squeeze()
#     )
#     
#     obs["mtctime"] = (obs["localtime"] - obs["x"]/15.) % 24
# 
#     #get the data locations from the data file, and a blank array to store results
#     data=dict(x=atmosfile.variables[atmosx][0,0,:].squeeze(),
#                   y=atmosfile.variables[atmosy][0,:,0].squeeze(),
#                   time=atmosfile.variables[atmostime][:].squeeze(),
#                   data=np.ma.array(obs["data"]*.0,mask=True),
#                   mtctime=mtc_time(atmosfile)
#     )
# 
# 
#     obs["x"][obs["x"]>180.] -= 360. 
#     #restrict data time axis to be monotonic
#     monotonic_time,slices = variables.monotonic(data["time"],return_slices=True)
# 
#     #build a reusable index array of each corner of the cube.
#     #interpolation indices for later in the calculation.
#     int_indices = np.indices((2,2,2)).reshape((3,8)).T
#     #For some quicker math, we write the interpolation as
#     #weighted_mean = sum ( data * weights )
#     #the data comes from the int_data array above, flattened to be a list of 8 numbers
#     #the weights come from the suitable product of each dimensions individual weight 
#     #in a bi-linear calculation.
#     #The weight for a dimension given a fractional distance f from point p_i 
#     #is w_i+1 = f
#     # and w_i = 1-f
#     #so we construct the 8 weights simultaneously using the indices array above
#     #realizing that all points have the weight of product(ijk)((1-i) + (2*i - 1)*f)
#     #such that for lower points in any dimension the result is (1-0) + (2*0-1)*f = 1-f
#     #and for upper points the result is (1-1) + (2*1-1)*f = f
#     #Mscale and Moff are calculated for this purpose and are unchanged throughout the code.
#     Mscale = int_indices *2. - 1.
#     Moff = 1.-int_indices
#     
#     for isl,sl in enumerate(slices):
#         #A slice of data is a single year of WRF data that we can map the observations onto.
#         #Start by finding the nearest bin in Ls space for each observation
#         count=0
#         #zero out data to make sure
#         data["data"]*=0.
#         #filter the observations in this Ls range just in case we have 
#         #a truncated WRF year.
#         fil =   inrange(obs["time"],data["time"][sl]) &\
#                     inrange(obs["x"],data["x"]) &\
#                     inrange(obs["y"],data["y"])
# 
#         ww=np.where(fil)
# 
#         #should we return early if there are no GCM data points for these observations
#         if len(ww) ==0:
#             continue
#         elif len(ww[0])==0:
#             continue
#         ww=ww[0]
#         log.info("total={0}".format(len(ww)))
#                                         
#         lsbins,mtc_map = bin_axis(data["time"][sl],obs["time"][ww])
#         xbins,x_map = bin_axis(data["x"],obs["x"][ww])
#         ybins,y_map = bin_axis(data["y"],obs["y"][ww])
#     
#         
#         delta_mtc_wrf = np.diff(data["mtctime"]) % 24
#         if not inrange(max(delta_mtc_wrf)-min(delta_mtc_wrf),[-1e-5,1e-5]):
#             print "Time Deltas are not constant in model output" 
#             break
#         mean_delta_mtc_wrf = np.mean(delta_mtc_wrf)
#         #build a map from each element in the obs array to elements in the model array
#         #this is equivalent to populating an array using the reverse_index as the key and 
#         #forward_index as the value.
#     
#         delta_mtc = (obs["mtctime"][ww] - data["mtctime"][mtc_map])
#         delta_mtc[delta_mtc > 12] = delta_mtc[delta_mtc > 12]-24.
#     #    for mw,mo,d,d2 in zip(mtc_wrf[mtc_map],mtc_obs, delta_mtc):
#     #        print mo, mw, d
#         #Now we have a close Ls point in the model data for each observation
#         #We also have the real MTC, the model MTC of the close Ls point
#         #We have the delta time between them in shortest path
#         #We have the spacing between bins
#     
#         delta_bins = np.ceil(delta_mtc / mean_delta_mtc_wrf).astype(int)
#         corrected_bins = mtc_map + delta_bins
#         
#         #in corrected_bins we have the nearest local time bin and nearest Ls bin, with a preference to 
#         #getting the local time closer because the effect is stronger.
#         #in a test, typical Ls deviations were -0.03+-0.15
#     
#         #Now we can interpolate in space.
#         
#         #calculate the shape of the 3D array that would be constructed out of the sparse array
#         #for use by unravel_index to rebuild data and sample the GCMs raw data.
#         bins = [corrected_bins,y_map,x_map]
#         myobs_data = dict(zip(["mtctime","y","x","data"],[obs[var][fil] for var in "mtctime","y","x","data"]))
#         shp = tuple([len(b) for b in data["time"],data["y"],data["x"]])
#         from progressbar import ProgressBar
#         mytsk=atmosfile.variables["TSK"][:]
#         for ri,fi in enumerate(ProgressBar()(zip(*bins))):
#             index_high = fi
#             index = [f-1 for f in fi]
#             #ww contains a list if indices in the original array that went into the the gridded data
#             #so ww[ri] would be a list of original boxes to store in a simulated observation array
#             #we can check this is true... by comparing obs_data[-2] below to obs["data"][obs_data[-1]]
#             fil2=ww[ri]
#             def retrieve_cube(data, index,shp):
#                 if np.any(np.array(index) < 0) or np.any(np.array(index)-shp >= -1):
#                     #slow method
#                     #res = np.empty(2,2,2)
#                     #offsets = np.indices((2,2,2)).reshape((3,8)).T
#                     #for o in offsets:
#                     #   v = tuple(np.clip(a,0,b-1) for a,b in zip(o,shp))
#                     #print v
#                     #import sys
#                     
#                     raise ("bad data point for interpolation")
#                     pass
#                 else:
#                     #fast method
#                     #build up the slices to be Nt:Nt+2,Ny:Ny+2,nx:Nx+2, constrained
#                     #to be physical which shouldn't be a problem here.
#                     #that should be dealt with the code above.
#                     slices = [slice(i,i+2 if i<j-1 else None,1) for i,j in zip(index,shp)]
#                     return data[slices]
#     
#             if extremely_verbose:
#                 print "calculation"
#                 print "index=", index
#                 print "shp=", shp
#                 print "obs= ", obs["time"][fil2],obs["y"][fil2],obs["x"][fil2],obs["mtctime"][fil2]
#                 print "data= ",data["time"][fi[0]],data["y"][fi[1]],data["x"][fi[2]],data["mtctime"][fi[0]]
#                 
# 
#             #grab the data out of the input data file
#             #by passing the variable, the location of the bottom left and the shape 
#             #(for clipping) into the retrieve_cube function
#             try:
#                 int_data = retrieve_cube(mytsk,index,shp).flatten()
#             except:
#                 data["data"][fil2].mask=True
#                 continue
#     
#             #build the local obs_data array
#             #consisting of the time and location for each element that would go into
#             #this aggregate box listed in ri
#             
#             obs_data= [myobs_data[var][ri] for var in "mtctime","y","x","data"]
#             obs_data.append(fil2)
#     
#             #axis values on the bottom front left side
#             data_axisM = np.array([data["mtctime"][index[0]],#data["time"][sl][index[0]], 
#                             data["y"][index[1]],    
#                             data["x"][index[2]]])
#             
#             #axis values on the top back right side
#             data_axisP = np.array([data["mtctime"][index[0]+1],#data["time"][sl][index[0]+1],
#                             data["y"][index[1]+1],  
#                             data["x"][index[2]+1]])
#             if data_axisP[0]<data_axisM[0]:
#                 data_axisP[0]+=24.
# 
#             count+=1
#             #calculate the fraction distance (i.e. weight) along each axis
#             delta = (obs_data[:3]-data_axisM)/(data_axisP-data_axisM)
#             #interpolate the data
#             mean = np.sum(np.product(Moff+Mscale*delta,axis=1)*int_data)
#             #store the data in the big array
#             data["data"][obs_data[-1]] = mean
#             #print "box number=",box, x[-1]
#             if extremely_verbose:
#                 print "axisM=", data_axisM
#                 print "axisP=", data_axisP
#                 print "source_data= ", int_data
#                 print "coords= ",obs_data[:3]
#                 print "delta= ",delta
#                 print data["data"][obs_data[-1]], obs_data[-2], int_data
#         finaldata = dict(x=obs["x"][ww],
#              y=obs["y"][ww],
#              time=obs["time"][ww],
#              localtime=obs["localtime"][ww],
#              obstsk=obs["data"][ww],
#              wrftsk=data["data"][ww]
#              )
#         
#         def build_variable(data, dimensions, typ):
#             return dict(data=data,
#                         dimensions=dimensions,
#                         type=typ)
#         def build_dimension(name,data,type):
#             return dict(array=data,
#                         type=type,
#                         dimensions=name)
# 
#         #WRITE TO NETCDF
#         if output_filename is None:
#             output_filename="observed.{0}.nc".format(atmosphere_file)
#         print output_filename
#         postprocess.make_sure_path_exists_for_filename(output_filename)
#         ncout = netCDF4.Dataset(output_filename,'w')
#         tesnc.create_dimensions(ncout,
#                                 dict(time=build_dimension("time",
#                                                           finaldata["time"],
#                                                           finaldata["time"].dtype
#                                     )))
#         vardict = dict((name,build_variable(finaldata[name],
#                                                 "time",
#                                                 finaldata[name].dtype
#                                                 )) for name in ["x","y","localtime","obstsk","wrftsk"])
#         
# 
#         vars = tesnc.create_variables(ncout,vardict)
#         for k,v in vars.items():
#             v[:]=finaldata[k]
#         ncout.close()
#         #cPickle.dump(finaldata,open("observed.{0}.{1}".format(atmosphere_file,isl),'w'))
# 
# 
# def observetes(observation_file, atmosphere_file, output_filename=None,
#     ):
# 
#     obsx="longitude_m"
#     obsy="latitude_m"
#     obsvar="target_temperature_m"
#     obstime="solar_longitude_m"
# 
#     with postprocess.flock("{0}.lock".format(atmosphere_file)):
#         observe(observation_file, atmosphere_file, 
#             output_filename=output_filename,
#             obsx=obsx,obsy=obsy,obstime=obstime,
#             obsvar=obsvar)
# 
# def main():
#     terminal.argh_main("observe",[observe,observetes])
