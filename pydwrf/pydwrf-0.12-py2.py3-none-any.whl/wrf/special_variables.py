from .wrf_exception import *
from . import nc
from . import twomoment

#special variable for temperature
def temperature(infh,indices=None, return_pressure=False,return_dimensions=False):
    """Calculate temperature from a netCDF file, either given a filehandle or filename.
        Try to allow for some indexing in "indices" variable.
    """
    fh = nc.open_if_file(infh)
    indices = nc.sanitize_indices(indices)

    t0,rd,cp = fh.T0, fh.R_D, fh.CP
    theta = fh.variables["T"][indices]+t0
    press = pressure(fh, indices)
    exner = press/fh.P0
    kappa = rd/cp
    temp = theta*(exner**kappa)
    if return_pressure:
        temp= temp, press
    if return_dimensions:
        temp=temp,fh.variables["T"].dimensions
    return temp

#special variable for pressure
def pressure(infh,indices=None,return_dimensions=False):
    """Calculate pressure from filename assuming P and PB are in the file"""
    fh = nc.open_if_file(infh)
    indices = nc.sanitize_indices(indices)

    press = (fh.variables["P"][indices] + fh.variables["PB"][indices])
    if return_dimensions:
        press=press,fh.variables["P"].dimensions
    return press

#special variable for two moment dust effective radius
def reffdust(infh, indices=None,return_dimensions=False):
    """Calculate effective radius by passing TRC01 and TRC02 into the twomoment reff calculation"""
    fh = nc.open_if_file(infh)
    indices = nc.sanitize_indices(indices)
    mass = fh.variables["TRC01"][indices]
    number = fh.variables["TRC02"][indices]
    reffval = twomoment.reff(mass,number)
    if return_dimensions:
        reffval=reffval,fh.variables["TRC01"].dimensions
    return reffval

#special variable for ice effective radius
def reffice(infh, indices=None,return_dimensions=False):
    """Calculate effective radius by passing TRC01 and TRC02 into the twomoment reffice calculation"""
    
    fh = nc.open_if_file(infh)
    indices = nc.sanitize_indices(indices)
    mass_core,mass_ice = fh.variables["TRC_IC"][indices], fh.variables["QICE"][indices]
    rhodust,rhoice=twomoment.rcParams["rhodust"],twomoment.rcParams["rhoice"]
    number = fh.variables["QNICE"][indices]
    mass = mass_core + mass_ice
    density = (mass_core*rhodust + mass_ice*rhoice)/mass
    reffval = twomoment.reff(mass,number,rho=density)
    if return_dimensions:
        reffice=reffice,fh.variables["TRC_IC"].dimensions
    return reffice
