"""FFT interface fo' science"""

try:
    import cdms2
    use_cdms2 = True
except:
    use_cdms2 = False
    
from ._internal import *

import numpy

def spec1d(data, d1, use_axes=0):
    """Calculate the 1 dimensional FFT and return a truncated array
    
    :param data: 1-dimensional array of data to FFT
    :type data: numpy array

    :param d1: : step size of the data, used to calculate axes data
    :type d1: float
    
    :return: Amplitude, calculated as the absolute magnitude of the complex FFT
    :return: phase, calculate as atan(imag(ft)/real(ft))
    :return: x axis values
    :rtype: tuple of (numpy 1d, numpy 1d, numpy 1d)
    """
    internal_use_axes =list([use_axes])
    ft = ifftn(data, internal_use_axes)
    n=ft.shape[internal_use_axes[0]]
    f1 = npfft.fftfreq(n, d1)
    f1 = abs(rffttruncate(f1,0))
    ft = rffttruncate(ft,internal_use_axes[0])
    #double amplitude and correct 0,0
    ft=ft*2.0
    ft[0]=ft[0]*0.5

    amp = numpy.abs(ft)
    pha = numpy.arctan2(numpy.imag(ft), numpy.real(ft))
    return (amp, pha, f1)
    
    
def axis_or_axes(data, axis=None, axes=None,*args, **kwargs):
    """Return either axes, axis or the indices of the last two dimensions
    
    :param axis: indices to use in the fft
    :type axis: list
    
    :param axes: alternative naming
    :type axes: list
    
    :return: axis is returned if defined, otherwise axes is defined
             otherwise the data rank is found, and the last two 
             dimensions are returned as indices
    :rtype: list
    """
    r = list(axis or axes or [data.ndim-2, data.ndim-1])
    return r

  

def truncate_fft(ft, d1, d2, use_axes, atmosphere=None, ocean=None):
    """Truncates a Complex 2d FFT plane to half the size in one dimension, removing negative exponents
    
    Given a 2-D NxM complex fft data, and step sizes along each, calculate the axis values 
    based on the step sizes, then truncate the 2D plane and axes to the right shape based on flags
    
    :param ft: 2D FFT'd data
    :type ft: numpy array
    
    :param d1: dimension along the X axis
    :type d1: float
    
    :param d2: dimension along the Y axis
    :type d2: float
    
    :param use_axis: two element axes list describing which axes are being used in the FFT, other axes are simply looped over
    :type use_axis: logical
    
    :param atmosphere: bool to decide to use 'atmosphere' truncation (f1 positive definite)
    :type atmosphere: logical

    :param ocean: bool to decide to use 'ocean' truncation (f2 positive definite)
    :type ocean: logical
    
    :return: tuple of complex truncated fft, axes1, axes2
    :rtype: 2d numpy, 1d numpy, 1d numpy
    """
    ao = False
    if atmosphere is not None:
        ao=True
    elif ocean is not None:
        ao=not ocean

    (f1, f2) = fft_axes(ft, d1, d2, use_axes)
    if ao: 
        #atmosphere
        #for atmosphere, wave (d1,f1) is positive definite
        #which means freq (d2,f2) can be negative

        f1 = -rffttruncate(f1, 0)
        ft = rffttruncate(ft,use_axes[0])
        #double amplitude and correct 0,0
        ft=ft*2.0
        ft[0,0]=ft[0,0]*0.5
        f2 = fftshift(f2, 0)
        ft = fftshift(ft,use_axes[1])
        
        pass
    else:
        #ocean

        f2 = -rffttruncate(f2,0)
        ft = rffttruncate(ft,use_axes[1])
        ft=ft*2.0
        ft[0,0]=ft[0,0]*0.5
        f1 = fftshift(f1, 0)
        ft = fftshift(ft, use_axes[0])
        pass

    return (ft, f1, f2)


def fft_core(field1, field2=None, use_axes=None):
    """Call the FFT core interface given data and axes to transform over
    
    :param field1: dataset 1, must contain at least the axes listed in use_axes
    :type field1: 2d numpy
    
    :param field2: optional extra field to be transformed. If field2 is not None, then the cospectrum of
                   field1 and field2 are calculated, as fft(field1)*conj(fft(field2))
    :type field2: 2d numpy
    
    :param use_axes: axes over which to FFT.
    :type use_axes: list

    :return: The fft'd field, or the cospectrum field
    :rtype: 2d numpy array
    """
    ft = ifftn(field1, use_axes)
#cospectrum optional
    if field2 is not None:
        ft2 = ifftn(field2, use_axes)
        ft = ft*numpy.conj(ft2)

    return ft

def spec(_data, d1, d2, *args, **kwargs):
    """Interface to spec_cdms or spec_numpy to wrap the result appropriately"""
    if use_cdms2:
        if isinstance(_data, cdms2.tvariable.TransientVariable):
            return spec_cdms2(_data,d1,d2,*args, **kwargs)
        elif isinstance(_data, numpy.ndarray):
            return spec_numpy(_data,d1,d2,*args, **kwargs)
    else:
        if isinstance(_data, numpy.ndarray):
            return spec_numpy(_data,d1,d2,*args, **kwargs)
    
