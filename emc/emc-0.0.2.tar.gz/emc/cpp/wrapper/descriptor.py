'''
Wrapper for C++ descriptor & descriptor distancing class.
'''

from numpy import size, float32, zeros

from emc.cpp.swig import emcpp


numDescriptors = emcpp.NUM_DESCRIPTORS


class DescriptorDirectoryWrapper(object):
    '''
    Wrapper for C++ descriptor & descriptor distancing class.
    '''
    
    def __init__(self, modelDir, numBins = 128, fourierSize = 2048, numClusters = 1, gamma = 1.0):
        '''
        Initialize by model directory and descriptor directory properties.
        This will use each model from directory as corpus object.
        Will add to descriptor correlationr and compute cluster center descriptors.
        '''
        self.modelDir = modelDir
        self.numModels = modelDir.numModels
        self.numTracks = modelDir.models[0].numTracks
        self.numBins = numBins
        self.fourierSize = fourierSize
        self.numClusters = numClusters
        self.gamma = gamma
        
        self.native = emcpp.DescriptorDirectory(self.numModels, self.modelDir.numTracks, self.numBins, self.fourierSize, self.numClusters)

        for modelIdx, model in enumerate(self.modelDir.models):
            for trackIdx, track in enumerate(model.tracks):
                self.native.addDescriptor(track.notes.T, modelIdx, trackIdx)
        
        self.native.calculateCentreDescriptors()
        
    
    def modelFitness(self, model):
        '''
        Calculates fitness values based on correlations between model's and centre descriptors.
        '''
        ret = zeros((self.numTracks, numDescriptors), dtype=float32)
        for trackIdx, track in enumerate(model.tracks):
            ret[trackIdx, :] = self.native.trackFitness(track.notes.T, trackIdx, numDescriptors, self.gamma)
        return ret
        
        
    def modelCorrelationsWithCentres(self, model):
        '''
        Calculates a model's descriptor and the correlations between it
        and the centre descriptors from the corpus.
        '''
        ret = zeros((self.numTracks, self.numClusters * numDescriptors), dtype=float32)
        for trackIdx, track in enumerate(model.tracks):
            ret[trackIdx, :] = self.native.trackCorrelationsWithCentres(track.notes.T, trackIdx, self.numClusters * numDescriptors)
        ret.shape = (self.numTracks, self.numClusters, numDescriptors)
        return ret
    
    
    def correlationsWithCentres(self, descriptor, trackIdx):
        '''
        Calculate correlations between a descriptor
        and the centre descriptors from the corpus.
        '''
        ret = self.native.correlationsWithCentres(descriptor.ravel(), trackIdx, self.numClusters * numDescriptors)
        ret.shape = (self.numClusters, numDescriptors)
        return ret
    
    
    def descriptor(self, model):
        '''
        Returns descriptor of model, i.e. an array of histograms/FFTs. 
        '''
        ret = zeros((self.numTracks, numDescriptors * self.numBins), dtype=float32)
        for trackIdx, track in enumerate(model.tracks):
            ret[trackIdx, :] = self.native.trackDescriptor(track.notes.T, numDescriptors * self.numBins)
        ret.shape = (self.numTracks, numDescriptors, self.numBins)
        return ret
    
    
    def descriptors(self):
        '''
        Returns all descriptors used in directory.
        '''
        ret = self.native.descriptors(self.numModels * self.numTracks * numDescriptors * self.numBins)
        ret.shape = (self.numModels, self.numTracks, numDescriptors, self.numBins)
        return ret
    
    
    def centreDescriptors(self):
        '''
        Returns centre descriptors of corpus.
        '''
        ret = self.native.centreDescriptors(self.numClusters * self.numTracks * numDescriptors * self.numBins)
        ret.shape = (self.numClusters, self.numTracks, numDescriptors, self.numBins)
        return ret
    
    
    def clusters(self):
        '''
        Returns clusters - indices of clusters each reference descriptor's been classified into.
        '''
        ret = self.native.clusters(self.numModels * self.numTracks * numDescriptors)
        ret.shape = (self.numModels, self.numTracks, numDescriptors)
        return ret
        
    
    def fourier(self, data, size = None, normalize = True):
        '''
        Returns FFT of data.
        '''
        if size is None:
            size = self.numBins
            
        return self.native.fourier(data, size, normalize)
    
    
    def diffFourier(self, data, size = None, normalize = True):
        '''
        Returns FFT of data.
        '''
        if size is None:
            size = self.numBins
            
        return self.native.diffFourier(data, size, normalize)
    
    
    def __getstate__(self):
        '''
        Do not serialize native.
        '''
        return (self.modelDir, self.numBins, self.fourierSize, self.numClusters, self.gamma)
    
    
    def __setstate__(self, state):
        '''
        Do not serialize native.
        '''
        self.__init__(state[0], state[1], state[2], state[3], state[4])




def normalize(data):
    '''
    Wrapper for normalization.
    '''
    emcpp.normalize(data)
    
    
    
def histogram(data, size = 128, normalize = True):
    '''
    Wrapper for histogram.
    '''
    return emcpp.histogram(data, size, normalize)
    
    
    
def diffHistogram(data, size = 128, normalize = True):
    '''
    Wrapper for histogram of first-order derivative.
    '''
    return emcpp.diffHistogram(data, size, normalize)



def correlation(descriptor1, descriptor2):
    '''
    Calculate correlations between 2 descriptors.
    '''
    if descriptor1.ndim == 1:
        length = 1
        numBins = size(descriptor1)
    else:
        length, numBins = descriptor1.shape
    
    return emcpp.correlation(descriptor1.ravel(), descriptor2.ravel(), int(length), int(numBins))



def fitness(data, gamma = 1.0):
    '''
    Calculates fitness values based on correlations. Assumes input array are correlations between descriptors.
    '''
    emcpp.fitness(data, gamma)