'''
WARNING
=======
This is a generated file that can be overwritten with regeneration.
It is a wrapper for the C++ op-code interpreter for the state machine ImmediateHarvard.
'''

from collections import OrderedDict
from numpy import float32

from emc.cpp.swig.emcpp import ImmediateHarvardOci


class ImmediateHarvardOciWrapper(object):
    '''
    Wrapper for C++ op-code interpreter ImmediateHarvard
    Description: OCI with immediate addressing (parameters of instructions in subsequent byte(s))
    '''
    
    categoryCommands = OrderedDict([ 
      ('transfer', 110),
      ('arithmetic', 86),
      ('machine', 7),
      ('branching', 21),
      ('output', 32)
    ])
    
    
    def __init__(self, memSizeInBytes, expectedOutputs, haltAllowed = False, maxCommandsRatio = 2.0):
        self.memSizeInBytes = memSizeInBytes
        
        self.ramSize = self.memSizeInBytes / (1 * 2) # unitsize=1,numMems=2
        self.romSize = self.memSizeInBytes / (1 * 2) # unitsize=1,numMems=2
        
        self.expectedOutputs = expectedOutputs
        self.haltAllowed = haltAllowed
        self.maxCommandsRatio = maxCommandsRatio
        
        inversePOutput = 256.0 / float32(self.categoryCommands['output'])
        self.maxCommands = int(float32(expectedOutputs) * maxCommandsRatio * inversePOutput)
        
        self.native = ImmediateHarvardOci(self.ramSize, self.romSize, self.maxCommands, self.expectedOutputs, self.haltAllowed)
        
    
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
    def acc(self): return self.native.acc()
    def setAcc(self, acc): self.native.setAcc(acc)
    def dataPtr(self): return self.native.dataPtr()
    def setDataPtr(self, dataPtr): self.native.setDataPtr(dataPtr)
    def flags(self): return self.native.flags()
    def setFlags(self, flags): self.native.setFlags(flags)
    def stackPtr(self): return self.native.stackPtr()
    def setStackPtr(self, stackPtr): self.native.setStackPtr(stackPtr)
    

    def output(self): return self.native.output(self.outputPtr())
    def outputAt(self, index): return self.native.outputAt(index)
    def setOutput(self, output): self.native.setOutput(output)
    def setOutputAt(self, index, value): self.native.setOutputAt(index, value)

    def registers(self): return self.native.registers(8)
    def register(self, index): return self.native.registerAt(index)
    def setRegisters(self, registers): self.native.setRegisters(registers)
    def setRegister(self, index, value): self.native.setRegister(index, value)
    
    def ram(self): return self.native.ram(self.ramSize)
    def ramAt(self, index): return self.native.ramAt(index)
    def setRam(self, ram): self.native.setRam(ram)
    def setRamAt(self, index, value): self.native.setRamAt(index, value)
    
    def rom(self): return self.native.rom(self.romSize)
    def romAt(self, index): return self.native.romAt(index)
    def setRom(self, rom): self.native.setRom(rom)
    def setRomAt(self, index, value): self.native.setRomAt(index, value)
    
    def stack(self): return self.native.stack(256)
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
    
    def occurrences(self): return self.native.occurrences(5)
    def occurrencesAt(self, index): return self.native.occurrencesAt(index)
    def setOccurrences(self, occurrences): self.native.setOccurrences(occurrences)
    def setOccurrencesAt(self, index, value): self.native.setOccurrencesAt(index, value)
    
    def touched(self): return self.native.touched(self.romSize)
    def touchedAt(self, index): return self.native.touchedAt(index)
    def setTouched(self, occurrences): self.native.setTouched(occurrences)
    def setTouchedAt(self, index, value): self.native.setTouchedAt(index, value)
    
    
    def __getstate__(self):
        return (self.memSizeInBytes, self.ramSize, self.romSize, self.expectedOutputs, self.haltAllowed, self.maxCommandsRatio, self.maxCommands)
    
    
    def __setstate__(self, state):
        self.memSizeInBytes, self.ramSize, self.romSize, self.expectedOutputs, self.haltAllowed, self.maxCommandsRatio, self.maxCommands = state
        self.native = ImmediateHarvardOci(self.ramSize, self.romSize, self.maxCommands, self.expectedOutputs, self.haltAllowed)
        