'''
Fitness tests related to a MIDI corpus.
From MIDI files, a Model directory is built up,
and all properties and diffs are compared.

@author: Csaba Sulyok
'''
from numpy import zeros, mean, sum, std, float32, frombuffer, uint32, array,\
    copy

from emc.core.fitness.normal import GivenLengthFitnessTest, GivenNumNotesFitnessTest,\
    EntropyFitnessTest
from emc.cpp.wrapper.descriptor import DescriptorDirectoryWrapper, numDescriptors
from emc.framework.core.model import FitnessTestContainer
from tymed import tymedCls, tymed


@tymedCls
class CorpusBasedFitnessTestContainer(FitnessTestContainer):
    '''
    Fitness test container which contains tests based on a corpus and the histogram descriptor
    built from it.
    '''
    
    '''
    This container cannot be changed after initial construction.
    '''
    final = True
    
    '''
    Number of tests is fixed.
    '''
    numTests = numDescriptors + 3
    
    '''
    Default value for importances
    '''
    defaultImportances = array([8,1,8,
                                8,2,3,1,
                                3,2,1,1,
                                15,6,6,1], dtype=float32)
    
    
    def __init__(self, modelDir, alpha = 0.0, 
                 numBins = 128, fourierSize = 2048, numClusters = 1, gamma = 1.0,
                 importances = None, expectedLength = None):
        '''
        Initialize by props necessary for descriptor directory.
        Also configure given length and numNotes tests from model directory.
        '''
        
        self.alpha = alpha
        
        self.dd = DescriptorDirectoryWrapper(modelDir, numBins, fourierSize, numClusters, gamma)
        if importances is None:
            self.importances = copy(self.defaultImportances)
        else:
            self.importances = copy(importances)
        self.normalize()
            
        if expectedLength is None:
            lengthRatio = 1.0
        else:
            # times 8 because there are 8 ticks per second and expectedLength is in seconds
            lengthRatio = 8.0 * expectedLength / float32(mean(modelDir.lengths()))
        
        self.expectedNumNotes = uint32(lengthRatio * float32(sum(mean(modelDir.numNotes(), axis=0))))
        
        self.glft = GivenLengthFitnessTest   (mu  = [lengthRatio * mean(modelDir.lengths())],
                                              sig = [lengthRatio * std (modelDir.lengths())])
        self.gnnft = GivenNumNotesFitnessTest(mu  =  lengthRatio * mean(modelDir.numNotes(), axis=0),
                                              sig =  lengthRatio * std (modelDir.numNotes(), axis=0))
        self.eft = EntropyFitnessTest        (mu  =  mean(modelDir.entropies(), axis=0),
                                              sig =  std (modelDir.entropies(), axis=0))
        
    
    def names(self):
        '''
        Get list of fitness test names.
        '''
        return [self.glft.name,  self.gnnft.name,     self.eft.name,
                'IOI hist',      'IOI diffHist',      'IOI Fft',          'IOI diffFft',
                'Duration hist', 'Duration diffHist', 'Duration Fourier', 'Duration diffFft',
                'Pitch hist',    'Pitch diffHist',    'Pitch Fourier',    'Pitch diffFft']
                #'Vel hist',      'Vel diffHist',      'Vel Fourier',      'Vel diffFft']
    
    
    @tymed
    def runOnModel(self, model):
        grades = zeros(self.numTests, dtype=float32)
        grades[0] = self.glft.run(model)
        grades[1] = self.gnnft.run(model)
        grades[2] = self.eft.run(model)
        grades[3:] = mean(self.dd.modelFitness(model), axis = 0)
        overallGrades = sum(grades * self.importances)
        return (grades, overallGrades)
    
    
    @tymed
    def runOnModelGivenGrades(self, model, gradesPerTest):
        gradesPerTest[0] = self.glft.run(model)
        gradesPerTest[1] = self.gnnft.run(model)
        gradesPerTest[2] = self.eft.run(model)
        gradesPerTest[3:] = mean(self.dd.modelFitness(model), axis = 0)
        grade = sum(gradesPerTest * self.importances)
        return grade
    
    
    @tymed    
    def runOnPopulation(self, pop):
        '''
        Run all fitness tests on a population.
        First tests are for given length, and number of notes,
        rest are histogram windowed results.
        '''
        
        for unitInd in range(pop.numUnits):
            model = pop.phenotypes[unitInd]
            pop.gradesPerTest[unitInd][0] = self.glft.run(model)
            pop.gradesPerTest[unitInd][1] = self.gnnft.run(model)
            pop.gradesPerTest[unitInd][2] = self.eft.run(model)
            pop.gradesPerTest[unitInd][3:] = mean(self.dd.modelFitness(model), axis = 0)
            pop.grades[unitInd] = sum(pop.gradesPerTest[unitInd] * self.importances)
            
        return pop
    
    
    def __getstate__(self):
        '''
        Do not cache importances as numpy array.
        '''
        return (self.alpha, self.dd, self.glft, self.gnnft, self.eft, bytearray(self.importances.astype(float32)))
    
    
    def __setstate__(self, state):
        '''
        Do not cache importances as numpy array.
        '''
        self.alpha, self.dd, self.glft, self.gnnft, self.eft, importancesBA = state
        self.importances = frombuffer(importancesBA, dtype=float32)
