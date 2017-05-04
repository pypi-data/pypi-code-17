import numpy as np


def calculate_reverse_indices(incount, full_index, sparse=False):
    """Calculates the indices that go into each bin in a histogram
        and returns an array of values where
        ri[index] is list of indices of bins in the source data that
        are part of the [index] bin in the histogram.
        Called from within grid_data only.
    """
    #Two arrays to consider here
    #The count in each bin, regardless of data validity (missing data, masks, etc.)
    #called count_full, and the full_index that places every element into the output array
    
    #We define two arrays, rii contains arrays of each for each output bin, where each
    #array is the list of indices that go into that bin.  rjj contains 
    
    array_length = incount.size
    shp = incount.shape
    #create the storage arrays
    rii = np.empty(array_length, dtype=np.ndarray)
    rjj = np.zeros(array_length, dtype=np.int)
    #flatten the incount array
    c = np.reshape(incount, incount.size)
    #calculate the unique values and their indices, and an array that can
    #be used to reconstruct the full_index
    (fi_value, fi_index, fi_inverse) = \
            np.unique(full_index, return_index=True, return_inverse=True)
    #count the elements that go into each bin
    bc_fi_inverse = np.bincount(fi_inverse)

    #IF we're in sparse mode, then we should index into a counter array, instead of the real fi_value array    
    if sparse:
        locations = np.arange(fi_value.size)
    else:
        locations= fi_value

#new inversion code
    temp = np.argsort(fi_inverse)
    counter=0
    for count,elem in enumerate(locations):
        rjj[elem] = bc_fi_inverse[count]
        rii[elem] = np.sort(temp[counter:counter+rjj[elem]])# np.where(fi_inverse==count)[0] 
        counter=counter+rjj[elem]
#The commented-out code should be the equivalent code, but it's slower than the where method above
#If there are problems, change the code back to calculate the full arrays as below.
#    #For each pair of value and its count, define an array
#    #of the appropriate (count) size
#    for loc, val in zip(locations, bc_fi_inverse):
#        if val > 0:
#            rii[loc] = np.zeros(val, dtype=int)
#    #no that we've allocated enough room
#    #loop through the inverse array, find its location in the main array outside
#    #using the fi_value lookup (we could have just used full_index, but not in sparse mode)
#
#
#    for count, val in enumerate(fi_inverse):
#        #I think this can be replaced by index=locations[val] after the definition above
#        if sparse is False:
#            index = fi_value[val]
#        else:
#            index = val
#        #rjj'th element of the riith element is set the location (count) of the value in fi_inverse, 
#        #which is equivalent to the location in the input array
#        rii[index][rjj[index]] = count
#        #a counter, to know which element we should write to next.
#        rjj[index] = rjj[index] + 1
    #finally, reshape, and output
    rii = np.reshape(rii, shp)
    rjj = np.reshape(rjj, shp)

    return rii, rjj


