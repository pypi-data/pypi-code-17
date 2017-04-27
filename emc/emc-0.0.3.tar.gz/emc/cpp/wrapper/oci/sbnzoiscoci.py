'''
WARNING
=======
This is a generated file that can be overwritten with regeneration.
It is a wrapper for the C++ op-code interpreter for the state machine SbnzOisc.
'''

from collections import OrderedDict
from numpy import float32

from emc.cpp.swig.emcpp import SbnzOiscOci


class SbnzOiscOciWrapper(object):
    '''
    Wrapper for C++ op-code interpreter SbnzOisc
    Description: One-instruction set computer (OISC) using SBNZ and the von Neumann architecture
    '''
    
    categoryCommands = OrderedDict([ 
      ('default', 256)
    ])
    
    
    def __init__(self, memSizeInBytes, expectedOutputs, haltAllowed = False, maxCommandsRatio = 2.0):
        self.memSizeInBytes = memSizeInBytes
        
        self.ramSize = self.memSizeInBytes / (2 * 1) # unitsize=2,numMems=1
        
        self.expectedOutputs = expectedOutputs
        self.haltAllowed = haltAllowed
        self.maxCommandsRatio = maxCommandsRatio
        
        inversePOutput = 1.0 / 0.5
        self.maxCommands = int(float32(expectedOutputs) * maxCommandsRatio * inversePOutput)
        
        self.native = SbnzOiscOci(self.ramSize, self.maxCommands, self.expectedOutputs, self.haltAllowed)
        
    
    def geneticStringToOutput(self, data):
        self.native.setFromGeneticString(data)
        self.native.interpret()
        return self.output()
    
    
    def geneticStringToOccurrences(self, data):
        self.setCountOccurrences(True)
        self.native.setFromGeneticString(data)
        self.native.interpret()
        return self.occurrences()
    
    
    def geneticStringToTouched(self, data):
        self.setCountTouched(True)
        self.native.setFromGeneticString(data)
        self.native.interpret()
        return (self.numTouched(), self.touched())
    
    
    @property
    def geneticStringSize(self): return self.native.geneticStringSize()
    
    def counter(self): return self.native.counter()
    def setCounter(self, counter): self.native.setCounter(counter)
    def outputPtr(self): return self.native.outputPtr()
    def setOutputPtr(self, outputPtr): self.native.setOutputPtr(outputPtr)
    

    def output(self): return self.native.output(self.outputPtr())
    def outputAt(self, index): return self.native.outputAt(index)
    def setOutput(self, output): self.native.setOutput(output)
    def setOutputAt(self, index, value): self.native.setOutputAt(index, value)
    
    def ram(self): return self.native.ram(self.ramSize)
    def ramAt(self, index): return self.native.ramAt(index)
    def setRam(self, ram): self.native.setRam(ram)
    def setRamAt(self, index, value): self.native.setRamAt(index, value)
    
    def debug(self): return self.native.debug()
    def setDebug(self, debug): self.native.setDebug(debug)
    def countOccurrences(self): return self.native.countOccurrences()
    def setCountOccurrences(self, countOccurrences): self.native.setCountOccurrences(countOccurrences)
    def countTouched(self): return self.native.countTouched()
    def setCountTouched(self, countTouched): self.native.setCountTouched(countTouched)
    def numTouched(self): return self.native.numTouched()
    def setNumTouched(self, numTouched): self.native.setNumTouched(numTouched)
    
    def occurrences(self): return self.native.occurrences(1)
    def occurrencesAt(self, index): return self.native.occurrencesAt(index)
    def setOccurrences(self, occurrences): self.native.setOccurrences(occurrences)
    def setOccurrencesAt(self, index, value): self.native.setOccurrencesAt(index, value)
    
    def touched(self): return self.native.touched(self.ramSize)
    def touchedAt(self, index): return self.native.touchedAt(index)
    def setTouched(self, occurrences): self.native.setTouched(occurrences)
    def setTouchedAt(self, index, value): self.native.setTouchedAt(index, value)
    
    
    def __getstate__(self):
        return (self.memSizeInBytes, self.ramSize, self.expectedOutputs, self.haltAllowed, self.maxCommandsRatio, self.maxCommands)
    
    
    def __setstate__(self, state):
        self.memSizeInBytes, self.ramSize, self.expectedOutputs, self.haltAllowed, self.maxCommandsRatio, self.maxCommands = state
        self.native = SbnzOiscOci(self.ramSize, self.maxCommands, self.expectedOutputs, self.haltAllowed)
        