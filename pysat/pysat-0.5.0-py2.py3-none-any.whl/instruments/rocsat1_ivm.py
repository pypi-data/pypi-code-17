# -*- coding: utf-8 -*-
"""Supports the Ion Velocity Meter (IVM)
onboard the Republic of China Satellite (ROCSAT-1). Downloads data from the
NASA Coordinated Data Analysis Web (CDAWeb).

Parameters
----------
platform : string
    'rocsat1'
name : string
    'ivm'
tag : string
    None

Note
----
- no tag required

Warnings
--------
- Currently no cleaning routine.
        
"""

from __future__ import print_function
from __future__ import absolute_import
import pandas as pds
import numpy as np
import pysat
import sys

import functools


from . import nasa_cdaweb_methods as cdw

# support list files routine
# use the default CDAWeb method
fname = 'rs_k0_ipei_{year:04d}{month:02d}{day:02d}_v01.cdf'
supported_tags = {'':fname}
list_files = functools.partial(cdw.list_files, 
                               supported_tags=supported_tags)
# support load routine
# use the default CDAWeb method
load = cdw.load

# support download routine
# use the default CDAWeb method
basic_tag = {'dir':'/pub/data/rocsat/ipei',
            'remote_fname':'{year:4d}/'+fname,
            'local_fname':fname}
supported_tags = {'':basic_tag}
download = functools.partial(cdw.download, supported_tags)
                
                    
def clean(inst):
    """Routine to return ROCSAT-1 IVM data cleaned to the specified level

    Parameters
    -----------
    inst : (pysat.Instrument)
        Instrument class object, whose attribute clean_level is used to return
        the desired level of data selectivity.

    Returns
    --------
    Void : (NoneType)
        data in inst is modified in-place.

    Notes
    --------
    No cleaning currently available for ROCSAT-1 IVM.
    """

    return None
                    
                    
                    
                    
                    