def calculate_statistics(full_index, weights,
                         bs, square=None, sparse=False, missing_data=None):
    """
    Calculates the mean, variance,and count of each bin indexed in full_index with data coming from 
    weights
    """
    
    #we have two data arrays here. The first is the 'full_index' that identifies
    #the bin into which each element goes, and the un-normalized weight of that element
    #in weights. In reality, 'weights' is the data we want to grid. The function we call
    #later (bincount) happens to consider them as weights to a different array
    #but in doing so calculates the statistics appropriately.
    
    #calculate the product of bin sizes to get the largest possible array size
    sz = 1
    for d in bs:
        sz = sz * d
    #now call numpy.unique asking for the 
    #fi_value = values that give a unique array
    #fi_index = the indices of the values in fi_value
    #fi_inverse = the location of each element in full_index in fi_value
    #can be used to reconstruct the full_index value OR used to bin properly later
    (fi_value, fi_index, fi_inverse) =\
            np.unique(full_index, return_index=True, return_inverse=True)
    
    #now deal with missing data if present. #If we find no real data (len(w[0])==0)
    #then our answer is pretty simple as the result is also all zeros (for variance and count),
    #or missing for mean.
    if missing_data:
        w = np.where(weights != missing_data)
        if len(w[0]):
            index = w[0]
        else:
            if sparse is False:
                m = np.zeros(bs)
                return (m + missing_data, m.copy(), m.copy())
            else:
                s = np.zeros(len(fi_value))
                return (s + missing_data, s.copy(), s.copy())
    #OR if the arrays are masked numpy arrays, then we perform the same analysis
    #but ask whether the mask is
    #just a single bool, then perform the same test as above
    #an array of bools, then invert it to get the data selection array
    #(mask==true -> bad data), (index=true -> good_data)
    elif isinstance(weights, np.ma.core.MaskedArray):
        if isinstance(weights.mask, np.bool_):
            if not weights.mask:
                index = slice(None, None, None)
            else:
                if sparse is False:
                    m = np.zeros(bs)
                    return (m + missing_data, m.copy(), m.copy())
                else:
                    s = np.zeros(len(fi_value))
                    return (s + missing_data, s.copy(), s.copy())
        elif isinstance(weights.mask, np.ndarray):
            index = ~weights.mask
    #OR there's no missing data, select all the data
    else:
        index = slice(None, None, None)
    #for convenient later, we perform a count on all of the data, regardless of 
    #it's validity
    count_full = np.bincount(fi_inverse[slice(None, None, None)])
    #No calculate the count (unweighted bincount) of the valid data
    #and the sum of the data in each bin (weighted by data)
    #and the sum of squares (weighted by data**2)
    try:
        count = np.bincount(fi_inverse[index])
        su = np.bincount(fi_inverse[index], weights=weights[index])
        var = np.bincount(fi_inverse[index], weights=weights[index] ** 2)
    #not sure what exception I'm expecting here, anymore. 
    except:
        count = 0. * count_full
        su = 0. * count_full
        var = 0. * count_full
    #if we DONT want sparse data then the array_length is product of all dimensions
    #and the shape is given in the binsize array bs
    #if we DO want sparse data, the array_length is the largest number in the unique inverse
    #array fi_inverse, which seems like it should eqyal the length of fi_value
    if sparse is False:
        array_length = sz
        shp = bs
    else:
        array_length = np.max(fi_inverse) + 1
        shp = np.max(fi_inverse) + 1
    #construct the output arrays
    m = np.zeros(array_length)
    c = np.zeros(array_length)
    cf = np.zeros(array_length)
    v = np.zeros(array_length)
    w = np.where(count != 0)[0]

    #for count_full we can't look for the number of valid elements, because there don't
    #have to be any, so we copy the data immediately
    if sparse is False:
        cf[fi_value] = count_full
    else:
        cf = count_full #no indexing -> straight copy 
    
    #if there is data (w.size>0) then save the data in the output, otherwise
    #the initialization to 0 is good enough.
    #If NOT sparse, then the indexing is stored in fi_value (where its count is 
    #nonzero
    #if YES sparse, then the indexing is just the locations of nonzero elements
    #which I think is every element in w.
    forward_index = None
    forward_index = fi_value
    if w.size:
        if sparse is False:
            index = fi_value[w]
        else:
            index = w
        #divide the sums by the counts to get means, 
        m[index] = su[w] / count[w]
        v[index] = var[w] / count[w]
        c[index] = count[w]
#        cf[index] = count_full[w]
    #if square is set, return the mean of the square, not the variance.
    if square is None:
        v = v - m * m
    else:
        pass
    #in NON sparse mode, we need to reshape the output to N dimensional arrays
    #otherwise shp is just the array length and nothing happens here.
    m = np.reshape(m, shp)
    v = np.reshape(v, shp)
    c = np.reshape(c, shp)
    cf = np.reshape(cf, shp)
    
    return (m, v, c, cf, forward_index)


