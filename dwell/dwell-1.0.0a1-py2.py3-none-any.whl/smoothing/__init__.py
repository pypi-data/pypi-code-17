import numpy


def smooth(data, weights, return_weights=False, allow_edge_effects=False):
    """Smooths 1-dimensional data using numpy.convolve based on the weights
    
    :param data: The input array
    :type data: numpy array
    
    :param weights:   The weights array, length M (not dependent on N)
    :type weights: numpy array
    
    :param return_weights: whether to include the weights and the output in a tuple
    :type return_weights: logical
    
    :return: A smoothed array of length N, possibly in a tuple with the weights
    :rtype: numpy array
    """
    result = numpy.convolve(data, weights, 'same')
    if not allow_edge_effects:
        #edge correct
        try:
            lw = len(weights)
        except:
           lw = weights.size 
        nw = (lw-1)/2
        s_start = slice(0,lw,1)
        s_end = slice(-lw,None,1)
        result[0:lw] = data[0:lw]
        result[-lw:] = data[-lw:]
    
    if return_weights is not None:
        if return_weights:
            return (result, weights)
        
    return result    

def oddbox(funcname, boxsize, quiet=False, *args, **kwargs):
    """Ensure that the boxsize for smoothing is centered
    
    Makes a smoothing box/window be 2M+1 long to put the result in the centre box
    
    :param funcname: Function name, just for the message 
    :type funcname: string
    
    :param boxsize: 2M|2M+1 that is corrected to be 2M+1
    :type boxsize: integer
    
    :param quiet: Determines if the warning is NOT printed, default is false.
    :type quiet: logical
    
    :return: Odd number.
    :rtype: integer
    """
    if boxsize % 2 == 0 and not quiet:
        print("""boxsize should be odd ({0} smoothing),
currently {1}""".format(funcname, boxsize))
        boxsize+=1

    return boxsize

def scipy_window_smooth(data, boxsize=9,window_name='triangle',options=None, *args, **kwargs):
    """
    Use a scipy defined window to smooth. Options include 
    'triangle','boxcar','gaussian','blackman','parzen','hamming'.
    
    All but the 'gaussian' option takes a single option of the window size. 'gaussian'
    also takes the width.
    
    :param data: The input array
    :type data: numpy array
    
    :param boxsize:  total width of the smoothing window
    :type boxsize: integer
    
    :param window_name: scipy defined name of the smoothing function
    
    :return: Results from smooth, which is either the smoothed data, or 
      smoothed data and weights used in the smooothing
    :rtype: numpy array
    """
    
    import scipy.signal
    if window_name == 'gaussian':
        input = (window_name, options)
    else:
        input = window_name
    
    weights = scipy.signal.get_window(input, boxsize)
    weights = weights / numpy.sum(weights)
    return smooth(data, weights, *args, **kwargs)
    
def box(data, boxsize=9, *args, **kwargs):
    """Smoothing with a uniform distribution
    
    Generates an array of length N filled with values of 1/N, then calls smooth with this window
    
    :param data: The input array
    :type data: numpy array
    
    :param boxsize:  total width of the smoothing window
    :type boxsize: integer
    
    :return: Results from smooth, which is either the smoothed data, or
      smoothed data + weights used in the smooothing
    :rtype: numpy array
    """
    boxsize = oddbox("box", boxsize, *args, **kwargs)
    weights = numpy.ones(boxsize) * (1./boxsize)
    weights = weights/numpy.sum(weights)
    return smooth(data, weights, *args, **kwargs)

def triangle(data, boxsize=9, *args, **kwargs):
    """Smoothing with a triangular distribution
    
    Generates an array of length N filled with values in a symmetric 
    triangular distribution, then calls smooth with this window
    
    :param data: The input array
    :type data: numpy array
    
    :param boxsize:  total width of the smoothing window
    :type boxsize: integer
    
    :return: Results from smooth, which is either the smoothed data, or smoothed data 
      and weights used in the smooothing
    :rtype: numpy array
    """
    boxsize = oddbox("box", boxsize, *args, **kwargs)
    weights = numpy.arange(boxsize)
    weights = boxsize/2. - numpy.abs(weights - numpy.mean(weights))
    weights = weights / numpy.sum(weights)
    return smooth(data, weights, *args, **kwargs)
    
def gaussian(data, boxsize=9, nsigma=3, *args, **kwargs):
    """Smoothing with a gaussian distribution of size boxsize that covers nsigma widths
    
    Generates an array of length N filled with values of 1/N, then calls smooth with this window
    
    Arguments:
    
    :param data: The input array
    :type data: numpy
    
    :param boxsize:  total width of the smoothing window
    :type boxsize: integer
    
    :param nsigma: number of sigmas (std devs) to contain in the len(boxsize) elements. 
    :type nsigma: float
    
    Larger values of sigma give a tighter distribution in the centre and more delta-function 
    like behaviour, low sigma value gives a smoother distribution with more uniform like
    behaviour.
    
    :return: Results from smooth, which is either the smoothed data, or smoothed data 
      and weights used in the smooothing.
    :rtype: numpy array
    """
    boxsize = oddbox("box", boxsize, *args, **kwargs)
    sigma = boxsize/ ((nsigma+1.0e-10)*numpy.sqrt(2*numpy.log(2)))
    weights = numpy.arange(boxsize)
    weights = (weights - numpy.mean(weights))
    weights = numpy.exp(-(weights/sigma)**2)
    weights = weights/numpy.sum(weights)

    return smooth(data, weights, *args, **kwargs)
    
