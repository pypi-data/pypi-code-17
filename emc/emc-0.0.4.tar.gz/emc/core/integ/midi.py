'''
Classes to convert EMC model to/from MIDI

@author: Csaba Sulyok
'''
from numpy import array, append, uint16, uint32

from emc.core.core.model import Model
from emc.core.integ.dict import DDict
from emc.core.integ.midiparser import MidiFile, MidiTrack, DeltaTime, MidiEvent


class NoteQueue(object):
    '''
    Queue which inserts into location based on absolute ending time of note.
    Popping always returns closest ending note.
    Used in calculating correct order for note-on/note-off events in MIDI exports.
    '''
    
    data = []
    
    def push(self, obj):
        i = 0
        while i < len(self.data) and self.data[i].end > obj.end:
            i += 1
        self.data.insert(i, obj)
    
    def empty(self):
        return len(self.data) == 0
    
    def peek(self):
        if not self.empty():
            return self.data[-1]
    
    def peekTime(self):
        if not self.empty():
            return self.data[-1].end
    
    def pop(self):
        if not self.empty():
            ret = self.data[-1]
            del(self.data[-1])
            return ret
    
    def delay(self, vtime):
        for note in self.data:
            note.start -= vtime
            note.end -= vtime
    
    def __repr__(self):
        ret = 'queue['
        for note in self.data:
            ret += "(%d, %d), " %(note.start, note.end)
        ret += ']'
        return ret
    



class MidiReader(object):
    '''
    Reads EMC model from MIDI file.
    '''
    
    debug = False
    
    def findEvent(self, track, eventStartIdx, lambdaExpr):
        '''
        Finds MIDI event based on lambda expression, starting from a given index.
        Returns a tuple of the following 3 elements:
        1. event index where the lambda expression is true
        2. aggregate delta time from event start index until the found event
        3. flag whether or not any value was found, or we've reached the end of the event queue
        '''
        
        eventIdx = eventStartIdx
        deltaTime = 0
        while eventIdx < len(track.events) and not lambdaExpr(track.events[eventIdx]):
            if track.events[eventIdx].type == 'DeltaTime':
                deltaTime += track.events[eventIdx].time
            eventIdx += 1
        
        success = eventIdx < len(track.events)
        return (eventIdx, deltaTime, success)
    
    
    
    def addNote(self, trackIdx, ioi, duration, pitch, velocity):
        '''
        Add a note to our bytestream which will yield a model.
        '''
        track = self.model.tracks[trackIdx]
        
        onset = self.trackPtr + ioi
        offset = onset + duration
        self.trackPtr = onset
        
        track.notes = append(track.notes, array([ioi, duration, onset, offset, pitch, velocity], dtype=self.dtype))
        
        
    
    def addTrack(self, trackIdx):
        '''
        Decodes a track from the MIDI file into an EMC model track.
        '''
        track = self.midiFile.tracks[trackIdx + 1]
        self.trackPtr = 0
        
        eventIdx = 0
        numNotes = 0
        (noteOnIdx, noteOnDelta, noteOnFound) = self.findEvent(track, eventIdx, lambda e: e.type == 'NOTE_ON')
        
        while noteOnFound:
            pitch = track.events[noteOnIdx].pitch
            velocity = track.events[noteOnIdx].velocity
            eventIdx = noteOnIdx + 1
            
            (_, noteOffDelta, _) = self.findEvent(track, eventIdx, lambda e: e.type == 'NOTE_OFF' and e.pitch == pitch)
            self.addNote(trackIdx, noteOnDelta, noteOffDelta, pitch, velocity)
            numNotes += 1
            (noteOnIdx, noteOnDelta, noteOnFound) = self.findEvent(track, eventIdx, lambda e: e.type == 'NOTE_ON')
        
        track = self.model.tracks[trackIdx]
        track.notes.shape = (len(track.notes) / track.propsPerNote, track.propsPerNote)
        
        if track.numNotes() > 0:
            track.length = max(track.offsets())
            self.model.length = max(track.length, self.model.length)
        
    
    
    def transformFromMidi(self, midiFile):
        '''
        Transforms MidiFile object into EMC model object.
        '''
        self.midiFile = midiFile
        self.dtype = uint16
        
        # get full length and check if too long
        length = self.midiFile.tracks[0].events[-1].time
        
        if length > 65536:
            print 'Warning. MIDI file too long, should subsample'
            print 'Using 4 bytes until then'
            self.dtype = uint32
        
        # track zero is ommitted
        numTracks = len(self.midiFile.tracks) - 1
        self.model = Model(numTracks = numTracks,
                           ticksPerQuarterNote = self.midiFile.ticksPerQuarterNote,
                           dtype = self.dtype)
        
        for trackIdx in range(numTracks):
            self.addTrack(trackIdx)
        
        return self.model


    
    def readFromMidi(self, filename):
        '''
        Reads model object from MIDI file.
        Transforms each MidiTrack to EMC tracks.
        '''
        self.midiFile = MidiFile()
        self.midiFile.open(filename, 'rb')
        self.midiFile.read()
        self.midiFile.close()
        
        return self.transformFromMidi(self.midiFile)
        



