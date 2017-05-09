# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 10:09:10 2017

@author: u0078867
"""

import sys
import os

modPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../')
sys.path.append(modPath)


from PyBiomech import procedure_or as proc
from PyBiomech import vtkh, fio, kine
from PyBiomech import mplh
import csv
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as m3d



# Necessary arguments
filePathC3D = 'Spec04_left_ukaFB_tibiaComponent_ridge.c3d'
filePathMimics = 'Spec4_15L_GlobalCS_Landmarks.txt'
refSegment = 'tibia'
segSTLFilePath = '4_15Lnewsegmentation.stl'
verbose = True


# Init data to show
dataToShow = []

# Add tibia mesh to data to show
item = {}
item['name'] = 'tibia'
item['type'] = 'STL'
item['filePath'] = segSTLFilePath
item['opacity'] = 1.
dataToShow.append(item)



# Read Mimics file
tip, tipReduced = proc.expressOptoWandTipToMimicsRefFrame(
                                        filePathC3D, 
                                        filePathMimics, 
                                        'MyPoint', 
                                        refSegment,
                                        filePathNewC3D = None,
                                        reduceAs = None,
                                        segSTLFilePath = segSTLFilePath,
                                        verbose = verbose,
                                        showNavigator = False,
                                        forceNoPauses = True
                                        )

 
# Write point cloud coordinates to file
with open('tip.txt', 'wb') as f:
    fieldNames = ['x', 'y', 'z']
    writer = csv.DictWriter(f, fieldnames=fieldNames)
    writer.writeheader()
    writer.writerows([{'x':t[0], 'y':t[1], 'z':t[2]} for t in tip])

# Create line item to show
item = {}
item['name'] = 'tracked_line'
item['type'] = 'line'
item['coords'] = tip
item['color'] = (255,0,0)
dataToShow.append(item)

# Create point cloud to export
pointCloud = []
for i in xrange(tip.shape[0]):
    item = {}
    item['name'] = 'point_' + str(i)
    item['type'] = 'point'
    item['coords'] = tip[i,:]
    pointCloud.append(item)

# Export to XML
fio.writeXML3Matic('tip.xml', pointCloud)

# Fit stright line with SVD
versor, center, other = kine.lineFitSVD(tip)
proj = other['proj']
linePoints = versor * np.mgrid[proj.min():proj.max():30j][:, np.newaxis]
linePoints += center

# Create straight to export
item = {}
item['name'] = 'fitted_straight_line'
item['type'] = 'line'
item['coords'] = linePoints
item['color'] = (0,255,0)
dataToShow.append(item)

# Export to XML
fio.writeXML3Matic('line.xml', [item])

# Plot 3D regression
ax = m3d.Axes3D(plt.figure())
ax.scatter3D(*tip.T)
ax.plot3D(linePoints[:,0], linePoints[:,1], linePoints[:,2], 'ro')
ax.set_aspect('equal')
mplh.set_axes_equal(ax)
plt.show()

# Show actors
vtkh.showData(dataToShow)




    
    