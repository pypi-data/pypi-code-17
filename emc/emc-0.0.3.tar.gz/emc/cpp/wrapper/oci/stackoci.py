'''
WARNING
=======
This is a generated file that can be overwritten with regeneration.
It is a wrapper for the C++ op-code interpreter for the state machine Stack.
'''

from collections import OrderedDict
from numpy import float32

from emc.cpp.swig.emcpp import StackOci


class StackOciWrapper(object):
    '''
    Wrapper for C++ op-code interpreter Stack
    Description: 
    '''
    
    categoryCommands = OrderedDict([ 
      ('default', 224),
      ('output', 32)
    ])
    
    
    def __init__(self, memSizeInBytes, expectedOutputs, haltAllowed = False, maxCommandsRatio = 2.0):
        self.memSizeInBytes = memSizeInBytes
        
        self.stackSize = self.memSizeInBytes / (2 * 1) # unitsize=2,numMems=1
        
        self.expectedOutputs = expectedOutputs
        self.haltAllowed = haltAllowed
        self.maxCommandsRatio = maxCommandsRatio
        
        inversePOutput = 256.0 / float32(self.categoryCommands['output'])
        self.maxCommands = int(float32(expectedOutputs) * maxCommandsRatio * inversePOutput)
        
        self.native = StackOci(self.stackSize, self.maxCommands, self.expectedOutputs, self.haltAllowed)
        
    
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
    def sp(self): return self.native.sp()
    def setSp(self, sp): self.native.setSp(sp)
    

    def output(self): return self.native.output(self.outputPtr())
    def outputAt(self, index): return self.native.outputAt(index)
    def setOutput(self, output): self.native.setOutput(output)
    def setOutputAt(self, index, value): self.native.setOutputAt(index, value)
    
    def stack(self): return self.native.stack(self.stackSize)
    def stackAt(self, index): return self.native.stackAt(index)
    def setStack(self, stack): self.native.setStack(stack)
    def setStackAt(self, index, value): self.native.setStackAt(index, value)
    
    def debug(self): return self.native.debug()
    def setDebug(self, debug): self.native.setDebug(debug)
    def countOccurrences(self): return self.native.countOccurrences()
    def setCountOccurrences(self, countOccurrences): self.native.setCountOccurrences(countOccurrences)
    def countTouched(self): return self.native.countTouched()
    def setCountTouched(self, countTouched): self.native.setCountTouched(countTouched)
    def numTouched(self): return self.native.numTouched()
    def setNumTouched(self, numTouched): self.native.setNumTouched(numTouched)
    
    def occurrences(self): return self.native.occurrences(2)
    def occurrencesAt(self, index): return self.native.occurrencesAt(index)
    def setOccurrences(self, occurrences): self.native.setOccurrences(occurrences)
    def setOccurrencesAt(self, index, value): self.native.setOccurrencesAt(index, value)
    
    def touched(self): return self.native.touched(self.stackSize)
    def touchedAt(self, index): return self.native.touchedAt(index)
    def setTouched(self, occurrences): self.native.setTouched(occurrences)
    def setTouchedAt(self, index, value): self.native.setTouchedAt(index, value)
    
    
    def __getstate__(self):
        return (self.memSizeInBytes, self.stackSize, self.expectedOutputs, self.haltAllowed, self.maxCommandsRatio, self.maxCommands)
    
    
    def __setstate__(self, state):
        self.memSizeInBytes, self.stackSize, self.expectedOutputs, self.haltAllowed, self.maxCommandsRatio, self.maxCommands = state
        self.native = StackOci(self.stackSize, self.maxCommands, self.expectedOutputs, self.haltAllowed)
        