def grid_data(data, bins, mn=None, mx=None,
                reverse_indices=None, square=None,
                sparse=False, missing_data=None):
    """Grids data into regular grid of bins
    data is an N*M numpy array, where:
    N is the number of data points,
    A<M is the number of dimensions we are binning over
    and D=M-A is the number of dimensions of data we bin.
    Bins can be a list of arrays of bin edges, or a list of
    bin sizes (integers). If bin edges are given, they are
    assumed to be monotonic and used as in bincount. If they
    are bin sizes, optional maximum (mx) and minimum (mn)
    values for all dimensions can be given. In this case,
    the edge bins (above mx, or below mn) contain the overflow data.
    By default, the function returns the mean value, the variance,
    and the counts of each bin. If reverse_indices is set to True,
    the indices in the data array (along the N dimension) of each
    element that contributes to every bin is stored in a variable
    length array in that bin.
    
    :param data: 2-dimensional(N,M) array of data to grid. 
            The first A columns are used as axes and require corresponding entries 
            in the bins list. The remaining D columns are data to be binned
    :type data: numpy array

    :param bins: list of bin edges (upper edge) or bin lengths for each axis in A
    :type bins: list
    
    :param mn: list of bin minima if the bins list contains integer number of bins
    :type mn: list

    :param mx: list of bin maxima if the bins list contains integer number of bins
    :type mx: list

    :param reverse_indices: logical to determine if the indices that are used in each grid box are calculated
    :type reverse_indices: bool

    :param square: logical to determine if the mean of the square data mean(X**2) is returned instead of variance (mean(X**2)-mean(X)**2)
    :type square: bool

    :param sparse: logical to determine if the sparse method is used instead and a 1D gridded dataset is created
    :type sparse: bool
    
    :param missing_data: list of missing data entries for each data array in D(better to mask arrays instead)
    :type missing_data: list


    :return: Mean, calculated mean value of each grid box
    :return: Variance, calculated variance of each grid box (or mean of square)
    :return: Count, number of elements in each grid box
    
    With reverse_indices=true
    
    :return: ri, array containing a list for each gridpoint containing the index back into D of each datapoint
    :return: rj, the length of each list in ri
    
    Types
    
    :rtype: tuple of (numpy (D+1)d, numpy (D+1)d, numpy (D+1)d) (no reverse_indices, no sparse)
    :rtype: tuple of (numpy 1d, numpy 1d, numpy 1d) (no reverse_indices, sparse)
    :rtype: tuple of (numpy (D+1)d, numpy (D+1)d, numpy (D+1)d,numpy (D+1)d,numpy (D+1)d) (reverse_indices, no sparse)
    :rtype: tuple of (numpy 1d, numpy 1d, numpy 1d,numpy 1d,numpy 1d) (reverse_indices, sparse)

    """
    #glossary
    #axis/axes = The first M rows of data that are used to filter the data into a grid
    #bins = The values of the axes that are used to group elements
    #data = The non-filterable part of the input data that is grouped by axes into bins
    
    import numpy as np
    #get the shape of the incoming data, create a bin size array read for bin data
    s = data.shape
    bs = np.zeros(len(bins), dtype=np.int)
    #if the first element is a numpy array, they should all be
    #then I assume that each element in bins contains the upper bin edges
    #of each dimension.
    if type(bins[0]) == np.ndarray:
        #if arrays are given in 'bins', assume they are bin edges
        use_bins = bins
        for i in range(len(bs)):
            bs[i] = len(use_bins[i])
            pass
        pass
    else:
        #if non-lists (int,long,float) are given, assume they are nbins
        #convert them to longs
        bs = [int(b) for b in bins]

        #if min or max are not given, calculate them
        if mn is None:
            mn = np.min(data, 0)
        if mx is None:
            mx = np.max(data, 0)
        use_bins = []
        for i in range(len(bs)):
            use_bins.append(
                np.linspace(mn[i], mx[i], bs[i] + 1)
                )
        pass

    #now we have bin edges for each of the axes, either supplied or generated
    #Calculate the product of the bin sizes
    sz = 1
    for d in bs:
        sz = sz * d
    #Create the index array that is the same shape as the incoming data
    #except for one bin in the last dimension,
    #TODO: I think the s[1]-1 dimension could be len(bs)
    #index = np.zeros((s[0], s[1] - 1), dtype=np.int)
    #implementing the TODO above
    index = np.zeros((s[0], len(bs)), dtype=np.int)
    #for each index array, call numpy.digitize on the data which calculates
    #the index into the bin array that each element of the axis data appears in.
    #We only use n-1 elements of each bin so that the overflow appears in the last
    #bin, not in the (undefined) bin above the last defined one.
    for i in range(len(bs)):
        index[:, i] = np.clip(bs[i] - np.digitize(data[:, i],
                            use_bins[i][::-1]),
                            0, bs[i] - 1)

    #Now we have the indexes into each dimension, combine them into a single index
    #by scaling the full_index by the product of the prior dimensions and adding the
    #next index. This is the same way you construct a multi-dimension array out of
    #one dimensional data.
    full_index = index[:, 0]
    for i in range(1, len(bs)):
        full_index = full_index * bs[i] + index[:, i]

    lb = len(bins)
    r = data.shape[1] - lb
    #if there is only one 'data' row (i.e. 1 non-filterable row) then we need to
    #call the calculate_statistics function with the correct shape
    #OR we loop through the data and call the function for each row.
    if r==0:
        (m, v, c, cf,forward_index) = calculate_statistics(full_index, data[:, -1]*0., bs,
                                        square=square, sparse=sparse
                                        )
        count = c
        count_full = cf
    elif r == 1:
        (m, v, c, cf,forward_index) = calculate_statistics(full_index, data[:, -1], bs,
                                        square=square, sparse=sparse,
                                        missing_data=missing_data)
        count = c
        count_full = cf
    else:
        #if there's no missing data, generates a list of 'None's to fool the algorithm,
        #otherwise there must be the correct number of missing data values for the
        #size of the data. Also acceptable is to pass in a masked array instead,
        #with no missing data.
        if missing_data is None:
            missing_data = [None for i in range(lb, data.shape[1])]
        for i in range(lb, data.shape[1]):
            (m, v, c, cf, forward_index) = calculate_statistics(full_index, data[:, i], bs,
                                            square=square, sparse=sparse,
                                            missing_data=missing_data[i - lb])
            #If we wanted non-sparse data, m will be Naxis dimensional, so generate
            #a slice-index thing for that shape
            #otherwise generate a single dimension slice, with a blank axis at the
            #end to allow concatenation
            slall = slice(None, None, None)
            if sparse is False:
                sl = [slall for j in range(len(m.shape))]
                sl.append(np.newaxis)
            else:
                sl = [slall, np.newaxis]
                pass
            #For the first element i==lb we need to create the final storage variables
            #for other elements i>lb , we need to concatenate
            if i == lb:
                m2 = m[sl]
                v2 = v[sl]
                c2 = c[sl]
                count = c
                count_full = cf
            else:
                m2 = np.concatenate((m2, m[sl]), axis=-1)
                v2 = np.concatenate((v2, v[sl]), axis=-1)
                c2 = np.concatenate((c2, c[sl]), axis=-1)
                pass
            pass

        m = m2
        v = v2
        c = c2
    #if we don't want to calculate the reverse indices array, we can stop here
    #otherwise we need to call the appropriate function and add the results
    #to the tuple we return
    result = [m,v,c]
    if sparse:
        result.append(forward_index)
    if reverse_indices:
        ri, rj = calculate_reverse_indices(count_full, full_index, sparse=sparse)    
        result.extend([ri,rj])
    return result
