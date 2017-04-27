'''
Model directory

@author: Csaba Sulyok
'''
import os

from numpy import array, append, zeros, size, unique, uint16, float32

from emc.core.core.model import Model
from emc.core.integ.midi import readFromMidi, writeToMidi
from emc.helper.entropy import entropyModel


class ModelDirectory(object):
    '''
    Collection of model instances to be used in analysis/transformation.
    Built with a folder name containing MIDI files which will all be read and transformed into Model instances.
    Transformations can be performed and resulting models will be written back to same files
    '''
    
    def __init__(self, midiFolder ='.'):
        '''
        Initialize by foldername.
        '''
        self.folder = os.path.abspath(midiFolder)
        self.read(self.folder)
    
    
    
    def read(self, newMidiFolder = None):
        '''
        Reads model directory by reading all MIDI files from given folder and transforming them to instances of Model.
        '''
        if newMidiFolder is None:
            newMidiFolder = self.folder
            
        self.filenames = array([])
        for fname in os.listdir(self.folder):
            if fname.endswith(".mid"):
                self.filenames = append(self.filenames, fname)
        self.numModels = len(self.filenames)
        self.models = zeros(self.numModels, dtype=Model)
        for i, fname in enumerate(self.filenames):
            self.models[i] = readFromMidi("%s/%s" %(self.folder, fname))
        
        if size(unique(array([m.numTracks for m in self.models]))) != 1:
            print "ERROR: Model directory '%s' contains MIDIs with different number of tracks. Behavior unpredictable" %self.folder
        self.numTracks = self.models[0].numTracks
    
    
    
    def write(self, newMidiFolder = None, includeEmptyTracks = True):
        '''
        Writes model directory as MIDI to new output folder.
        '''
        if newMidiFolder is None:
            newMidiFolder = self.folder
            
        self.folder = os.path.abspath(newMidiFolder)
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        
        for i, fname in enumerate(self.filenames):
            writeToMidi(self.models[i], "%s/%s" %(self.folder, fname), includeEmptyTracks)



    def lengths(self):
        '''
        List of all lengths in models.
        '''
        ret = zeros(self.numModels)
        for modelIdx, model in enumerate(self.models):
            ret[modelIdx] = model.length
        return ret
    
    
    def numNotes(self):
        '''
        List of number of notes in models.
        '''
        ret = zeros((self.numModels, self.numTracks), dtype=uint16)
        for modelIdx, model in enumerate(self.models):
            ret[modelIdx, :] = model.numNotes()
        return ret
    
    
    def entropies(self):
        '''
        Entropy of all models in dir.
        '''
        ret = zeros((self.numModels, self.numTracks * 3), dtype=float32)
        for modelIdx, model in enumerate(self.models):
            ret[modelIdx, :] = entropyModel(model)
        return ret
    
    
    def __getstate__(self):
        '''
        Do not serialize cached values.
        '''
        return os.path.relpath(self.folder)



    def __setstate__(self, state):
        '''
        Rebuild cached values when deserializing.
        '''
        self.folder = os.path.abspath(state)
        self.read(self.folder)