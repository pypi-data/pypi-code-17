'''
Wrapper for the C++ model builder library
@author Csaba Sulyok
'''

from emc.cpp.swig.emcpp import ModelBuilder
from tymed import tymedCls, tymed


@tymedCls
class ModelBuilderWrapper(object):
    '''
    Wrapper for C++ model builder module.
    Takes byte array, feeds it to builder,
    and populates an instance of Model with its results.
    '''
    
    propsPerNote = 6
    
    def __init__(self, ticksPerQuarterNote = 4, quarterNotesPerMinute = 120, 
                 numTracks = 4, 
                 restsEnabled = False, velocityEnabled = False,
                 omitZeroDurations = True, omitZeroPitches = True, omitZeroVelocities = True,
                 ioiMask = 0xFF, durationMask = 0xFF, pitchMask = 0x7F, velocityMask = 0x7F,
                 debug = False):
        self.ticksPerQuarterNote = ticksPerQuarterNote
        self.quarterNotesPerMinute = quarterNotesPerMinute
        self.numTracks = numTracks
        
        self.restsEnabled = restsEnabled
        self.velocityEnabled = velocityEnabled
        self.omitZeroDurations = omitZeroDurations
        self.omitZeroPitches = omitZeroPitches
        self.omitZeroVelocities = omitZeroVelocities
        self.ioiMask = ioiMask
        self.durationMask = durationMask
        self.pitchMask = pitchMask
        self.velocityMask = velocityMask
        self.debug = debug

        self.native = ModelBuilder(self.numTracks, self.restsEnabled, self.velocityEnabled,
                                   self.omitZeroDurations, self.omitZeroPitches, self.omitZeroVelocities,
                                   self.ioiMask, self.durationMask, self.pitchMask, self.velocityMask,
                                   self.debug)
        
    
    @tymed
    def bytesToModel(self, modelClass, bytes):
        self.native.addNotesFromBytes(bytes)
        
        model = modelClass(self.ticksPerQuarterNote, self.numTracks)
        model.length = self.native.length()
        
        for trackIdx in range(self.numTracks):
            numNotes = self.native.numNotes(trackIdx)
            model.tracks[trackIdx].length = self.native.length(trackIdx)
            model.tracks[trackIdx].notes = self.native.notes(numNotes * self.propsPerNote, trackIdx)
            model.tracks[trackIdx].notes.shape = (numNotes, self.propsPerNote)
            
        self.native.clear()
        return model
    
    
    def setDebug(self, debug):
        self.native.setDebug(debug)
        
    
    def bytesPerNote(self):
        return self.native.bytesPerNote()
    
    
    def __getstate__(self):
        '''
        Overwrite getstate, since pickling fails if
        native model builder is included, because it is a c++ proxy.
        '''
        return (self.ticksPerQuarterNote, self.quarterNotesPerMinute, self.numTracks, 
                self.restsEnabled, self.velocityEnabled,
                self.omitZeroDurations, self.omitZeroPitches, self.omitZeroVelocities,
                self.ioiMask, self.durationMask, self.pitchMask, self.velocityMask,
                self.debug)


    def __setstate__(self, state):
        '''
        Overwrite setstate, since pickling fails if
        native model builder is included, because it is a c++ proxy.
        '''
        self.ticksPerQuarterNote, self.quarterNotesPerMinute, self.numTracks,\
            self.restsEnabled, self.velocityEnabled,\
            self.omitZeroDurations, self.omitZeroPitches, self.omitZeroVelocities,\
            self.ioiMask, self.durationMask, self.pitchMask, self.velocityMask,\
            self.debug = state
            
        self.native = ModelBuilder(self.numTracks, self.restsEnabled, self.velocityEnabled,
                                   self.omitZeroDurations, self.omitZeroPitches, self.omitZeroVelocities,\
                                   self.ioiMask, self.durationMask, self.pitchMask, self.velocityMask,
                                   self.debug)
