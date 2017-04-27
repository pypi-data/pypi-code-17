'''
Copy last gen MIDIs from run to common folder.
'''

from os import listdir, makedirs
from os.path import join, exists
from re import search
from shutil import copyfile

if __name__ == '__main__':
        
    resultsDir = '/media/csaba/emc/2017-04-ecal'
    outputDir = join(resultsDir, 'midi')
    
    if not exists(outputDir):
        makedirs(outputDir)
    numGens = 10000
    
    
    print "Searching for test runs"
    
    for testDirName in listdir(resultsDir):
        match = search('emc-ecal2017-oci([a-zA-Z]*)-mem([0-9]*)', testDirName)
        if match:
            ociType = match.group(1)
            memSize = int(match.group(2))
            testDir = join(resultsDir, testDirName)
            
            for subDirName in listdir(testDir):
                match = search('emc_time([0-9\-]*)_rev.*', subDirName)
                if match:
                    timestamp = match.group(1)
                    subDir = join(testDir, subDirName)
                    
                    for midiFileName in listdir(join(subDir, 'midi')):
                        match = search('emc_score([0-9\.]*)_gen([0-9]*)\.mid', midiFileName)
                        if match:
                            grade = match.group(1)
                            gen = int(match.group(2))
                            if gen == numGens - 1:
                                
                                midiFile = join(subDir, 'midi', midiFileName)
                                targetMidiFileName = 'emc-ecal2017-score%s-oci%s-mem%d-time%s.mid' %(
                                              grade, ociType, memSize, timestamp)
                                targetMidiFile = join(outputDir, targetMidiFileName)
                                
                                print 'Copying %s to %s' %(midiFileName, targetMidiFileName)
                                copyfile(midiFile, targetMidiFile)