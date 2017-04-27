'''
Provides saving features for a genetic algorithm run.
Will be called after each generation.
Necessary since we do not wish to store all generations in memory. 

Provides an empty implementation (nothing is done to save state in-between generations).
Also provides an implementation where the individual fitness test results and the algorithm state are
saved after a certain generation count.
'''

import datetime
import sys
from os import makedirs
from os.path import exists
from time import time

from emc.helper.numpyba import NumpyArrayBA
from emc.helper.serializeutils import toFile


class GASaving(object):
    algorithm = None
    
    def __init__(self, cycleSize = 3, outputDir = 'output'):
        self.cycleSize = cycleSize
        self.outputDir = outputDir
    
    
    def init(self, algorithm, gitRevision, numUnits, numTests):
        print 'Initializing saving mechanism'
        self.algorithm = algorithm
        

    def afterGeneration(self):
        pass
    
    
    def finishRun(self):
        print 'Finishing run'
        
        
    def reset(self, importances):
        print 'Resetting saving mechanism'
    


        
    
class GASavingToFile(GASaving):
    '''
    File serializer for algorithm state.
    Saves algorithm and fitness test results after a given number of iterations.
    This way they do not need to stay in memory.
    '''

    
    def init(self, algorithm, gitRevision, numUnits, numTests):
        '''
        Initialize caching fitness test array.
        Will get flushed when full and restarted from the beginning.
        
        D1: generation index, D2: unit index, D3: fitness test index.
        '''
        print 'Initializing saving mechanism'
        self.algorithm = algorithm
        self.gitRevision = gitRevision
        self.allGrades = NumpyArrayBA((self.cycleSize, numUnits, numTests))
        self.timeStamp = datetime.datetime.fromtimestamp(time()).strftime('%Y%m%d-%H%M%S')
        self.ptr = 0
        
        if self.gitRevision:
            self.baseName = 'emc_time%s_rev%s' %(self.timeStamp, self.gitRevision)
        else:
            self.baseName = 'emc_time%s' %(self.timeStamp)
        
        
    
    def afterGeneration(self):
        '''
        Saves fitness test results to its array.
        If array full, will flush it.
        '''
        self.allGrades[self.ptr, :, :] = self.algorithm.population.gradesPerTest
        self.ptr = self.ptr + 1
        
        if self.ptr == self.cycleSize:
            self.flush(self.algorithm.data.generation)
        
    
    
    def finishRun(self):
        '''
        Flushes fitness test result array even if not full.
        Call with gen - 1, because this will be called after generation index already incremented.
        '''
        self.flush(self.algorithm.data.generation - 1)
    
    
    
    def flush(self, generation):
        '''
        Flushes fitness test array elements to file.
        Serializes algorithm state into another file.
        Goes up until write pointer of cache.
        Ignored if write pointer is at 0.
        '''
        if self.ptr is 0:
            return
        
        
        self.ensureSubDirExists('fitness')
        gradesFileName = "%s/%s/fitness/emc_fitness%05d-%05d.bin" %(self.outputDir, self.baseName,
                                                                  generation - self.ptr + 1, generation)
        try:
            toFile(self.allGrades[:self.ptr, :, :], gradesFileName)
        except SystemError as e:
            print "Weird system error", e, "when trying to save following to", gradesFileName, 'ptr=', self.ptr
            print self.allGrades[:self.ptr, :, :]
        except:
            print "Reeeally unexpected behavior:", sys.exc_info()[0], "when trying to save following to", gradesFileName, 'ptr=', self.ptr
            print self.allGrades[:self.ptr, :, :]
            
            
        
        self.ensureSubDirExists('alg')
        algFileName = "%s/%s/alg/emc_gen%05d.emc" %(self.outputDir, self.baseName, generation)
        toFile(self.algorithm, algFileName)
        
        self.ptr = 0
    
    
    
    def ensureSubDirExists(self, subdir):
        if not exists('%s/%s/%s' %(self.outputDir, self.baseName, subdir)):
            makedirs('%s/%s/%s' %(self.outputDir, self.baseName, subdir))
    
    
            
    def reset(self):
        '''
        Reset state of saving mechanism.
        Resets timestamp so it becomes a new run.
        '''
        self.timeStamp = datetime.datetime.fromtimestamp(time()).strftime('%Y%m%d-%H%M%S')
    
    
    
    def __getstate__(self):
        '''
        Do not serialize cache array.
        '''
        return (self.cycleSize, self.outputDir)
    
    
    
    def __setstate__(self, state):
        '''
        Recall only helper objects.
        '''
        self.cycleSize, self.outputDir = state