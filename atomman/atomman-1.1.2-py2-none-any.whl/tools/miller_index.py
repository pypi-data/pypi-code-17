import numpy as np


def miller_to_cartesian(miller, avect=None, bvect=None, cvect=None, vects=None, system=None, box=None):
    """
    Conversion tool that converts a crystallographic vector (in Miller or 
    Miller-Bravais indices) to a Cartesian vector.
    
    Arguments:
    miller -- list/tuple/array of 3 or 4 integers representing a 
              crystallographic direction. 3 terms corresponds to the classic
              Miller indices, while 4 terms corresponds to the Miller-Bravais
              indices as used with hexagonal systems. 

    Keyword Arguments:
    avect, bvect, cvect -- The three individual box vectors
    vects -- a 3x3 array containing the three box vectors
    system -- an atomman.System from which box vectors can be taken
    box -- an atomman.Box to take vectors from
    
    Returns a numpy array for a 3D vector.
    """
    
    #Check box vectors
    if   avect is not None or bvect is not None or cvect is not None:
        assert avect is not None and bvect is not None and cvect is not None,   'avect, bvect and cvect must all be given if one is given'
        assert vects is None,                                                   'vects cannot be given with avect, bvect, cvect'
        assert system is None,                                                  'system cannot be given with avect, bvect, cvect'
        assert box is None,                                                     'box cannot be given with avect, bvect, cvect'
        vects = np.array([avect, bvect, cvect])
    elif vects is not None:
        assert system is None,                                                  'system cannot be given with vects'
        assert box is None,                                                     'box cannot be given with vects'
        vects = np.asarray(vects)
    elif system is not None:
        assert box is None,                                                     'box cannot be given with system'
        vects = system.box.vects
    elif box is not None:
        vects = box.vects
    else:
        vects = np.identity(3)
        
    #Check miller
    miller = np.asarray(miller)
    if miller.shape = (4,):
        assert miller[0]+miller[1]+miller[2] == 0, 'invalid Miller-Bravais indices'
        
        
        
def miller_4_to_3(uvtw):
    """
    Converts from Miller-Bravais four-term index to Miller three-term index.
    
    Arguments:
    uvtw -- list/tuple/array of four integers representing a Miller-Bravais 
            set of indices.
                  
    returns a numpy array of three integers.
    """
    
    #Convert to numpy integer array
    uvtw = np.asarray(uvtw, dtype=int)
    assert uvtw[0] + uvtw[1] + uvtw[2] == 0, 'invalid Miller-Bravais indices'
    
    #Build 3 term indices
    uvw = np.empty(3, dtype=int)
    uvw[0] = 6 * uvtw[0] + 3 * uvtw[1]
    uvw[1] = 6 * uvtw[1] + 3 * uvtw[0]
    uvw[2] = 3 * uvtw[3]
    
    #Reduce to smallest integers
    for i in xrange(uvw.max(), 1, -1):
        while np.array_equal(np.mod(uvw, i), np.zeros(3, dtype=int)):
            uvw = uvw / i
    
    return uvw
    
    
def miller_3_to_4(uvw):
    """
    Converts from Miller-Bravais three-term index to Miller four-term index.
    
    Arguments:
    uvw -- list/tuple/array of three integers representing a Miller set of 
               indices.
                   
    returns a numpy array of four integers.
    """
    
    #Convert to numpy integer array
    uvw = np.asarray(uvw, dtype=int)
    
    #Build 4 term indices
    uvtw = np.empty(4, dtype=int)
    uvtw[0] = 2 * uvw[0] - uvw[1]
    uvtw[1] = 2 * uvw[1] - uvw[0]
    uvtw[2] = -(uvtw[0] + uvtw[1])
    uvtw[3] = 3 * uvw[2]
    
    #Reduce to smallest integers
    for i in xrange(uvtw.max(), 1, -1):
        while np.array_equal(np.mod(uvtw, i), np.zeros(4, dtype=int)):
            uvtw = uvtw / i
    
    return uvtw   