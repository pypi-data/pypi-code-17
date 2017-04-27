'''
Model-related classes in EMC.
@author Csaba Sulyok
'''

from numpy import frombuffer, zeros, array, uint16, append


class Track(object):
    '''
    Class representation of a track, i.e. a collection of notes related to a virtual
    instrument/voice.
    '''
    
    propsPerNote = 6
    
    def __init__(self, trackNum, dtype):
        self.trackNum = trackNum
        self.length = 0
        self.dtype = dtype
        
        self.notes = array([[]], dtype=self.dtype)
        self.notes.shape = (0, self.propsPerNote)
    
    
    '''
    Getters for one property of all notes
    '''
    def interonsets(self): return self.notes[:, 0]
    def durations(self):   return self.notes[:, 1]    
    def onsets(self):      return self.notes[:, 2]    
    def offsets(self):     return self.notes[:, 3]    
    def pitches(self):     return self.notes[:, 4]
    def velocities(self):  return self.notes[:, 5]
    
    
    def numNotes(self):
        '''
        Number of notes
        '''
        if self.notes is None or len(self.notes.shape) == 0 or self.notes.shape[0] == 0:
            return 0
        elif len(self.notes.shape) > 1:
            return self.notes.shape[0]
        else:
            return 1
        
    
    def __repr__(self):
        ret = "[trackNum=%d, numNotes=%d, length=%d, notes:\n" %(self.trackNum, self.numNotes(), self.length)
        for i in range(self.numNotes()):
            ret += "        %d:[trackNum=%d, interonset=%d, duration=%d, onset=%d, offset=%d, pitch=%d, velocity=%d]\n" %(
                i, self.trackNum, self.notes[i,0], self.notes[i,1], self.notes[i,2], self.notes[i,3], self.notes[i,4], self.notes[i,5])
        ret += "    ]"
        return ret
    
    
    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        if self.__getstate__() != other.__getstate__():
            return False
        return True
    
    
    def __getstate__(self):
        '''
        Overwrite serialization because cPickle saves extra information making the output files very large.
        '''
        notesBA = bytearray(self.notes)
        
        return (self.trackNum,
                self.length,
                self.dtype,
                notesBA)


    def __setstate__(self, state):
        '''
        Overwrite serialization because cPickle saves extra information making the output files very large.
        '''
        self.trackNum, self.length, self.dtype, notesBA = state
        self.notes = frombuffer(notesBA, dtype=self.dtype)
        self.notes.shape = (len(self.notes) / self.propsPerNote, self.propsPerNote)
            
    


class Model(object):
    '''
    Phenotype of the EMC genetic algorithm.
    Represents a musical piece as a collection of tracks.
    '''
    
    def __init__(self, ticksPerQuarterNote = 4, numTracks = 4, dtype = uint16):
        self.ticksPerQuarterNote = ticksPerQuarterNote
        # TODO incorporate tempo here
        self.quarterNotesPerMinute = 120
        self.numTracks = numTracks
        self.dtype = dtype
        
        self.tracks = zeros(self.numTracks, dtype=Track)
        for i in range(self.tracks.size):
            self.tracks[i] = Track(i, self.dtype)
        self.length = 0
        
    
    def interonsets(self):
        '''
        All interonsets.
        TODO if this type of function needed without reallocation with multiple tracks,
        use one array with appended notes for full model.
        '''
        if self.numTracks == 1:
            return self.tracks[0].interonsets()
        iois = array([], dtype=self.dtype)
        for track in self.tracks:
            iois = append(iois, track.interonsets())
        return iois
    
    
    def durations(self):
        '''
        All durations.
        TODO if this type of function needed without reallocation with multiple tracks,
        use one array with appended notes for full model.
        '''
        if self.numTracks == 1:
            return self.tracks[0].durations()
        iois = array([], dtype=self.dtype)
        for track in self.tracks:
            iois = append(iois, track.durations())
        return iois
    
    
    def pitches(self):
        '''
        All pitches.
        TODO if this type of function needed without reallocation with multiple tracks,
        use one array with appended notes for full model.
        '''
        if self.numTracks == 1:
            return self.tracks[0].pitches()
        iois = array([], dtype=self.dtype)
        for track in self.tracks:
            iois = append(iois, track.pitches())
        return iois
    
    
    def velocities(self):
        '''
        All velocities.
        TODO if this type of function needed without reallocation with multiple tracks,
        use one array with appended notes for full model.
        '''
        if self.numTracks == 1:
            return self.tracks[0].velocities()
        iois = array([], dtype=self.dtype)
        for track in self.tracks:
            iois = append(iois, track.velocities())
        return iois
    
    
    def numNotes(self):
        '''
        Number of notes per track.
        '''
        return [track.numNotes() for track in self.tracks]
            
    
    def __repr__(self):
        ret = "[numTracks=%d, ticksPerQuarterNote=%d, length=%d, tracks:\n" %(self.numTracks, self.ticksPerQuarterNote, self.length)
        for i in range(self.tracks.size):
            ret += "    %d:%s\n" %(i,str(self.tracks[i]))
        ret += "]"
        return ret


    def __eq__(self, other):
        if not isinstance(other, Model):
            return False
    
        selfdata = [self.ticksPerQuarterNote, self.numTracks, self.length]
        otherdata = [other.ticksPerQuarterNote, other.numTracks, other.length]
        if selfdata != otherdata:
            return False
        
        for trackInd in range(self.numTracks):
            if not self.tracks[trackInd].__eq__(other.tracks[trackInd]):
                return False

        return True