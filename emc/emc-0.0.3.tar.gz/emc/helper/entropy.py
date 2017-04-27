from numpy import array, uint8, unique, log2, sum, zeros, arange, float32
from numpy.random import random
from emc.cpp.swig.emcpp import entropy


def entropy2(data):
    '''
    Measure binary Shannon entropy of a 2-D data set per column.
    Returns value between 0 and 255 if casting needed to uint8.
    '''
    cols = data.shape[1]
    ret = zeros(data.shape[1], dtype=float32)
    
    for col in arange(cols):
        ret[col] = entropy(data[:, col])
    
    return ret


def entropyModel(model):
    '''
    Measure entropy of model.
    Only take IOI, duration and pitch.
    Values per track are flattened into a vector.
    '''
    ret = zeros([model.numTracks * 3], dtype=float32)
    for trackIdx, track in enumerate(model.tracks):
        ret[trackIdx*3] = entropy(track.notes[:, 0])
        ret[trackIdx*3 + 1] = entropy(track.notes[:, 1])
        ret[trackIdx*3 + 2] = entropy(track.notes[:, 4])
    return ret



if __name__ == '__main__':
    a1 = array([1,1,1,1,1,1,1,1], dtype=uint8)
    a2 = array([1,2,1,2,1,2,1,2,1,2,1,2], dtype=uint8)
    a3 = array([1,2,3,1,4,3,1,2,3], dtype=uint8)
    a4 = array(random(1000) * 256, dtype=uint8)
    
    for a in [a1, a2, a3, a4]:
        print entropy(a)
    
    a5 = zeros([256, 3], dtype=uint8)
    a5[:, 0] = array(random(256) * 256, dtype=uint8)
    a5[:, 1] = 1
    a5[:, 2] = arange(256, dtype=uint8)
    
    print entropy2(a5)

