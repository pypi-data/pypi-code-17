'''
Randomly choose 10 MIDIs above 0.7 for display in report.
'''

from os import listdir
from re import search

from numpy import *
from numpy.random.mtrand import randint, choice

from emc.core.integ.midi import readFromMidi
from emc.core.scripts.midicrop import cropModel

if __name__ == '__main__':
    inputDir = 'i:/2015-07-evocomp/midi'
    outputDir = 'i:/2015-07-evocomp/midi/forReport'
    
    # number of MIDIs to choose
    N = 10
    # minimum grade of chosen MIDIs
    cutOffGrade = 0.7
    # length to crop the MIDIs randomly
    L = 96
    
    goodMidis = array([], dtype=str)
    
    # READ RESULTS FILES
    
    
    
    # parse MIDI folder - find MIDIs with good enough overall grade
    for mf in listdir(inputDir):
        match = search('emc_oci([a-zA-Z]*)_([a-zA-Z]*)Track_pop([0-9]*)_time([0-9-]+)_gen19999_score([0-9\.]+)\.mid', mf)
        
        if match:
            ociType = match.group(1)
            trackType = match.group(2)
            popSize = match.group(3)
            timeStamp = match.group(4)
            grade = float32(match.group(5))
            
            if grade >= cutOffGrade:
                goodMidis = append(goodMidis, mf)
    
    
    # choose 10 randomly from these MIDIs
    numGoodMidis = goodMidis.shape[0]
    chosenMidiIdxs = choice(numGoodMidis, N, replace=False)
    
    
    # crop chosen MIDIs and save
    for chosenMidiIdx in chosenMidiIdxs:
        chosenMidi = goodMidis[chosenMidiIdx]
        
        # read model
        model = readFromMidi('%s/%s' %(inputDir, chosenMidi))
        # generate crop start and end point 
        startTicks = randint(model.length - L)
        endTicks = startTicks + L
        # perform cropping and save
        outputFilename = '%s/%s' %(outputDir, chosenMidi)
        cropModel(model = model, outputFilename = outputFilename,
                  startTicks = startTicks, endTicks = endTicks)