'''
Provides general methods for K-means and GMM clustering.
@author Csaba Sulyok
'''
from numpy import size, zeros, uint8, float32, arange, argmin, mean


def cluster(x, K, maxiter = 1000):
    '''
    Performs clustering on a 1-D array. Uses K-means.
    Returns cluster indices and centres.
    
    TODO: extend to n-D
    TODO: add option for GMM so variance will also matter
    TODO: use this also for descriptor clustering.
    
    x - input array
    K - number of clusters
    maxiter - maximal number of iterations before exiting. avoids oscillatory behavior
    '''
    
    N = size(x)
    
    # cluster indices. all will have values 0:K
    cl = zeros(N, dtype=uint8)
    # centre values - start with first units in data
    cntr = x[0:K].astype(float32)
    # distances between data and current cluster centres
    dist = zeros((N, K), dtype=float32)
    
    changed = True
    it = 0
    
    while changed and it < maxiter:
        
        # E-step - assign each value to a cluster
        for n in arange(N):
            for k in arange(K):
                # TODO: generalize the distancing method
                # descriptor clustering will use correlation
                dist[n,k] = abs(x[n] - cntr[k])
        
        # check if anything has changed
        new_cl = argmin(dist, axis=1)
        changed = (new_cl != cl).any()
        cl = new_cl
        
        # M-step - recalculate centres
        for k in arange(K):
            cntr[k] = mean(x[cl == k])
        
        it += 1
    
    
    return (cl, cntr)