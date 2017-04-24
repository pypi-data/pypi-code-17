from numpy import *
from ..util import make_gen


def mask_peaks(peaks):
    """
    Given a window of peaks, mask all but the maximum to zero
    """
    return array(peaks) * (arange(len(peaks)) == argmax(peaks))


def suppress_peaks(data, thresh):
    """
    Find peaks in data, suppressing neighboring, smaller peaks in the event that we
    are using some kind of nois detector (such as subsample_matched_filter()) that
    can have multiple peaks output for a single event. This function will find all
    peaks exceeding a threshold, but for each contiguous range of peaks it will
    emit only the maximum of the range, truncating all others to zero.

    Parameters
    ----------
    data : 1-D signal (array or iterator)
        The signal stream to suppress peaks in
    thresh : number
        The threshold to define peaky areas

    Return values
    -------------
    peakstream : 1-D signal
        A stream of peaks with all other values set to zero
    """
    data = make_gen(data)

    while True:
        # Always reset our data window
        data_win = [next(data)]

        try:
            # Read stuff into data_win as long as the data exceeds threshold
            while abs(data_win[-1]) > thresh:
                data_win += [next(data)]
        except StopIteration:
            # Yield any values if we have them
            if len(data_win):
                for val in mask_peaks(data_win):
                    yield val

            # Finally, re-raise the StopIteration
            raise StopIteration()

        # The number of thresh-surpassing points is len(data_win) - 1:
        if len(data_win) > 1:
            for val in mask_peaks(data_win[:-1]):
                yield val

        # No matter what, we always yield a 0 here for the last data point that
        # didn't exceed thresh
        yield data_win[0] * 0
