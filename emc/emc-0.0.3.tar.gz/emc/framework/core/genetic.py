'''
Container for genetic algorithm runner.
Configurable instances of all configurations, population number and generation number
may come from a config file configuring the instance for the class below.
@author: Csaba Sulyok
'''
import time
from time import sleep

from numpy import copy, arange, min, max, mean

from emc.helper.git import gitRevision, verifyGitRevision
from monitoring.monitor import monitorState
from emc.helper.serializeutils import toFile
from emc.framework.core.model import Population
from tymed import lap


class MonitorableData(object):
    '''
    Small internal class which should be exposed to external
    processes monitoring this genetic algorithm.
    Can be extended.
    '''
    def __init__(self):
        self.generation = 0
        self.running = False
    
    def __repr__(self):
        return str(self.__dict__)
        
        
        
class GeneticAlgorithm(object):
    '''
    Class for running a genetic algorithm based on configurable breeders, renderers,
    genotypes, phenotypes etc.
    '''
    
    def __init__(self, data = MonitorableData(),
                       populationBreeder = None,
                       phenotypeRenderer = None,
                       fitnessTestContainer = None,
                       realignImportancesCycle = 100,
                       targetGeneration = 20000,
                       numberOfRuns = 5,
                       loggingCycle = 10,
                       saving = None):
        '''
        Build algorithm before first run.
        For building from previous runs, see __getstate__ and __setstate__
        '''
        self.data = data
        self.populationBreeder = populationBreeder
        self.phenotypeRenderer = phenotypeRenderer
        self.fitnessTestContainer = fitnessTestContainer
        self.realignImportancesCycle = realignImportancesCycle
        self.targetGeneration = targetGeneration
        self.numberOfRuns = numberOfRuns
        self.loggingCycle = loggingCycle
        self.saving = saving
        
        self.population = None
        
        self.usedGitRevision = gitRevision()
    
    
    def __getstate__(self):
        '''
        Serialization
        '''
        return (self.data,
                self.populationBreeder,
                self.phenotypeRenderer,
                self.fitnessTestContainer,
                self.realignImportancesCycle,
                self.targetGeneration,
                self.numberOfRuns,
                self.loggingCycle,
                self.saving,
                self.population,
                self.usedGitRevision)
    
    
    def __setstate__(self, state):
        '''
        Serialization
        '''
        self.data, self.populationBreeder, self.phenotypeRenderer, self.fitnessTestContainer,\
            self.realignImportancesCycle, self.targetGeneration,\
            self.numberOfRuns, self.loggingCycle, self.saving,\
            self.population, self.usedGitRevision = state
        
        # verify git revision is the same as current
        verifyGitRevision(self.usedGitRevision)
    
    
    def save(self, fileName):
        '''
        Save current state of algorithm to file
        '''
        toFile(self, fileName)
        
    
    def performFull(self):
        '''
        Perform full algorithm, using set target generation
        and number of runs.
        '''
        self.data.running = True
        initialImportances = copy(self.fitnessTestContainer.importances)
        
        for _ in arange(self.numberOfRuns):
            self._performForGenerations(self.targetGeneration)
            self.reset(initialImportances)
        
        
    def performUntilGeneration(self, generationCount):
        '''
        Main method for performing the genetic algorithm for until a given number of generations is reached.
        '''
        while self.data.generation < generationCount:
            self._performForNextGeneration()
        self.saving.finishRun()
    
    
    def performUntilSignalled(self):
        '''
        Main method for performing the genetic algorithm for until externally stopped.
        '''
        self.data.running = True
        while not monitorState['exitRequested']:
            if monitorState['pauseRequested']:
                self.data.running = False
                sleep(1)
            else:
                self.data.running = True
                self._performForNextGeneration()
        self.saving.finishRun()
    
    
    def _performForGenerations(self, generationCount):
        '''
        Main method for performing the genetic algorithm for a given number of generations.
        '''
        target = self.data.generation + generationCount
        while self.data.generation < target:
            self._performForNextGeneration()
        self.saving.finishRun()
        
        
    def _performForNextGeneration(self):
        '''
        Perform next generation. If first, do generation zero,
        if not, do normal generation.
        '''
        if self.data.generation == 0:
            self._performForGenerationZero()
        else:
            self._performForOneGeneration()
  
    
    
    def _performForGenerationZero(self):
        '''
        Method for creating and evaluating generation zero
        '''
        startTime = time.time()
        
        self.saving.init(self, self.usedGitRevision, self.populationBreeder.numUnits, self.fitnessTestContainer.numTests)
        self.populationBreeder.numTests = self.fitnessTestContainer.numTests
        self.populationBreeder.importances = self.fitnessTestContainer.importances
        
        self.population = Population(self.populationBreeder.numUnits, self.populationBreeder.numTests)
        
        for unitIdx in range(self.population.numUnits):
            self.population.genotypes[unitIdx] = self.populationBreeder.genotypeBreeder.createGenerationZeroGenotype()
            self.population.phenotypes[unitIdx] = self.phenotypeRenderer.run(self.population.genotypes[unitIdx])
            self.population.grades[unitIdx] = self.fitnessTestContainer.runOnModelGivenGrades(self.population.phenotypes[unitIdx], self.population.gradesPerTest[unitIdx])
        
        endTime = time.time()
        self.saving.afterGeneration()
        
        
        print "Generation %d" %(self.data.generation)
        print "Grades: Min/Mean/Max: %.3f, %.3f, %.3f" %(min(self.population.grades),
                         mean(self.population.grades), max(self.population.grades))
        print "Time:   G/Ph/F/Total: %.3f, %.3f, %.3f, %.3f\n" %(lap(self.populationBreeder.genotypeBreeder.createGenerationZeroGenotype),
                                                                 lap(self.phenotypeRenderer.run),
                                                                 lap(self.fitnessTestContainer.runOnModelGivenGrades),
                                                                 endTime - startTime)
        
        
        self.data.generation += 1
        return self.population
        
    
    
    def _performForOneGeneration(self):
        '''
        Method for breeding and evaluating a generation
        '''
        
        if self.saving.algorithm is None:
            self.saving.init(self, self.usedGitRevision, self.populationBreeder.numUnits, self.fitnessTestContainer.numTests)
        
        if self.data.generation % self.realignImportancesCycle == 0:
            self.fitnessTestContainer.realignImportances(self.population)
            self.populationBreeder.importances = self.fitnessTestContainer.importances
            # print "New importances: %s" %array_str(self.fitnessTestContainer.importances)
            
            
        startTime = time.time()
        
        self.population = self.populationBreeder.breedNewGeneration(self.population)
        for unitIdx in range(self.population.numUnits):
            self.population.phenotypes[unitIdx] = self.phenotypeRenderer.run(self.population.genotypes[unitIdx])
            self.population.grades[unitIdx] = self.fitnessTestContainer.runOnModelGivenGrades(self.population.phenotypes[unitIdx], self.population.gradesPerTest[unitIdx])
            
        endTime = time.time()
        
        self.saving.afterGeneration()
        

        if self.data.generation % self.loggingCycle == 0:
            print "Generation %d" %self.data.generation
            print "Output: %s" %self.saving.outputDir
            print "Grades: Min/Mean/Max: %.3f, %.3f, %.3f" %(min(self.population.grades),
                             mean(self.population.grades), max(self.population.grades))
            print "Time:   G/Ph/F/Total: %.3f, %.3f, %.3f, %.3f\n" %(lap(self.populationBreeder.breedNewGeneration),
                                                                     lap(self.phenotypeRenderer.run),
                                                                     lap(self.fitnessTestContainer.runOnModelGivenGrades),
                                                                     endTime - startTime)

        
        self.data.generation += 1
        return self.population
    
    
    def reset(self, importances):
        '''
        Reset state of algorithm.
        Retains all builders and renderers, but resets generation to 0, and flushes any remaining data.
        '''
        self.saving.finishRun()
        self.data.generation = 0
        self.fitnessTestContainer.importances = copy(importances)
        self.saving.reset()