def spec_cdms2(_data, d1, d2, *args, **kwargs):
    """Calls the fft spec_numpy function, then wraps the output
    in cdms variables to return a pretty object to the user."""
    
#cdms variable
    #break the variable into data and axes
    (amp,pha,freq,wave) = spec_numpy(_data.data,d1,d2,*args,**kwargs)

    #reconstruct two transient variables 
    _data=0.0
    amp_var = cdms2.tvariable.TransientVariable(amp)
    amp=0.0
    pha_var = cdms2.tvariable.TransientVariable(pha)
    pha=0.0
    wave_var = cdms2.tvariable.TransientVariable(wave)
    freq_var = cdms2.tvariable.TransientVariable(freq)
    #find out which axes are being used
    use_axis = axis_or_axes(_data,*args, **kwargs)
    not_fft_axes = set(numpy.arange(_data.ndim)).difference(set(use_axis))

    for a in not_fft_axes:
        amp_var.setAxis(a,_data.getAxis(a))
        pha_var.setAxis(a,_data.getAxis(a))

    #add axes
    wave_axis = cdms2.axis.TransientAxis(wave,id="wavenumber")
    freq_axis = cdms2.axis.TransientAxis(freq,id="frequency")
    for v in [amp_var,pha_var]:
        v.setAxis(use_axis[0], freq_axis)
        v.setAxis(use_axis[1], wave_axis)
    
    freq_var.setAxis(0, freq_axis)
    wave_var.setAxis(0, wave_axis)
    
    return (amp_var, pha_var, wave_var, freq_var)


def spec_numpy(_data, d1, d2,
              axis=None, axes=None,
              detrend=None, perturb=None,
              atmosphere=None, ocean=None, field2=None
              ):
    """Routine transforms a real field to frequency/zonal wavenumber space
    Positive k are eastward propagating
    Negative k are westward propagating
    frequency is always positive
    
    Phase has been defined as im(wave)/re(wave)
    wave = exp(i(k.lon - w.t + phi))
    and c_phase = w/k, w=s.Omega, s = freq = 1./(period/days)
    t + lon/omega is the local time at longitude lon
    for this convection local time of first max. = phi/w
    longitude of first max.  = -phi/k
    
    :param _data: The data to transform
    :type _data: 2d numpy
    
    :param d1: axis 1 step size
    :type d1: float
    
    :param d2: axis 2 step size
    :type d2: float
    
    :param axes: axis over which to fft
    :type axes: list
    
    :param axis: alternate name for axes
    :type axis: list
    
    :param detrend: boolean to determine whether the data is first detrended over some axis NOT USED
    :type detrend: logical
    
    :param perturb: boolean to determine whether the data is first detrended over the other axis NOT USED
    :type perturb: logical
    
    :param atmosphere: booleans to determine the axis to truncate
    :type atmosphere: logical

    :param ocean: booleans to determine the axis to truncate
    :type ocean: logical
    
    :param field2: optional argument to flag a cospectrum calculation.
    :type field2: float
    """

    data = _data
    #which axes?
    use_axes = axis_or_axes(data,axis,axes)
    #calculate the fft over n dimensions
    ft = fft_core(data, field2=field2, use_axes=use_axes)
    #calculate axis and truncate    
    ft,f1,f2 = truncate_fft(ft, d1, d2, use_axes, atmosphere, ocean)

    if field2 is None:
        #amplitude spec
        amp = numpy.abs(ft)
        pha = numpy.arctan2(numpy.imag(ft),numpy.real(ft))
        return (amp,pha,f1, f2)
    else :
        #cospectrum
        cospec = numpy.real(ft)
        quad = numpy.imag(ft)
        return (cospec,quad,f1, f2)

def cospec(_data, field2, d1, d2,
            axis=None, axes=None,
            detrend=None, perturb=None,
            atmosphere=None, ocean=None
            ):
    """Calculates the cospectrum as fft(_data)*conj(fft(field2))
    
    :param _data: first field
    :type _data: 2D numpy array

    :param field2: second field
    :type field2: 2D numpy array
    
    :param d1: axis 1 step size
    :type d1: float
    :param d2: axis 2 step size
    :type d2: float
    
    :param axes: axis over which to fft
    :param axis: alternate name for axes
    :param detrend: boolean to determine whether the data is first detrended over some axis NOT USED
    :param perturb: boolean to determine whether the data is first detrended over the other axis NOT USED
    :param atmosphere,ocean: booleans to determine the axis to truncate.
    """
    return spec(_data, d1, d2,
    axis=axis, axes=axes,
    detrend=detrend, perturb=perturb,
    atmosphere=atmosphere, ocean=ocean, field2=field2
    )
