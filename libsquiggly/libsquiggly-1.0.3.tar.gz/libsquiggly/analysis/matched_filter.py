from numpy import *
from ..util import make_gen
from ..resampling import sinc_fractional_shift


def energy(x, demeaned=False):
    """
    Calculate the energy in x, demeaning if necessary

    Parameters
    ----------
    x : 1-D signal array
        The actual timeseries window to calculate the energy over
    demeaned : bool (default: False)
        If the signal has already been demeaned, don't bother calculating the mean again

    Return values
    -------------
    energy : float
        The calculated energy of the input signal
    """
    if not demeaned:
        x_d = x - mean(x)
        return sqrt(real(vdot(x_d, x_d)))
    else:
        return sqrt(real(vdot(x, x)))


def matched_filter(data, h, step=1, mode="same"):
    """
    Perform matched filtering between a datastream and an array representing the template filter
    The result from this function is normalized to fall within the range [0, 1]

    Parameters
    ----------
    data : 1-D signal (array or iterator)
        The actual timeseries to filter through.  This can be an array or an iterator
    h : 1-D signal
        The filter to be used as the template filter to be searched for
    step : int (default: 1)
        To save computation time, the output can be pre-emptively decimated before being returned
        from this function.  Set this number to an integer greater than 1 to skip output samples.
    mode : string
        Similar to numpy.convolve(); output length should be "same" or "valid" to disable/enable
        chomping of output that is due to transient response at the beginning/end of a stream.
        Note that since this function assumes an infinite stream, it only bothers with the beginning

    Return values
    -------------
    data_hat : 1-D signal array stream
        This function acts as a generator, calculating samples on demand.  Use an iteration
        to pull all the data out of it. Example:
            data_hat = [x for x in matched_filter(data[startIdx:], barker)]
        Alternatively, use the acollect() function in libsquiggly.util:
            data_hat = acollect(matched_filter(data[startIdx:], barker))
    """
    data = make_gen(data)

    # Demean/normalize h first, so that we never have to do it again
    h = copy(h) - mean(h)
    h = h / energy(h, demeaned=True)
    h_len = len(h)

    # Grab the first element
    x = next(data)

    # Load in a single step
    buff = zeros((len(h),), x.dtype)
    buff[-1] = x
    for idx in range(step - 1):
        buff = roll(buff, -1, 0)
        buff[-1] = next(data)

    # if mode is "valid", skip over any extra samples that we need to to skip
    # the transient response
    if mode == "valid":
        for idx in range(len(h) - (step - 1)):
            buff = roll(buff, -1, 0)
            buff[-1] = next(data)

    # Calculate dot product at each point, normalizing out x's energy
    while True:
        x_slice = buff - mean(buff)
        x_slice_energy = energy(x_slice)

        if x_slice_energy == 0.0:
            yield 0.0
        else:
            yield dot(x_slice, h) / x_slice_energy

        for idx in range(step):
            buff = roll(buff, -1, 0)
            buff[-1] = next(data)


def subsample_matched_filter(data, h, M=5, mode="same"):
    """
    Perform matched filtering between a datastream and an array representing the template filter
    The result from this function is normalized to fall within the range [0, 1]

    This function differs from matched_filter() in that it creates a polyphase matched
    filterbank to detect subsample shifted template filters embedded in data. The parameter
    M controls the number of evenly-spaced, shifted matched filters created. The result
    returned is the maximum absolute value across polyphase matched filters.

    Parameters
    ----------
    data : 1-D signal (array or iterator)
        The actual timeseries to filter through.  This can be an array or an iterator
    h : 1-D signal
        The filter to be used as the template filter to be searched for
    M : int (default: 5)
        The number of shifted matched filters to generate and use
    mode : string
        Similar to numpy.convolve(); output length should be "same" or "valid" to disable/enable
        chomping of output that is due to transient response at the beginning/end of a stream.
        Note that since this function assumes an infinite stream, it only bothers with the beginning

    Return values
    -------------
    data_hat : 1-D signal array stream
        This function acts as a generator, calculating samples on demand.  Use an iteration
        to pull all the data out of it. Example:
            data_hat = [x for x in subsample_matched_filter(data[startIdx:], barker)]
        Alternatively, use the acollect() function in libsquiggly.util:
            data_hat = acollect(subsample_matched_filter(data[startIdx:], barker))
    """

    data = make_gen(data)

    # Create one matched filter for each fractional shift we want to perform
    mfilts = [matched_filter(data.copy(), sinc_fractional_shift(
        h, idx * 1.0 / M)) for idx in range(M)]

    while True:
        # Get the outputs of all matched filters
        mfilt_outputs = array([next(mfilts[idx]) for idx in range(M)])

        # Find the maximum absolute value
        maxind = argmax(abs(mfilt_outputs))

        # Yield that (complex) value
        yield mfilt_outputs[maxind]
