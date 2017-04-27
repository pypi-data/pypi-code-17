'''
Script to separate a model track into multiple tracks by clustering their pitch.
Clustering occurs based not just based on pitch, but also based on time difference,
so notes closer together in both time and pitch are clustered together.

@author Csaba Sulyok
'''

from numpy import int16, zeros, exp, log2, arange, uint8, float32, average, \
    argmin

from emc.core.core.model import Model
from emc.core.integ.modeldir import ModelDirectory


def clusterPitchesToTwoTracks(pitches, onsets = None, sig2 = 8, maxiter = 100):
    '''
    Cluster by pitch and time into two tracks.
    Assumes one-track model as input.
    
    sig2 - Variance of log-normal curve used to give importances
    to time intervals. The larger this value, the further in time notes are taken into weighting
    when assigning notes to a cluster.
    '''
    N = pitches.shape[0]
    
    if onsets is None:
        onsets = arange(N)
    
    # build log-normal curve for weighting when
    # assigning to cluster
    T = max(onsets) + 1
    w = zeros(T)
    w[1:] = exp(-(log2(arange(1, T))) ** 2 / sig2)
    
    # initial clusters separated in middle
    # between min and max pitch
    cl = (pitches < (float(min(pitches) + max(pitches)) / 2)).astype(uint8)
    
    # distances from cluster "centre"
    # centre not actually a point, since distancing depends on time
    dist = zeros((N, 2), dtype=float32)
    
    changed = True
    it = 0
        
    while changed and it < maxiter:
        #print cl
        
        # extract pitches/onsets currently chosen to be in cluster 0/1
        pitches0 = pitches[cl == 0]
        pitches1 = pitches[cl == 1]
        onsets0 = onsets[cl == 0]
        onsets1 = onsets[cl == 1]
        
        # M-step
        for n in arange(N):
            # for each note, calculate distance
            # taking regular mean would be same as K-means clustering
            # instead, we weight based on log-normal from above
            tweights0 = w[abs(onsets[n] - onsets0)]
            tweights1 = w[abs(onsets[n] - onsets1)]
            dist[n, 0] = average(abs(pitches[n] - pitches0), weights = tweights0)
            dist[n, 1] = average(abs(pitches[n] - pitches1), weights = tweights1)
            #dist[n, 0] = sum(abs(pitches[n] - pitches0) * tweights0) / sum(tweights0)
            #dist[n, 1] = sum(abs(pitches[n] - pitches1) * tweights1) / sum(tweights1)
    
        # E-step
        # reassign all notes to clusters based on distance
        # if nothing changes, exit
        new_cl = argmin(dist, axis=1)
        changed = (new_cl != cl).any()
        cl = new_cl
        
        it += 1
    
    print 'Finished in %d iterations' %it
    return cl



def clusterModelByPitchToTwoTracks(model, sig2 = 8, maxiter = 100):
    '''
    Cluster model to 2 tracks
    '''
    notes = model.tracks[0].notes
    pitches = notes[:,4].astype(int16)
    onsets = notes[:,2].astype(int16)
    return clusterPitchesToTwoTracks(pitches, onsets, sig2, maxiter)



def clusterModelDirectoryByPitchToTwoTracks(modelDir, sig2 = 8, maxiter = 100):
    '''
    Clusters all models in directory to 2 tracks.
    '''
    for i, model in enumerate(modelDir.models):
        print 'Separating %s into 2 tracks' %modelDir.filenames[i]
        
        notes = model.tracks[0].notes
        
        cl = clusterModelByPitchToTwoTracks(model, sig2, maxiter)
        
        # extract notes based on cluster
        # update IOI using onsets, since that depends on previous note
        # warning: will not work if onsets overflowed
        notes1 = notes[cl == 0, :]
        notes1[0, 0] = notes1[0, 2]
        notes1[1:, 0] = notes1[1:, 2] - notes1[:-1, 2]
        notes2 = notes[cl == 1, :]
        notes2[0, 0] = notes2[0, 2]
        notes2[1:, 0] = notes2[1:, 2] - notes2[:-1, 2]
        
        print 'Separation complete. Number of notes in tracks: %d/%d' %(notes1.shape[0], notes2.shape[0])
        print ''
    
        # build new 2-track model
        newmodel = Model(model.ticksPerQuarterNote, 2, model.dtype)
        newmodel.tracks[0].notes = notes1
        newmodel.tracks[1].notes = notes2
        newmodel.length = newmodel.tracks[0].length = newmodel.tracks[1].length = model.length
    
        modelDir.models[i] = newmodel



def clusterBachMidis(sig2 = 8):
    md = ModelDirectory('../../../../../midi/bach_1track')
    clusterModelDirectoryByPitchToTwoTracks(md, sig2)
    md.write('../../../../../midi/bach_2track', includeEmptyTracks = False)



if __name__ == '__main__':
    clusterBachMidis()

'''
pitches = array([10, 11, 12, 13, 14, 7, 8, 9, 10, 11], dtype=int16)
onsets  = array([0,  1,  2,  3,  4,  3, 4, 5, 6,  7], dtype=int16)

cl = clusterPitchesToTwoTracks(pitches, onsets, 2)
print cl
plot(onsets, pitches, '*')
show()
'''