'''
Model objects for genetic algorithms.

@author: Csaba Sulyok
'''
from numpy import float32, array, append, delete, zeros, arange
from numpy import uint8

from emc.cpp.swig.emcpp import realignImportances
from tymed import tymedCls, tymed


class Population(object):
    '''
    Denotes a general population object.
    Contains lists of genotypes, phenotypes and grades
    '''
    
    numUnits = 0
    numTests = 0
    
    def __init__(self, numUnits, numTests):
        self.numUnits = numUnits
        self.numTests = numTests
        self.genotypes = zeros(numUnits, dtype=object)
        self.phenotypes = zeros(numUnits, dtype=object)
        self.grades = zeros(numUnits, dtype=float32)
        self.gradesPerTest = zeros((numUnits, numTests), dtype=float32)
        self.ages = zeros(numUnits, dtype=uint8)
        
        
    def survive(self, oldPopulation, survivors):
        '''
        Persist entities from an old population over to this one.
        They will be inserted as the first units.
        '''
        for newIdx, oldIdx in enumerate(survivors):
            self.genotypes[newIdx] = oldPopulation.genotypes[oldIdx]
            self.ages[newIdx] = oldPopulation.ages[oldIdx] + 1
            



@tymedCls
class PopulationBreeder(object):
    '''
    Class which performs the procedures of the genotype breeder
    on entire populations.
    '''
    numUnits = 0
    numTests = 0
    importances = 0
    
    maxAge = 3
    
    genotypeBreeder = None
    genotypeSelector = None
    
    
    def createGenerationZero(self):
        '''
        Creates generation zero of genotypes based on the preset genotypeBreeder
        '''
        population = Population(self.numUnits, self.numTests)
        
        for genotypeIndex in range(self.numUnits):
            population.genotypes[genotypeIndex] = self.genotypeBreeder.createGenerationZeroGenotype()
            
        return population
            
    
    @tymed
    def breedNewGeneration(self, oldPopulation):
        '''
        Breeds a new generation from a previous one. Chooses parents and survivors
        using the genotype selector, and performs breeding/mutation using the genotype breeder.
        '''
        newPopulation = Population(self.numUnits, self.numTests)
        
        # choose indices for survivors and parents
        (survivors, survivorCount, parents, parentCount
            ) = self.genotypeSelector.chooseUnits(oldPopulation, self.importances, self.maxAge)
        # survive chosen units to new population
        newPopulation.survive(oldPopulation, survivors)
        
        for unitIndex in arange(parentCount):
            # select parent genotypes
            mother = oldPopulation.genotypes[parents[0, unitIndex]]
            father = oldPopulation.genotypes[parents[1, unitIndex]]
            # crossover & mutation
            offspring1, offspring2 = self.genotypeBreeder.breed(mother, father)
            self.genotypeBreeder.mutate(offspring1)
            self.genotypeBreeder.mutate(offspring2)
            # assign genotypes to new generation
            newPopulation.genotypes[survivorCount + 2 * unitIndex] = offspring1
            newPopulation.genotypes[survivorCount + 2 * unitIndex + 1] = offspring2
            
        return newPopulation
    

@tymedCls
class PhenotypeRenderer(object):
    '''
    Abstraction of a phenotype renderer, which takes genotype(s)
    and produces the corresponding phenotype(s).
    '''
    
    @tymed
    def runOnPopulation(self, population):
        '''
        Runs the phenotype renderer to produce phenotypes for each genotype
        in a given population.
        '''
        for phenotypeIndex in range(population.numUnits):
            # create new phenotype
            newPhenotype = self.run(population.genotypes[phenotypeIndex])
            # assign to same index in population
            population.phenotypes[phenotypeIndex] = newPhenotype
            
        return population



class FitnessTestContainer(object):
    '''
    Container class for fitness tests.
    Should contain a collection of FitnessTest objects, and their mapping to
    importance values settled from 0 to 1.
    '''
    
    '''
    Flag to represent whether or not this container
    can be extended after first construction.
    Specific implementations can set it to False.
    '''
    final = False
    
    
    def __init__(self, alpha = 0.0):
        '''
        Initialize properties
        '''
        self.numTests = 0
        self.tests = array([], dtype=object)
        self.importances = array([], dtype=float32)
        self.alpha = alpha
        
        
    def add(self, test, importance):
        '''
        Add new fitness test with proportional importance
        '''
        self.tests = append(self.tests, test)
        self.importances = append(self.importances, float32(importance))
        self.numTests += 1
    
    
    def remove(self, index):
        '''
        Removes a fitness test by index
        '''
        if index in range(self.numTests):
            self.tests = delete(self.tests, index)
            self.importances = delete(self.importances, index)
            self.numTests -= 1
    
    
    def names(self):
        '''
        Get list of fitness test names.
        '''
        return [test.name for test in self.tests]
    
        
    def normalize(self):
        '''
        Recalculates importances of fitness test container
        to be summed to 1
        '''
        if sum(self.importances) != 0:
            self.importances /= sum(self.importances)
        else:
            self.importances[:] = 1.0 / self.numTests


    def runOnPopulation(self, population):
        '''
        Run all fitness tests on a population, and returns changed population.
        '''
        for unitInd in range(population.numUnits):
            for testInd in range(self.numTests):
                population.gradesPerTest[unitInd][testInd] = self.tests[testInd].run(population.phenotypes[unitInd])
            population.grades[unitInd] = sum(population.gradesPerTest[unitInd] * self.importances)
            
        return population
    
    
    def realignImportances(self, population):
        '''
        Recalculate importances based on how good the population is doing.
        Uses the factor alpha
        '''
        realignImportances(self.importances, population.gradesPerTest, self.alpha)
    
    
    def __str__(self):
        '''
        String representation of fitness test container. Lists names, types and importances.
        '''
        ret = 'fitnessTestContainer{\n'
        for testInd, test in enumerate(self.tests):
            ret += '  name=%s, type=%s, imp=%.2f\n' %(test.name, test.__class__.__name__, self.importances[testInd])
        ret += '}'
        return ret