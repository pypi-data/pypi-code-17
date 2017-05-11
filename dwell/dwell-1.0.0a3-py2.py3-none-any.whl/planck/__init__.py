"""This module calculates the Planck function in various forms, usually between a lower and 
upper limit and for a single temperature. Two functions use weave.blitz code to 
speed up the functions.

"""

#planck module
import numpy as np
import dwell.constants as const


def planck_wavelength(wavelength, temp):
    """Calculate Black Body radiance at a single wavelength or wavelengths.
    
    :param wavelength: wavelengths, microns
    :type wavelength: numpy array

    :param temp: of temperatures, kelvin
    :type temp: numpy array, or float

    :returns: Planck function in units of W/m^2/ster/micron 
              calculated at wavelength and temperature
    :rtype: numpy array
    """
    
    metres_to_microns = 1.e6
    c1 = 2*const.h*const.c*const.c    * metres_to_microns**4     #1.911e8
    c2 = (const.h*const.c/const.k_B) * metres_to_microns     #1.439e4
    Blambda = c1 * (wavelength)**(-5)/(np.exp(c2/(wavelength*temp))-1)
    
    return Blambda

    
def planck_wavenumber(wavenumber, temp):
    """Calculate Black Body radiance at a given wavenumber or set of wavenumbers
    
    :param wavenumber: wavenumber, cm-1
    :type wavenumber: numpy array

    :param temp: of temperatures, kelvin
    :type temp: numpy array or float

    :returns: Planck function in units of W/m^2/ster/cm-1 
              calculated at wavelength and temperature
    :rtype: numpy array
    """
    
    metres_to_centimetres = 1e2
    
    c1 = 2*const.h*const.c*const.c * metres_to_centimetres**4 #1.e-8
    c2 = const.h*const.c/(const.k_B) * metres_to_centimetres # 1.439
    
    Bnu = c1 * (wavenumber**3) / (np.exp(wavenumber*c2/temp) - 1)
    
    return Bnu

def cfst4_wavenumber(wl, wh, *args, **kwargs):
    """Calculate the integrated Planck function between two wavenumbers
    
    :param wl: low wavenumber, cm-1
    :type wl: numpy array
    
    :param wh: high wavenumber, cm-1
    :type wh: numpy array

    :param temp: of temperatures, kelvin
    :type temp: float

    :returns: Planck function in units of W/m^2/ster
              at temperature integrated between wl and wh
    :rtype: numpy array
    """
    return cfst4_wavelength(10000./wh,10000./wl, *args, **kwargs)

def cfst4_wavelength(wl, wh, temperature, diff_planck=None, diff_planck_2=None):
    """Calculate the integrated Planck function between two wavelengths
    
    :param wl: low wavelength, micron
    :type wl: numpy array
    
    :param wh: high wavelength, micron
    :type wh: numpy array

    :param temp: of temperatures, kelvin
    :type temp: float

    :returns: Planck function in units of W/m^2/ster
              at temperature integrated between wl and wh
    :rtype: numpy array

    """
    c=0.153989733
    c2 = 1.43883e4
    sigma = const.sigma
    
    wn = [wl,wh]
    fac = 0.0000001
    f=[0.0,0.0]
    for i in range(2):
        f[i]=0.0
        v = c2/(wn[i]*temperature)
        for m in range(1,1000):
            wv=float(m)*v
            ff=(float(m)**(-4))*(np.exp(-wv))*(((wv+3.0)*wv+6.0)*wv+6.0)
            f[i]=f[i]+ff
            if f[i] == 0.0:
                continue
            if ff/f[i] <= fac :
                break
            pass
        pass
    fst4 = c*(f[1]-f[0])*sigma*temperature**4
        
    
    return fst4

def cfst4_wavelength_weave(wl, wh, temperature, diff_planck=None, diff_planck_2=None):
    """Calculate the integrated Planck function between two wavenumbers. Uses 
    blitz.weave code to speed up the calculation.
    
    :param wl: low wavelength, micron
    :type wl: numpy array
    
    :param wh: high wavelength, micron
    :type wh: numpy array

    :param temp: of temperatures, kelvin
    :type temp: float

    :returns: Planck function in units of W/m^2/ster
              at temperature integrated between wl and wh
    :rtype: numpy array
    """
    c=0.153989733
    c2 = 1.43883e4
    sigma = const.sigma
    
    wn = np.array([wl,wh])
    fac = 0.0000001
    f=np.array([0.0,0.0])
    code="""
    double v,ff,wv,fst4;
    for (int i=0;i<2;i++){
        f(i)=0.0;
        v = c2/(wn(i)*temperature);
        ff=1e6;
        for (int m=1;m<1000;m++){
            wv=m*v;
            ff=(exp(-4.0*log(m)))*(exp(-wv))*(((wv+3.0)*wv+6.0)*wv+6.0);
            f(i)=f(i)+ff;
            if (f(i) == 0.0)  continue;
            if (ff/f(i) <= fac) break;
      }
      }

    fst4 = c*(f(1)-f(0))*sigma*exp(4*log(temperature));
    return_val = fst4;
    """
    from scipy.weave import converters
    import scipy.weave as weave
    err = weave.inline(code,['f','temperature', 'wn', 'fac','sigma','c','c2'],
                       type_converters=converters.blitz,compiler='gcc')
    
    return err

def cfst4_wavelength_weave_loop(wl, wh, temperature, diff_planck=None, diff_planck_2=None):
    """Calculate the integrated Planck function between two wavelengths. Uses 
    blitz.weave code to speed up the calculation
    :param wl: low wavelength, micron
    :type wl: numpy array
    
    :param wh: high wavelength, micron
    :type wh: numpy array

    :param temp: of temperatures, kelvin
    :type temp: float

    :returns: Planck function in units of W/m^2/ster
              at temperature integrated between wl and wh
    :rtype: numpy array

     
    """
    c=0.153989733
    c2 = 1.43883e4
    sigma = const.sigma
    
    wn = np.array([wl,wh])
    fac = 0.0000001
    f=np.array([0.0,0.0])
    len_t = temperature.size
    res=np.zeros(len_t, d_type=temperature.d_type)
    code="""
    double v,ff,wv,fst4;
    for(int l=0;l<len_t;l++){
    for (int i=0;i<2;i++){
        f(i)=0.0;
        v = c2/(wn(i)*temperature[l]);
        ff=1e6;
        for (int m=1;m<1000;m++){
            wv=m*v;
            ff=(exp(-4.0*log(m)))*(exp(-wv))*(((wv+3.0)*wv+6.0)*wv+6.0);
            f(i)=f(i)+ff;
            if (f(i) == 0.0)  continue;
            if (ff/f(i) <= fac) break;
      }
      }
    fst4 = c*(f(1)-f(0))*sigma*exp(4*log(temperature[i]));
    res[i]=fst4      
      }
      
    return_val = fst4;
    """
    from scipy.weave import converters
    import scipy.weave as weave
    err = weave.inline(code,['f','temperature', 'wn', 'fac','sigma','c','c2'],
                       type_converters=converters.blitz,compiler='gcc')
    
    return res


def st4(temp):
    """Calculates the integrated Black body function from zero to infinity,
    (wavenumber or wavelength),   sigma*temp^4.
    
    :param temp: temperature, K
    :type temp: numpy array, or float

    :returns: Planck function in units of W/m^2
              at temperature
    :rtype: same as input
    """
    
    bb = const.sigma * temp**4
    return bb

if __name__=="__main__":
    import dwell.testing.test_planck as pp
    c = pp.test_planck()
    c.allt()
