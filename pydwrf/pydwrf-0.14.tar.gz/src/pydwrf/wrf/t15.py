from .wrf_exception import *
from netCDF4 import Dataset
import numpy as np

#Pressure grid for the interpolation
pw = np.exp(((1+np.arange(62))/10.)-4.6)

#Weighting function for the brightness temperature calculation
wtfcn = np.array([.03500,.03500,.03600,.03600,.03700,.03700,.03800,.03900,\
                   .04100,.04300,.04600,.04900,.05200,.05600,.06000,.06500,\
                   .07000,.07600,.08200,.09000,.09700,.10500,.11500,.12500,\
                   .13600,.14700,.15900,.17200,.18600,.20100,.21700,.23400,\
                   .25200,.27000,.28800,.30800,.32600,.34300,.36000,.37200,\
                   .38200,.38800,.39100,.38800,.37900,.36400,.34200,.31000,\
                   .27800,.24600,.21300,.17800,.14300,.10900,.08100,.06100,\
                   .04500,.03200,.02200,.01500,.01000,.00700])

wtfcn = np.reshape(wtfcn,(62, wtfcn.size/62))

def t15data():
    """Returns T15 data based on Claire Newman's interpolation of Basu 2002 paper"""
    ls =np.arange(73)*5.
    t = np.array([175.6,173.8,172.6,171.4,170.2,169.1,168.1,167.2,\
             166.4,165.8,165.8,166.,166.2,166.5,166.8,167.1,\
             167.4,167.7,168.,168.65,169.3,169.95,170.6,\
             171.3,172.,172.7,173.4,174.15,174.9,175.7,176.5,\
             177.25,178.,178.7,179.4,180.,180.8,181.6,182.4,\
             183.2,184.,184.8,185.6,186.4,187.2,188.05,188.9,\
             189.8,190.7,191.35,191.95,191.75,191.15,190.55,\
             190.,189.3,188.6,187.9,187.2,186.5,185.8,185.15,\
             184.55,184.,183.4,182.8,182.15,181.4,180.6,179.4,\
             178.6,177.6,175.8])
    return ls, t

try:
    #Try importing Just-In-Time (jit) compiler from numba
    from numba import jit
    @jit
    def interp(p,t,pw):
        """Using jit compiler to run faster interpolation"""
        j=0
        tw=np.zeros(pw.size)
        for i in np.arange(pw.size):
            if pw[i] < p[0]:
                tw[i] = t[0]
            elif pw[i] >= p[-1]:
                tw[i] = t[-1]
            else:
                while(p[j+1]<pw[i]):
                    j=j+1
                k2=j+1
                k1=j
                tw[i] = ((p[k2]-pw[i])*t[k1] + (pw[i]-p[k1])*t[k2]) / (p[k2]-p[k1])
        return tw
except:

    def interp(p,t,pw):
        """Interpolate temperature in pressure."""
        j=0
        tw=np.zeros(pw.size)
        for i in np.arange(pw.size):
            if pw[i] < p[0]:
                tw[i] = t[0]
            elif pw[i] >= p[-1]:
                tw[i] = t[-1]
            else:
                while(p[j+1]<pw[i]):
                    j=j+1
                k2=j+1
                k1=j
                tw[i] = ((p[k2]-pw[i])*t[k1] + (pw[i]-p[k1])*t[k2]) / (p[k2]-p[k1])
        return tw

def t15_core(press,temp,area):
    """Calculate area weighted mean brightness temperature at 15 microns
        First interpolate temperature profile to pressure values, then use 
        weighting function to calculate brightness temperature.
    """
    #area weighted mean temperature
    mean_temp = np.average(np.average(temp*area[None,:,:], axis=1),axis=0) / np.average(area)
    y=0
    tb15av=0.
    arav =0.
    f=None
    tw=np.zeros(pw.shape)
    for i in np.arange(temp.shape[1]):
        for j in np.arange(temp.shape[2]):     
            t,p=temp[::-1,i,j],press[::-1,i,j]*0.01 #reversed
            tw = interp(p,t,pw)
            rad = (-.0181075-39.4312/( tw-2353.76-62644./(tw+64.445+84263.9/(tw-185.333)) ))
            
            radsum = sum(rad*wtfcn[:,y])
            sumwt = sum(wtfcn[:,y])
            xx=radsum/sumwt
            
            tb15=881.042-2.40183/( xx+.00364298-.61044E-7/(xx+.162965E-3-.113959E-8/(xx+.228812E-4)) )
            tb15av = tb15av + tb15*area[i,j]
            arav =arav+area[i,j]
    return tb15av/arav

def process_file(filename,rows=None):
    """Process a file. Extract variables from the netCDF file, calculate the temperature from potential temperature.
    Then pass T,P into the t15_core function to calculate T15 values.
    """
    nc = Dataset(filename)
    xlat = nc.variables["XLAT"][0,:,:]
    xlong = nc.variables["XLONG"][0,:,:]
    xlong_u = nc.variables["XLONG_U"][0,:,:]
    xlat_v = nc.variables["XLAT_V"][0,:,:]
    dlat = np.diff(xlat_v,axis=0)
    dlong = np.diff(xlong_u,axis=1)

    radius = nc.RADIUS
    area = radius*radius*(1./72) * 2*np.pi * (np.sin(np.deg2rad(xlat_v[1:])) - np.sin(np.deg2rad(xlat_v[:-1])))

    g = nc.G
    omega = nc.EOMEG
    cp = nc.CP
    rd = nc.R_D
    kappa =rd/cp
    t0 = nc.T0
    p0 = nc.P0
    
    lat = xlat[:,0]

    l_s, P, PB, T = [nc.variables[x] for x in ["L_S", "P", "PB","T"]]
    latsel = np.where((xlat[:,0] >= -40.)&(xlat[:,0]<40))[0]
    latsel=slice(latsel[0],latsel[-1],1)
    tvals=[]
    rows = rows or slice(None)
    rows = np.arange(T.shape[0])[rows].astype(int)
    for i in rows:
        press = (P[i,:,latsel] + PB[i,:,latsel])
        theta = T[i,:,latsel]+t0
        temp = (press/p0)**kappa * theta
        t15_values = t15_core(press, temp,area[latsel])
        tvals.append(t15_values)
    data= dict(ls=l_s[rows], t15=np.array(tvals))
    data["times"]=["".join(s) for s in nc.variables["Times"][:]]
    return data
