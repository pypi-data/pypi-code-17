# from argh import ArghParser
# import dwell.rad.terminal as terminal
# import netCDF4
# import dwell.climate as climate
# import numpy as np
# import variables
# import itertools
# import cPickle
# import progressbar
# 
# def surface_temperature(observation_file,atmosphere_file):
# 	pass
# 
# def observe(observation_file, atmosphere_file,
# 	obsx="LONGITUDE",obsy="LATITUDE",obstime="SOLAR_LONGITUDE",
# 	obsvar=None,
# 	atmosx="XLONG",atmosy="XLAT",atmostime="L_S",
# 	atmosvar=None,
# 	):
# 
# 	#load the files
# 	atmosfile = netCDF4.Dataset(atmosphere_file)
# 	obsfile = netCDF4.Dataset(observation_file)
# 
# 	#get the obs locations from the obs file
# 	ss=slice(None,None,1)
# 	obs=dict(x=obsfile.variables[obsx][ss].squeeze(),
# 			 y=obsfile.variables[obsy][ss].squeeze(),
# 			 time=obsfile.variables[obstime][ss].squeeze(),
# 			 data=obsfile.variables[obsvar][ss].squeeze()
# 		)
# 	#get the data locations from the data file, and a blank array to store results
# 	data=dict(x=atmosfile.variables[atmosx][0,0,:].squeeze(),
# 			  y=atmosfile.variables[atmosy][0,:,0].squeeze(),
# 			  time=atmosfile.variables[atmostime][:].squeeze(),
# 			  data=np.ma.array(obs["data"]*.0,mask=True)
# 		)
# 
# 	obs["x"][obs["x"]>180.] -= 360. 
# 	#restrict data time axis to be monotonic
# 	monotonic_time,slices = variables.monotonic(data["time"],return_slices=True)
# 
# 	def inrange(a,b):
# 		return (a>=min(b)) & (a<max(b))
# 
# 	for isl,sl in enumerate(slices):
# 		count=0
# 		#zero out data to make sure
# 		data["data"]*=0.
# 		#filter out all out of bounds data before binning
# 		fil = 	inrange(obs["time"],data["time"][sl]) &\
# 				inrange(obs["x"],data["x"]) &\
# 				inrange(obs["y"],data["y"])
# 		print "total=",sum(fil)
# 		wh=np.where(fil)
# 		#should we return early because there are no GCM data points for these observations
# 		if len(wh) ==0:
# 			continue
# 		elif len(wh[0])==0:
# 			continue
# 		wh=wh[0]
# 
# 		#contruct the GCM bins to index the observations into
# 		bins = [data["time"][sl],data["y"],data["x"]]
# 		
# 		#grid the data by finding the correct GCM x,y,t bins for each point in obs
# 		#saved in a sparse file because it's a nearly empty Ndimensional array, and return
# 		#the reverse indices array that puts each aggregate point in the forward index back into
# 		#the source array (obs[*][fil])
# 		d=climate.grid_data(
# 			np.vstack([obs["time"][fil],obs["y"][fil],obs["x"][fil]]).T,
# 			bins,sparse=True,reverse_indices=True)
# 
# 		#test observation on d
# 		#each gridded dataset contains mean,variance, count of the (null) data
# 		#the forward index that maps each point in the source to the aggregated destination
# 		#the reverse index that maps each aggregated point back to the source
# 		#and the number of indices in each of the bins of the reverse_index array
# 		#which I guess must match the count array *unless* there is missing data
# 		m,v,c,fi,ri,rj = d
# 		#calculate the shape of the 3D array that would be constructed out of the sparse array
# 		#for use by unravel_index to rebuild data and sample the GCMs raw data.
# 		shp = tuple([len(b) for b in bins])
# 		
# 		#for each aggregated bin in fi, loop through and performd some operations
# 		for box in range(len(fi)):
# 
# 		#for box in progressbar.ProgressBar()(range(len(fi))):
# 			#This element has a unique location in the GCM dataset, find it.
# 			index=np.array(np.unravel_index(fi[box],shp))
# 			#index returns the element at the "top back right" of the cube, we
# 			#want the "bottom front left" instead, subtract 1 of each point.
# 			index=np.array([i-1 for i in index]) 
# 
# 			def retrieve_cube(data, index,shp):
# 				if np.any(np.array(index) < 0) or np.any(np.array(index)-shp > -1):
# 					#slow method
# 					#res = np.empty(2,2,2)
# 					#offsets = np.indices((2,2,2)).reshape((3,8)).T
# 					#for o in offsets:
# 					#	v = tuple(np.clip(a,0,b-1) for a,b in zip(o,shp))
# 					#print v
# 					#import sys
# 					print "This has never happened, I think because of prefiltering"
# 					sys.exit(1)
# 					return None
# 					pass
# 				else:
# 					#fast method
# 					#build up the slices to be Nt:Nt+2,Ny:Ny+2,nx:Nx+2, constrained
# 					#to be physical which shouldn't be a problem here.
# 					#that should be dealt with the code above.
# 					slices = [slice(i,i+2 if i<j-1 else None,1) for i,j in zip(index,shp)]
# 					return data[slices]
# 
# 			#grab the data out of the input data file
# 			#by passing the variable, the location of the bottom left and the shape 
# 			#(for clipping) into the retrieve_cube function
# 			int_data = retrieve_cube(atmosfile.variables["TSK"],index,shp).flatten()
# 			#build a reusable index array of each corner of the cube.
# 			int_indices = np.indices((2,2,2)).reshape((3,8)).T
# 			#For some quicker math, we write the interpolation as
# 			#weighted_mean = sum ( data * weights )
# 			#the data comes from the int_data array above, flattened to be a list of 8 numbers
# 			#the weights come from the suitable product of each dimensions individual weight 
# 			#in a bi-linear calculation.
# 			#The weight for a dimension given a fractional distance f from point p_i 
# 			#is w_i+1 = f
# 			# and w_i = 1-f
# 			#so we construct the 8 weights simultaneously using the indices array above
# 			#realizing that all points have the weight of product(ijk)((1-i) + (2*i - 1)*f)
# 			#such that for lower points in any dimension the result is (1-0) + (2*0-1)*f = 1-f
# 			#and for upper points the result is (1-1) + (2*1-1)*f = f
# 			#Mscale and Moff are calculated for this purpose and are unchanged throughout the code.
# 			Mscale = int_indices *2. - 1.
# 			Moff = 1.-int_indices
# 
# 			#wh contains a list if indices in the original array that went into the the gridded data
# 			#so wh[ri] would be a list of original boxes to store in a simulated observation array
# 			#we can check this is true... by comparing obs_data[-2] below to obs["data"][obs_data[-1]]
# 			fil2=wh[ri[box]]
# 			
# 			#build the local obs_data array
# 			#consisting of the time and location for each element that would go into
# 			#this aggregate box listed in ri
# 
# 			obs_data= [obs[var][fil][ri[box]] for var in "time","y","x","data"]
# 			obs_data.append(fil2)
# 
# 			#axis values on the bottom front left side
# 			data_axisM = np.array([data["time"][sl][index[0]], 
# 							data["y"][index[1]],	
# 							data["x"][index[2]]])
# 			
# 			#axis values on the top back right side
# 			data_axisP = np.array([data["time"][sl][index[0]+1],
# 							data["y"][index[1]+1],	
# 							data["x"][index[2]+1]])
# 
# 			#loop through each source point here, interpolate the GCM to that location
# 			for x in np.array(obs_data).T:
# 				count+=1
# 				#calculate the fraction distance (i.e. weight) along each axis
# 				delta = (x[:3]-data_axisM)/(data_axisP-data_axisM)
# 				#interpolate the data
# 				mean = np.sum(np.product(Moff+Mscale*delta,axis=1)*int_data)
# 				#store the data in the big array
# 				data["data"][x[-1]] = mean
# 				#print "box number=",box, x[-1]
# 		print "count=",count
# 	
# 		cPickle.dump(dict(obs=obs,data=data),open("{0}.observed.{1}".format(atmosphere_file,isl),'w'))
# 
# def main():
# 	terminal.argh_main("observe",[observe])# 