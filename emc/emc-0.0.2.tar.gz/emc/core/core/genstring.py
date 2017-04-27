'''
EMC-specific genotype related model objects.

@author: Csaba Sulyok
'''

from numpy import uint8, frombuffer, zeros

from emc.cpp.swig.emcpp import randomByteArray, combineByteArray, mutateBytesInByteArray
from tymed import tymedCls, tymed


class GeneticString(object):
    '''
    EMC representation of a genetic string - the initial condition of the Virtual Machine.
    This also represents the genotype for the genetic algorithm.
    '''
    
    def __init__(self, data):
        '''
        Initialize by data, which should be a numpy byte(uint8) array.
        '''
        self.data = data
    
    
    def __getstate__(self):
        '''
        Overwrite serialization because cPickle saves extra information making the output files very large.
        '''
        return bytearray(self.data)


    def __setstate__(self, state):
        '''
        Overwrite serialization because cPickle saves extra information making the output files very large.
        '''
        self.data = frombuffer(state, dtype=uint8)




@tymedCls
class GeneticStringBreeder(object):
    '''
    Logic to create, breed and mutate the EMC genetic string.
    Acts as a wrapper to the C++ library bytestream.
    '''
    
    def __init__(self, geneticStringSize, maxCutPointsRatio = 0.05, maxMutatedBytesRatio = 0.05):
        self.geneticStringSize = geneticStringSize
        self.maxCutPoints = int(self.geneticStringSize * maxCutPointsRatio) 
        self.maxMutatedBytes = int(self.geneticStringSize * maxMutatedBytesRatio)
        
    
    @tymed
    def createGenerationZeroGenotype(self):
        '''
        Returns a random byte stream with size as the configured genetic string size.
        Done through C++ library.
        '''
        data = randomByteArray(self.geneticStringSize)
        return GeneticString(data = data)
    
    
    @tymed
    def breed(self, mother, father):
        '''
        Recombines two genetic strings by generating random cut points,
        taking successive parts from mother and father, and creating 2 new children.
        Done through C++ library.
        '''
        child1data = zeros(self.geneticStringSize, dtype=uint8)
        child2data = zeros(self.geneticStringSize, dtype=uint8)
        
        combineByteArray(mother.data, father.data, child1data, child2data, self.maxCutPoints)
        
        return (GeneticString(data = child1data), GeneticString(data = child2data))
    
    
    @tymed
    def mutate(self, genotype):
        '''
        Mutates the genetic string by generating random indices whose bytes get
        inverted.
        Done through C++ library.
        '''
        mutateBytesInByteArray(genotype.data, self.maxMutatedBytes)


    def __getstate__(self):
        '''
        Do not serialize cut points, they are a helper construct.
        '''
        return (self.geneticStringSize, self.maxCutPoints, self.maxMutatedBytes)


    def __setstate__(self, state):
        '''
        Rebuild cut points when deserializing.
        '''
        (self.geneticStringSize, self.maxCutPoints, self.maxMutatedBytes) = state

