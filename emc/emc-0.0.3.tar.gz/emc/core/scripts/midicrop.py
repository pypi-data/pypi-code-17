'''
Helper script to crop a MIDI file/model based on ticks or seconds.
@author Csaba Sulyok
'''
from os import chdir
from numpy import floor, ceil, zeros, arange

from emc.core.integ.midi import readFromMidi, writeToMidi


def cropTrack(track, startTicks, endTicks):
    # find notes which will be included
    noteIncluded = zeros(track.numNotes(), dtype=bool)
    for i in arange(track.numNotes()):
        noteIncluded[i] = track.notes[i,2] >= startTicks and track.notes[i,2] <= endTicks
        
    # disregard other notes
    track.notes = track.notes[noteIncluded,:]
    
    # find delay of first note so tracks will remain aligned
    delay = track.notes[0,2] - startTicks
    track.notes[0,0] = delay
    track.notes[:,2] -= startTicks
    track.notes[:,3] -= startTicks
    

def cropModel(filename = None, model = None,
              startTicks = None, endTicks = None,
              startSecs = None, endSecs = None,
              outputFilename = None):
    '''
    Helper script to crop a MIDI file/model based on ticks or seconds.
    Either a model or a filename must be passed.
    Edges may be given in seconds or ticks. File start/end assumed to be edges as default.
    '''
    
    # check if mandatory parameter given
    if filename is None and model is None:
        print "Error: filename or model must be given"
        return
    
    # if filename given, read it
    if filename is not None:
        print 'Reading MIDI file %s' %(filename)
        model = readFromMidi(filename)
    
    # deduce start/end
    ticksPerSecond = model.ticksPerQuarterNote * model.quarterNotesPerMinute / 60.0
    
    if startSecs is not None:
        startTicks = int(floor(startSecs * ticksPerSecond))
    elif startTicks is not None:
        startSecs = float(startTicks) / float(ticksPerSecond)
    else:
        startTicks = startSecs = 0
    
    if endSecs is not None:
        endTicks = int(ceil(endSecs * ticksPerSecond))
    elif endTicks is not None:
        endSecs = float(endTicks) / float(ticksPerSecond)
    else:
        endTicks = model.length
        endSecs = float(endTicks) / float(ticksPerSecond)
    
    print 'Cropping from %.2fs to %.2fs (%d to %d ticks)' %(startSecs, endSecs, startTicks, endTicks)
    for track in model.tracks:
        cropTrack(track, startTicks, endTicks)
    
    # if file was read and no specific output filename was given, deduce one
    if filename is not None and outputFilename is None:
        outputFilename = '%s_cropped_%.1f_%.1f.mid' %(filename[:-4], startSecs, endSecs)
        #outputFilename = '%s_cropped.mid' %(filename[:-4])
    
    # if output filename given (or deduced from input), write output there
    if outputFilename is not None:
        print 'Writing MIDI file %s' %(outputFilename)
        writeToMidi(model, outputFilename)
        


if __name__ == '__main__':
    d = 'x:/Semester10/ECS750D - Project/emc/src/emc-core/resources/output/hall of fame'
    chdir(d)
    
    cropModel(filename = 'm2.mid', startSecs = 53)
    cropModel(filename = 'emc_score0.823_gen19999.mid', startSecs = 1.5, endSecs = 14.5)
    cropModel(filename = 'emc_time20150314-235255_gen07999_score0.616.mid', endSecs = 77)
    cropModel(filename = 'emc_time20150315-000716_gen01999_score0.626.mid', endSecs = 28)
    cropModel(filename = 'emc_time20150315-003711_gen08999_score0.783.mid', startSecs = 66)
    cropModel(filename = 'emc_time20150315-005932_gen00999_score0.829.mid', startSecs = 6.5, endSecs = 23)
    cropModel(filename = 'emc_time20150315-020236_gen00999_score0.686.mid', endSecs = 61)
    cropModel(filename = 'emc_time20150315-021548_gen01499_score0.737.mid', startSecs = 3, endSecs = 15)
    cropModel(filename = 'm_4.mid', startSecs = 9, endSecs = 78)