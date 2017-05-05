from .wrf_exception import *
from scipy.special import gamma
from numpy import pi
import numpy as np

def masknans(data):
    """Mask variables based on presence of nan values in the data"""
    return np.ma.array(data,mask=np.isnan(data))

def maskval(data,maskval):
    """Mask values looking for a particular value in the data (e.g. 0)"""
    return np.ma.array(data,mask=data==maskval)

#default parameters
#mu=7 -> veff=0.1, rhodust=2.5e3, rhoice=1e3
rcParams=dict(mu=1./0.1 - 3, rhodust=2.5e3,rhoice=1e3, rho=2.5e3)

def loadParams(kwargs,only=None):
    """Return the parameters requested in 'only' list or all keywords after updating 
        with kwargs."""
    res=dict(rcParams)
    res.update(kwargs)
    if only is None:
        return res

    res2=[res[k] for k in only]
    return res2

def lam(mass,number, **kwargs):
    """Calculate lambda from mass and number """
    mu,rho = loadParams(kwargs,only=["mu","rho"])
    num = pi * rho * number * gamma(mu+4)
    denom = 6 * mass * gamma(mu+1)

    num = np.ma.array(num,mask=num<0)
    denom = np.ma.array(denom,mask=denom<=0)

    lamval = (num/denom)**(1./3)
    return lamval

def reff(mass,number,**kwargs):
    """Calculate effective radius based on input mass and number"""
    mu, = loadParams(kwargs,only=["mu"])
    lamval = lam(mass,number, **kwargs)
    lamval = np.ma.array(lamval,mask=lamval==0)
    reffval = gamma(mu+4) / (2*lamval*gamma(mu+3))
    return reffval

def veff(mass,number,**kwargs):
    """Calculate effective variance given a mu value. 
    Takes mass and number but doesn't use them."""
    mu, = loadParams(kwargs,only="mu")
    veffval = 1./(kwargs["mu"]+3)
    return veffval
