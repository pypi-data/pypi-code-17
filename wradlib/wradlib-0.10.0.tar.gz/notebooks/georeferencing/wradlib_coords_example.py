
# coding: utf-8

# This notebook is part of the $\omega radlib$ documentation: http://wradlib.org/wradlib-docs.
# 
# Copyright (c) 2016, $\omega radlib$ developers.
# Distributed under the MIT License. See LICENSE.txt for more info.

# # Computing cartesian coordinates for polar data

# In[ ]:

import numpy as np
import wradlib.georef as georef
import wradlib.io as io
import wradlib.util as util
import warnings
warnings.filterwarnings('ignore')


# ### Read the data
# 
# Here, we use an OPERA hdf5 dataset.

# In[ ]:

filename = 'hdf5/20130429043000.rad.bewid.pvol.dbzh.scan1.hdf'
filename = util.get_wradlib_data_file(filename)
pvol = io.read_OPERA_hdf5(filename)


# ### Count the number of datasets

# In[ ]:

ntilt = 1
for i in range(100):
    try:
        pvol["dataset%d/what" % ntilt]
        ntilt += 1
    except Exception:
        ntilt -= 1
        break


# ### Define radar location and scan geometry

# In[ ]:

nrays = int(pvol["dataset1/where"]["nrays"])
nbins = int(pvol["dataset1/where"]["nbins"])
rscale = int(pvol["dataset1/where"]["rscale"])
coord = np.empty((ntilt, nrays, nbins, 3))
for t in range(ntilt):
    elangle = pvol["dataset%d/where" % (t + 1)]["elangle"]
    coord[t, ...] = georef.sweep_centroids(nrays, rscale, nbins, elangle)
# ascale = math.pi / nrays
sitecoords = (pvol["where"]["lon"], pvol["where"]["lat"],
              pvol["where"]["height"])


# ### Retrieve geographic coordinates (longitude and latitude)

# In[ ]:

proj_radar = georef.create_osr("aeqd", lat_0=pvol["where"]["lat"],
                               lon_0=pvol["where"]["lon"])
radius = georef.get_earth_radius(pvol["where"]["lat"], proj_radar)

lon, lat, height = georef.polar2lonlatalt_n(coord[..., 0],
                                            np.degrees(coord[..., 1]),
                                            coord[..., 2], sitecoords,
                                            re=radius, ke=4. / 3.)


# ### Reproject to Azimuthal Equidistant projection

# In[ ]:

x, y = georef.reproject(lon, lat, projection_target=proj_radar)

test = x[0, 90, 0:960:60]
print(test)

