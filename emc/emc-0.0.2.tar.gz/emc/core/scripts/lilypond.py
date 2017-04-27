'''

Creating MIDI out of model:

1. Install Lilypond, include in PATH and set lilypond_home

'''
from numpy import uint8, array

from emc.core.core.model import Model
from emc.core.integ.midi import writeToMidi
from emc.cpp.wrapper.modelbuilder import ModelBuilderWrapper

if __name__ == '__main__':
    '''
    2. Output a MIDI file somewhere.
    '''
    
    notes = array([0, 0, 2, 0x34,
                   0, 2, 2, 0x35,
                   1, 0, 4, 0x3b], dtype=uint8)
    mb = ModelBuilderWrapper(numTracks = 2)
    model = mb.bytesToModel(Model, notes)
    
    print 'Write MIDI'
    writeToMidi(model, 'test.mid')
    
    
    '''
    3. Midi2Ly
    midi2ly.py test.mid
    '''
    
    
    '''
    4. Adapt LY file as you wish
    Pointers:
    
    \time 11/16
    \key d \major
    
    '''
    
    '''
    5. lilypond ly file
    lilypond test-midi.ly
    '''