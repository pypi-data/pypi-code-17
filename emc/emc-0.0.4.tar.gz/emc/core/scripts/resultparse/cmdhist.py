from matplotlib.pyplot import *
from numpy import *

from emc.core.integ.cd import cdr
from emc.cpp.wrapper.oci.immediateoci import ImmediateOciWrapper
from emc.cpp.wrapper.oci.indirectoci import IndirectOciWrapper
from emc.helper.serializeutils import fromFile

oci1 = ImmediateOciWrapper(maxCommands = 60000, maxOutputs = 2600, haltAllowed = True)
oci2 = IndirectOciWrapper(maxCommands = 60000, maxOutputs = 2600, haltAllowed = True)


def occurrencesByFile(inp):
    cdr()
    alg = fromFile(inp)
    pop = alg.population
    oci = alg.phenotypeRenderer.opCodeInterpreter
    
    idx = argmax(pop.grades)
    genString = pop.genotypes[idx]
    return oci.geneticStringToOccurrences(genString.data)


if __name__ == '__main__':
        
    '''
    STEP 1 - expected ratios of occurrences
    '''
    expected1 = array(oci1.categoryCommands.values(), dtype=float64) / 256
    expected2 = array(oci2.categoryCommands.values(), dtype=float64) / 256
    
    
    '''
    STEP 2 - random genetic strings occurrences
    '''
    '''
    n = 2000
    
    oc1 = zeros((n, 5), dtype=float64)
    oc2 = zeros((n, 5), dtype=float64)
    
    for _ in arange(1):
        for i in arange(n):
            genString = GeneticString(data = randomByteArray(oci1.geneticStringSize))
            oc1[i,:] = oci1.geneticStringToOccurrences(genString.data)
            oc1[i,:] /= sum(oc1[i,:])
            genString = GeneticString(data = randomByteArray(oci2.geneticStringSize))
            oc2[i,:] = oci2.geneticStringToOccurrences(genString.data)
            oc2[i,:] /= sum(oc2[i,:])
        
        random1 = mean(oc1, axis=0)
        random2 = mean(oc2, axis=0)
    '''
    random1 = array([0.3566, 0.2959, 0.0384, 0.2019, 0.1073], dtype=float64)
    random2 = array([0.2353, 0.2823, 0.0604, 0.3561, 0.0660], dtype=float64)
    
    '''
    STEP 3 - max genetic string occurrences
    '''
    resultsDir = 'I:/2015-07-evocomp'
    occurrencesFile = 'I:/2015-07-evocomp/cmdoccurrences/occurrences.bin'
    numGens = 20000
    numRuns = 20
    
    allNumUnits = array([16,32,64,128,256,512,1024], dtype=uint16)
    allOciTypes = ['Immediate', 'Indirect']
    allTrackTypes = ['single', 'multi']
    
    numUnitsSize = size(allNumUnits)
    ociTypesSize = size(allOciTypes)
    trackTypesSize = size(allTrackTypes)
    
    
    '''
    a) extract occurrences
    '''
    '''
    allOccurrences = zeros((numUnitsSize, ociTypesSize, trackTypesSize, numRuns, 5), dtype=uint32)
    
    for numUnitsIdx, numUnits in enumerate(allNumUnits):
        for ociTypeIdx, ociType in enumerate(allOciTypes):
            for trackTypeIdx, trackType in enumerate(allTrackTypes):
                runIdx = 0
                
                testDir = '%s/oci%s-%sTrack-pop%04d' %(resultsDir, ociType, trackType, numUnits)
                for subDir in listdir(testDir):
                    lastGenFile = '%s/%s/alg/%s_gen19999.emc' %(testDir, subDir, subDir)
                    
                    print lastGenFile
                    allOccurrences[numUnitsIdx, ociTypeIdx, trackTypeIdx, runIdx, :] = occurrencesByFile(lastGenFile)
                    runIdx += 1
    
    
    baAllOccurrences = NumpyArrayBA(data = allOccurrences)
    toFile(baAllOccurrences, occurrencesFile)
    '''
    '''
    b) use occurrences
    
    '''
    allOccurrences = fromFile(occurrencesFile).data.astype(float64)
    sumAllOccurrences = sum(allOccurrences, axis=4)
    
    allOccurrenceRatios = zeros((numUnitsSize, ociTypesSize, trackTypesSize, numRuns, 5), dtype=float64)
    for i in arange(5):
        allOccurrenceRatios[:, :, :, :, i] = allOccurrences[:, :, :, :, i] / sumAllOccurrences
    
    
    occurrenceRatios = mean(mean(mean(allOccurrenceRatios, axis=3), axis=2), axis=0)
    actual1 = occurrenceRatios[0,:]
    actual2 = occurrenceRatios[1,:]
    
    
    
    # FIGURES
    
    n = size(actual1)
    
    barwidth = 0.25
    gapwidth = 0.05
    margin = 0.1
    
    ind1 = arange(n) - barwidth - gapwidth / 2
    ind2 = arange(n) + gapwidth / 2
    
    for (idx, random, actual) in ((1, random1, actual1), (2, random2, actual2)):
        figure()
        
        rects1 = bar(ind1, random, barwidth, linewidth=2, color='#D0C0A0', label='First generation')
        rects2 = bar(ind2, actual, barwidth, linewidth=2, color='#204030', label='Last generation')
        
        grid('on')
        xlabel('Instruction types', fontsize=20)
        ylabel('Percentage of occurrence', fontsize=20)
        xticks((ind1 + ind2 + barwidth) / 2)
        
        gca().set_xticklabels([s[:1].upper() + s[1:] for s in oci1.categoryCommands.keys()])
        for tick in gca().xaxis.get_major_ticks():
            tick.label.set_fontsize(16)
        gca().set_yticklabels(['%d%%' %(i) for i in arange(0, 45, 5)])
        for tick in gca().yaxis.get_major_ticks():
            tick.label.set_fontsize(14)
        
        xlim([ind1[0] - margin, ind2[-1] + barwidth + margin])
        ylim([-0, 0.4])
        tight_layout()
        
        savefig('cmdhist%d.pdf' %idx)
        
    show()