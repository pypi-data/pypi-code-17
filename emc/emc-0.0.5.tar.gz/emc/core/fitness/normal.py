'''
Length-related fitness tests for musical pieces.

@author: Csaba Sulyok
'''
from numpy import array, float32, zeros, size, arange, exp, float64, frombuffer, max, round

from emc.helper.entropy import entropyModel


class NormalFitnessTest(object):
    '''
    Fitness test for value mapped to a multidimensional normal distribution.
    Given a set of means and variances, caches values of a normal distribution,
    so it can quickly be evaluated.
    '''
    
    def __init__(self, mu = [256], sig = [32]):
        self.mu = array(mu, dtype=float32)
        self.sig = array(sig, dtype=float32)
        self.buildValues()
    
    
    def buildValues(self):
        '''
        Evaluate and cache values up until 2*mu to avoid exping constantly.
        '''
        muends = round(2 * self.mu)
        self.values = zeros((size(self.mu), max(muends)), dtype=float32)
        
        for idx in arange(size(self.mu)):
            self.values[idx, :muends[idx]] = exp(-(arange(round(2 * self.mu[idx]), dtype=float64) - self.mu[idx]) ** 2 / (2 * self.sig[idx] ** 2))


    def normalValueOf(self, item):
        '''
        Recall cached value for fitness, otherwise 0.
        '''
        ret = float32(0)
        for idx in arange(len(self.mu)):
            if 0 <= item[idx] < self.values.shape[1]:
                ret += self.values[idx, item[idx]]
            else:
                return float32(0)
            
        return ret / float32(len(self.mu))
        
        
    def __getstate__(self):
        '''
        Do not serialize cached values.
        '''
        return (bytearray(self.mu.astype(float32)),\
                bytearray(self.sig.astype(float32)))


    def __setstate__(self, state):
        '''
        Rebuild cached values when deserializing.
        '''
        self.mu  = frombuffer(state[0], dtype=float32)
        self.sig = frombuffer(state[1], dtype=float32)
        self.buildValues()




class GivenLengthAndNumNotesFitnessTest(NormalFitnessTest):
    '''
    Fitness test for musical score length and number of notes.
    Maximum reward is given to a piece with length and number of notes of expected values.
    '''
    name = 'Length&NumNotes'
    
    def run(self, model):
        return self.normalValueOf((model.length, model.numNotes()))



class GivenLengthFitnessTest(NormalFitnessTest):
    '''
    Fitness test for musical score length and number of notes.
    Maximum reward is given to a piece with length of expected values.
    '''
    name = 'Length'
    
    def run(self, model):
        return self.normalValueOf([model.length])
    
    

class GivenNumNotesFitnessTest(NormalFitnessTest):
    '''
    Fitness test for musical score length and number of notes.
    Maximum reward is given to a piece with number of notes of expected values.
    '''
    name = 'NumNotes'
    
    def run(self, model):
        return self.normalValueOf(model.numNotes())
    
    

class EntropyFitnessTest(NormalFitnessTest):
    '''
    Fitness test for entropy.
    '''
    name = 'Entropy'
    
    def run(self, model):
        return self.normalValueOf(entropyModel(model))