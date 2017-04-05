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

# Necessary arguments
filePathC3D = 'FMCC.c3d'
filePathMimics = 'landmarks.mimics.txt'
wantTipName = 'MyPoint'
refSegment = 'femur'

# Optional arguments
reduceAs = 'avg_point'  # show average point
#reduceAs = None  # show line
filePathNewC3D = 'FMCC_tip.c3d'
segSTLFilePath = 'femur.stl'
verbose = False
showNavigator = True
forceNoPauses = False

# Read Mimics file
tip, tipReduced = proc.expressOptoWandTipToMimicsRefFrame(
                                        filePathC3D, 
                                        filePathMimics, 
                                        wantTipName, 
                                        refSegment,
                                        filePathNewC3D = filePathNewC3D,
                                        reduceAs = reduceAs,
                                        segSTLFilePath = segSTLFilePath,
                                        verbose = verbose,
                                        showNavigator = showNavigator,
                                        forceNoPauses = forceNoPauses
                                        )

print tip