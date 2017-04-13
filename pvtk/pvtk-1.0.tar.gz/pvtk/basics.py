#|- Funtions List in [.basics]:
#   |- roll_zeropad
#   |- shift
#      |- roll_zeropad
#   |- hit_rate
#   |- nonzero_percentile_thres
#   |- threshold

import numpy as np
from scipy.ndimage.filters import uniform_filter

def roll_zeropad(a, shift, axis=None):
    '''
    Shifts an array (a, TYPE:array) certain pixels (shift, TYPE:int) 
    along specified axis (axis=, TYPE:int, RANGE:[0,len(a.shape)]) 
    and pad with zeros after shifting.
    Returns: shifted and zeropadded a.
    '''
    a = np.asanyarray(a)
    if shift == 0: return a
    if axis is None:
        n = a.size
        reshape = True
    else:
        n = a.shape[axis]
        reshape = False
    if np.abs(shift) > n:
        res = np.zeros_like(a)
    elif shift < 0:
        shift += n
        zeros = np.zeros_like(a.take(np.arange(n-shift), axis))
        res = np.concatenate((a.take(np.arange(n-shift,n), axis), zeros), axis)
    else:
        zeros = np.zeros_like(a.take(np.arange(n-shift,n), axis))
        res = np.concatenate((zeros, a.take(np.arange(n-shift), axis)), axis)
    if reshape:
        return res.reshape(a.shape)
    else:
        return res

def shift(m, U, V):
    '''
    Shift m (2d array) with zonal (U, TYPE:float)
    and merional (V, TYPE:float) displacements in pixels.
    Dependencies: [roll_zeropad,]
    Return: shifted m. 
    Caution: If U or V is float, the detailed structure of m
    is not conserved after shifting.
    '''

    U = 1.*U
    V = 1.*V
    #if U >= 0:
    #    U_int = int(U)
    #else:
    #    U_int = int(U)-1
    #if V >= 0:
    #    V_int = int(V)
    #else:
    #    V_int = int(V)-1
    #U_deci = U-U_int
    #V_deci = V-V_int
    #a = (1-U_deci)*(1-V_deci)
    #b = U_deci*(1-V_deci)
    #c = (1-U_deci)*V_deci
    #d = U_deci*V_deci
    return roll_zeropad(roll_zeropad(m,int(V),0),int(U),1)
    #m_shift1 = (1-U_deci)*(1-V_deci)*roll_zeropad(roll_zeropad(m,V_int,0),U_int,1)
    #m_shift2 = U_deci*(1-V_deci)*roll_zeropad(roll_zeropad(m,V_int,0),U_int+1,1)
    #m_shift3 = (1-U_deci)*V_deci*roll_zeropad(roll_zeropad(m,V_int+1,0),U_int,1)
    #m_shift4 = U_deci*V_deci*roll_zeropad(roll_zeropad(m,V_int+1,0),U_int+1,1)
    #return m_shift1+m_shift2+m_shift3+m_shift4

def hit_rate(m, a, m_thres=0., a_thres=0.):
    '''
    Hit Rate = #hits/(#hits+#misses)
    threshold parameters: m_thres for m, a_thres for a
    '''    
    m_bin = np.asanyarray(m).copy()
    a_bin = np.asanyarray(a).copy()
    m_bin[np.where(m <= m_thres)] = 0
    m_bin[np.where(m_bin != 0)] = 1
    a_bin[np.where(a <= a_thres)] = 0
    a_bin[np.where(a_bin != 0)] = 1

    hit = len(np.where((m_bin==1)&(a_bin==1))[0])
    miss = len(np.where((m_bin==0)&(a_bin==1))[0])
    if len(np.where(a_bin>0)[0]) == 0:
        return 0
    else:
        return hit*1./(hit+miss)


def nonzero_percentile_thres(m, percent=95):
    m_copy = np.asanyarray(m).copy()
    M = m_copy[np.nonzero(m_copy)]
    return np.percentile(M,percent)

def threshold(m, thres=0.):
    m_copy = np.asanyarray(m).copy()
    m_copy[np.where(m_copy<thres)] = 0.
    return m_copy






