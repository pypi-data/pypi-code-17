"""Interal fft code. Interfaces to anfft, numpy.fft or scipy.fft for use by fft"""

import numpy
got_fft_library=False
using_fft_library=None
#Try to get an FFT library in order of anfft, scipy.fftpack, numpy.fft
#we require numpy for everything else, so the last check shouldn't fail?

if not got_fft_library:
    try:
        import anfft as fft
        got_fft_library = True
        using_fft_library="anfft"
    except ImportError:
        got_fft_library = False

if not got_fft_library:
    try:
        import scipy
        import scipy.fftpack as fft
        got_fft_library = True
        using_fft_library="scipy"
    except ImportError:
        got_fft_library = False

if not got_fft_library:
    try:
        import numpy.fft as fft
        got_fft_library = True
        using_fft_library="numpy"
    except ImportError:
        got_fft_library = False

if not got_fft_library:
    raise ImportError("Error: Cannot use fft libraries")        

import numpy.fft as npfft

fftshift = npfft.fftshift
def fft_ifftn(*args, **kwargs):
    """Call the core fft library function ifftn (inverse)
    
    If the anfft library is used, enable 'measure' optimization.
    
    """
    if using_fft_library=="anfft":
        return fft.ifftn(*args, measure=True, **kwargs)
    else:
        return fft.ifftn(*args, **kwargs)

def fft_fftn(*args, **kwargs):
    """Call the core fft library function fftn.
    
    If the anfft library is used, enable 'measure' optimization.
    
    """
    
    if using_fft_library=="anfft":
        return fft.fftn(*args, measure=True, **kwargs)
    else:
        return fft.fftn(*args, **kwargs)
    
def odd(n):
    """Returns true if the input is odd
    
    :param n: number to test
    :type n: integer
    
    :return: logical if input is odd or not
    :rtype: Boolean
    
    """
    if n % 2 == 1:
        return True
    else:
        return False


def rffttruncate(ft, axis):
    """Truncates the FFTd data along the particular axis
    
    :param ft: multiple dimension array with at least one dimension FFT'd
    :type ft: numpy array

    :param axis: axis to truncate
    :type axis: list

    :return: Truncated data
    :rtype: numpy array

    This function shifts (rolls) the data along the correct axis, calculates a slice range
    which is either (N-1)/2 or N/2-1.
    
    """
    ft2 = numpy.roll(ft, -1,axis)
    d=[]
    for i in range(ft.ndim):
        d.append(slice(None,None,None))

    n=ft2.shape[axis]
    if odd(n):
        x = (n-1)/2
    else:
        x=n/2-1
    d[axis]=slice(-1,x-1,-1)
    return ft2[d]

def ffttruncate(ft, axis):
    """Truncates the FFTd data along the particular axis
    
    :param ft: multiple dimension array with at least one dimension FFT'd
    :type ft: numpy array
    
    :param axis: axis to truncate
    :type axis: list
    
    :return: Truncated data
    :rtype: numpy array
    
    This function shifts (rolls) the data along the correct axis, calculates a slice range
    which is either (N-1)/2 or N/2-1.
    
    """
    d=[]
    for i in range(ft.ndim):
        d.append(slice(None,None,None))

    n=ft.shape[axis]
    x = (n+1)/2
    d[axis]=slice(None,x,None)
    return ft[d]

def fftshift(ft, axis):
    """Calls the fftshift core function, which shifts the ft half way along the axis
    :param ft: array to be shifted
    :type ft: numpy array
    
    :param axis: axis to shift over
    :type axis: integer
    
    :return: shifted array
    :rtype: numpy array
    
    This function is only available in numpy
    
    """
    return npfft.fftshift(ft,axis)


def fft_axes(ft, d1, d2, axis):
    """Uses numpy to generate the axes because on step size and length
    
    :param ft: Input fft'd data, used only for the dimension data
    :type ft: numpy array
    :param d1: dimension 1 step size
    :type d1: float
    :param d1: dimension 2 step size
    :type d2: float
    :param axis: axis indexes of dimensions
    :type axis: list
    
    :return: tuple of axes values
    :rtype: tuple of integers
    """
    n=ft.shape[axis[0]]
    f1 = npfft.fftfreq(n, d1)
    n=ft.shape[axis[1]]
    f2 = npfft.fftfreq(n, d2)

    return (f1, f2)


