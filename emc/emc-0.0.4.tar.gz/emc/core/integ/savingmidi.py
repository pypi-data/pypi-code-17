'''
Extension to algorithm's file saver mechanism to also write out best model as MIDI.
'''

from numpy import argmax

from emc.core.integ.midi import writeToMidi
from emc.framework.saving import GASavingToFile


class GASavingMidiToFile(GASavingToFile):
    
    
    def flush(self, generation):
        '''
        Flushes as parent would + exports best MIDI file from current generation.
        '''
        if self.ptr is 0:
            return
        
        super(GASavingMidiToFile, self).flush(generation)
        
        bestModelIdx = argmax(self.algorithm.population.grades)
        bestModel = self.algorithm.population.phenotypes[bestModelIdx]
        bestModelGrade = self.algorithm.population.grades[bestModelIdx]
        
        self.ensureSubDirExists('midi')
        midiFileName = "%s/%s/midi/emc_score%.3f_gen%05d.mid" %(self.outputDir, self.baseName, 
                                                                 bestModelGrade, generation)
        writeToMidi(bestModel, midiFileName)
        
        self.ptr = 0