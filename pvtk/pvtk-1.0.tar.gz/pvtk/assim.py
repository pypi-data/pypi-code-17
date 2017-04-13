#|- Funtions List in [.assim]:
#   |- assim
#      |- threshold in [.basics]



import numpy as np
from scipy.stats import pearsonr
from .basics import threshold


def assim(m, a, i=1./3, j=1./3, k=1./3, m_thres=0., a_thres=0.):
    m_copy = threshold(m,thres=m_thres)
    a_copy = threshold(a,thres=a_thres)
    if m_copy.mean() == 0 and a_copy.mean() == 0:
        AMP = 1.
        VAR = 1.
        STR = 1.
    elif m_copy.std() == 0 and a_copy.std() == 0:
        AMP = 2.*m_copy.mean()*a_copy.mean()/(m_copy.mean()**2+a_copy.mean()**2)
        VAR = 1.
        STR = 1.
    else:
        AMP = 2.*m_copy.mean()*a_copy.mean()/(m_copy.mean()**2+a_copy.mean()**2)
        VAR = 2.*m_copy.std()*a_copy.std()/(m_copy.std()**2+a_copy.std()**2)
        STR = pearsonr(m_copy.reshape(-1),a_copy.reshape(-1))[0]
    if STR < 0:
        STR = 0.
    return (AMP**i)*(VAR**j)*(STR**k)