def trans_array(data, _axes):
    """Calculates indices for an array transpose use by anFFT.
    
    :param data: The data, used for dimension purposes (rank)
    :type data: numpy array
    :param _axes: axes to FFT over, and hence transpose to the end
    :type _axes: list
    :return: tuple of axes values
    :rtype: tuple of integers
    
    """
    ind = list(range(data.ndim))
    try:
        axes = list(_axes)
    except: #integer
        axes=[_axes]
    axes.sort()
    axes.reverse()
    for a in axes:
        ind.pop(a)
    ind.extend(axes)
    return ind

def rtrans_array(data, _axes):
    """Calculates the indices to reverse the transpose of an array after anFFT.
    
    :param data: The data, used for dimension purposes (rank)
    :type data: numpy array
    
    :param _axes: axes to FFT over, and hence transpose to the end
    :type _axes: list
    
    :return: tuple of axes values
    :rtype: tuple of integers
    """
    ind = trans_array(data, _axes)
    rind=list(ind)
    for i,j in enumerate(ind):
        rind[j]=i
    return rind

def trans_forward(data, _axes):
    """Transpose an array to the correct order for anfft
    
    :param data: The data to be transposed
    :type data: numpy array
    
    :param _axes: axes to FFT, and hence transpose
    :type _axes: list
    
    :return: The transposed array
    :rtype: numpy array
    """
    ind = trans_array(data, _axes)
    #ind now contains the transposed dimensions
    return numpy.transpose(data, ind)
    
def trans_backward(data, _axes):
    """Reverse the transpose of an array to the correct order for anfft
    
    :param data: The data to transpose
    :type data: numpy array
    
    :param _axes: The axes over which to FFT, and transpose if anfft is used
    :type _axes: list
    
    :param function: ifft function, or fft function if overridden
    :type function: function pointer
    
    :return: The transposed array
    :rtype: numpy array
       """
    ind = trans_array(data, _axes)
    ind2=list(ind)
    for d in ind:
        ind2[d]=ind.index(d)
    #ind now contains the reverse transposed dimensions
    return numpy.transpose(data, ind2)

    
def ifftn(data,axes=None, function=None):
    """Runs the inverse FFT function over multiple axes
    
    :param data: The data to transpose
    :type data: numpy array
    
    :param axes: The axes over which to FFT, and transpose if anfft is used
    :type axes: numpy array

    :param function: ifft function, or fft function if overridden
    :type function: function pointer

    :return: An FFTd array 
    :rtype: numpy array
    
    """
    if function is None:
        function =fft_ifftn
        
    if axes is None:
        return function(data)
    else:
        if using_fft_library == "anfft":
            #transpose the array so that the fft dims are all at the end
            data = trans_forward(data, axes)
            #fft
            if type(axes) is list:
                k = len(axes)
            elif type(axes) is numpy.ndarray:
                k = axes.size
            elif type(axes) is int:
                k=1
            ft = function(data, k)
            #transpose back
            data = trans_backward(data, axes)
            ft = trans_backward(ft, axes)
            
            pass
        elif using_fft_library == "scipy":
            ft = function(data, axes=axes)
            pass
        elif using_fft_library == "numpy":
            ft = function(data, axes=axes)
            pass
        else:
            print("Error: Can't get here")

        return ft

def fftn(data,axes=None):
    """Runs the inverse FFT function over multiple axes
    
    :param data: The data to transpose
    :type data: numpy array

    :param axes: The axes over which to FFT, and transpose if anfft is used
    :type axes: numpy array

    :param function: ifft function, or fft function if overridden
    :type function: function
    
    :return: An FFTd array 
    :rtype: numpy array
    """
    return ifftn(data, axes, fft_fftn)

    