class MidiWriter(object):
    '''
    Writes EMC model objects out to MIDI files.
    Uses only a minimal number of MIDI events to get the job done.
    '''

    
    def addEvent(self, deltaTime, eventType, pitch=None, velocity=None, data=None):
        '''
        Writes a next MIDI event placed on the current time pointer.
        This creates both a DeltaTime MIDI event, and an actual note-on/note-off/meta event
        with given parameters.
        '''
        self.currentTime += deltaTime
        
        deltaEvent = DeltaTime(self.midiTrack)
        deltaEvent.time = deltaTime
        self.midiTrack.events.append(deltaEvent)
        
        midiEvent = MidiEvent(self.midiTrack)
        midiEvent.time = self.currentTime
        midiEvent.type = eventType
        midiEvent.channel = self.midiTrack.index
        midiEvent.pitch = pitch
        midiEvent.velocity = velocity
        midiEvent.data = data
        
        self.midiTrack.events.append(midiEvent)
        
        
    
    def addTrackZero(self):
        '''
        Writes zeroeth track into MidiFile object, which just sets the tempo.
        '''
        self.currentTime = 0
        
        self.midiTrack = MidiTrack(0)
        self.midiFile.tracks.append(self.midiTrack)
        
        # TODO incorporate tempo here
        self.addEvent(0, "SET_TEMPO", data = '\x07\xa1 ')
        self.addEvent(0, "SEQUENCE_TRACK_NAME", data = '')
        self.addEvent(0, "END_OF_TRACK", data = '')
        
        
    
    def addNote(self, data):
        '''
        Adds note on and note off events to midi file.
        Takes care of queueing to make sure note-on-off events come in order.
        '''
        note = DDict(start = int(data[0]), end = int(data[0]+data[1]), data = data)
        
        self.noteQueue.push(note)
        
        while not self.noteQueue.empty() and self.noteQueue.peekTime() <= note.start:
            offNote = self.noteQueue.pop()
            self.addEvent(offNote.end, "NOTE_OFF", pitch = offNote.data[4], velocity = 80)
            self.noteQueue.delay(offNote.end)
        
        self.addEvent(note.start, "NOTE_ON", pitch = note.data[4], velocity = note.data[5])
        self.noteQueue.delay(note.start)
        
        
        
    def addTrack(self, track):
        '''
        Writes current track into MidiFile object.
        Creates MidiTrack object and populates it with events.
        '''
        self.currentTime = 0
        
        self.midiTrack = MidiTrack(track.trackNum + 1)
        self.midiFile.tracks.append(self.midiTrack)

        self.addEvent(0, "SEQUENCE_TRACK_NAME", data = 'EMC Track %d' % self.midiTrack.index)        
        
        self.noteQueue = NoteQueue()
        for i in range(track.numNotes()):
            self.addNote(track.notes[i])
        while not self.noteQueue.empty():
            offNote = self.noteQueue.pop()
            self.addEvent(offNote.end, "NOTE_OFF", pitch = offNote.data[4], velocity = 80)
            self.noteQueue.delay(offNote.end)
        
        self.addEvent(0, "END_OF_TRACK", data = '')
            
    
    
    def transformToMidi(self, model, includeEmptyTracks = True):
        '''
        Transforms EMC model object into MidiFile object.
        Can be used to write MIDI to file.
        '''
        self.midiFile = MidiFile()
        self.midiFile.ticksPerQuarterNote = model.ticksPerQuarterNote
        
        self.addTrackZero()
        for track in model.tracks:
            if includeEmptyTracks or track.numNotes() > 0:
                self.addTrack(track)
        
        return self.midiFile
    

    
    def writeToMidi(self, model, filename, includeEmptyTracks = True):
        '''
        Writes model object into MIDI file.
        Transforms each track of model into MidiTrack and outputs result to file.
        '''
        self.transformToMidi(model, includeEmptyTracks)
        self.midiFile.open(filename, 'wb')
        self.midiFile.write()
        self.midiFile.close()
        
        return self.midiFile
        


# default instances
midiReader = MidiReader() 
midiWriter = MidiWriter()

# default methods
transformFromMidi = midiReader.transformFromMidi
transformToMidi = midiWriter.transformToMidi
readFromMidi = midiReader.readFromMidi
writeToMidi = midiWriter.writeToMidi
