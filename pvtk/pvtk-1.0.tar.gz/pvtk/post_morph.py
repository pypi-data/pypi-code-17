import numpy as np
from .basics import shift
from .assim import assim

def morph_test(m,a,u,v,assim0=0.8):
    D = assim(shift(m,u,v),a)
    return D > assim0


