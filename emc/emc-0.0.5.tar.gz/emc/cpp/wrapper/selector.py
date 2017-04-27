from emc.cpp.swig.emcpp import ComplementaryGenotypeSelector


class ComplementaryGenotypeSelectorWrapper(object):

    def __init__(self, numUnits, numTests, minProb = .25, survivalProb = .1):
        self.numUnits = numUnits
        self.numTests = numTests
        self.minProb = minProb
        self.survivalProb = survivalProb
        
        self.native = ComplementaryGenotypeSelector(self.numUnits, self.numTests, self.minProb, self.survivalProb)
    
    
    def setNumUnits(self, numUnits):
        self.numUnits = numUnits
        self.native = ComplementaryGenotypeSelector(self.numUnits, self.numTests, self.minProb, self.survivalProb)
        
        
    def chooseUnits(self, population, importances, maxAge):
        (survivorCount, units) = self.native.chooseUnits(population.gradesPerTest,
                                                         population.grades,
                                                         population.ages,
                                                         importances, self.numUnits, maxAge)
        survivors = units[:survivorCount]
        parents = units[survivorCount:]
        parentCount = len(parents) / 2
        parents.shape = (2, parentCount)
        return (survivors, survivorCount, parents, parentCount)
    
    
    def __getstate__(self):
        return (self.numUnits, self.numTests, self.minProb, self.survivalProb)


    def __setstate__(self, state):
        (self.numUnits, self.numTests, self.minProb, self.survivalProb) = state
        self.native = ComplementaryGenotypeSelector(self.numUnits, self.numTests, self.minProb, self.survivalProb)
