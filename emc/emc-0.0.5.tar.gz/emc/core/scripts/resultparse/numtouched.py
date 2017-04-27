from matplotlib.pyplot import *
from numpy import *
from os import chdir, makedirs
from os.path import join, abspath, dirname, exists
from posix import listdir
from re import search

from emc.cpp.swig.emcpp import randomByteArray
from emc.cpp.wrapper.oci.immediateoci import ImmediateOciWrapper
from emc.helper.serializeutils import fromFile, toFile
from emc.core.integ.dict import DDict


if __name__ == '__main__':
    
    chdir(abspath("%s/../../.." % (dirname(__file__))))
    set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)},
                     linewidth=150)
    rcParams['xtick.major.pad'] = 10
    
    resultsDir = '/media/csaba/emc/2017-04-ecal'
    bgsDir = join(resultsDir, 'bestgenstring')
    
    if not exists(bgsDir):
        makedirs(bgsDir)
    
    allOciTypes = ['Immediate', 'SingleRisc', 'Stack']
    allOciTypesPretty = ['Complex', 'Single-', 'Stack-based']
    allArchTypes = ['', 'Harvard'] # '' = Von Neumann
    allMemSizes = [256, 4096, 65536]
    
    ociTypesSize = size(allOciTypes)
    archTypesSize = size(allArchTypes)
    memSizesSize = size(allMemSizes)
    numRuns = 20
    numUnits = 1024
    
    numTouchedBestLocal = zeros(numUnits, dtype=uint32)
    numTouchedRndLocal = zeros(numUnits, dtype=uint32)
    
    numTouchedBest = zeros((memSizesSize, ociTypesSize, archTypesSize, numRuns, numUnits), dtype=float32)
    numTouchedBestOverall = zeros((memSizesSize, ociTypesSize, archTypesSize, numRuns), dtype=float32)
    numTouchedRnd = zeros((memSizesSize, ociTypesSize, archTypesSize, numRuns, numUnits), dtype=float32)
    
    for ociTypeIdx, ociType in enumerate(allOciTypes):
        for archTypeIdx, archType in enumerate(allArchTypes):
            for memSizeIdx, memSize in enumerate(allMemSizes):
                
                if memSizeIdx is not 2:
                    continue
                
                run = 0
                testDir = join(resultsDir, 'emc-ecal2017-oci%s%s-mem%d' %(ociType, archType, memSize))
                for subDir in listdir(testDir):
                    match = search('emc_time([0-9\-]*)_rev.*', subDir)
                    if match:
                        timestamp = match.group(1)
                        
                        bgsFile = join(bgsDir, 'emc-ecal2017-oci%s%s-mem%d-time%s.bin' %(ociType, archType, memSize, timestamp))
                        
                        if not exists(bgsFile):
                            algFile = join(testDir, '%s/alg/emc_gen09999.emc' %(subDir))
                            alg = fromFile(algFile)
                            
                            bestModelIdx = argmax(alg.population.grades)
                            genotypes = alg.population.genotypes
                            oci = alg.phenotypeRenderer.opCodeInterpreter
                            
                            for unitIdx in arange(numUnits):
                                numTouchedBestLocal[unitIdx], _ = oci.geneticStringToTouched(genotypes[unitIdx].data)
                                randomData = randomByteArray(oci.geneticStringSize)
                                numTouchedRndLocal[unitIdx], _ = oci.geneticStringToTouched(randomData)
                            
                            content = DDict(numTouchedBest = numTouchedBestLocal, numTouchedRnd = numTouchedRndLocal, oci = oci, bestModelIdx = bestModelIdx)
                            toFile(content, bgsFile)
                            print 'Writing', bgsFile
                        else:
                            content = fromFile(bgsFile)
                            #print 'Using cached', bgsFile
                        
                        if run >= numRuns:
                            #print 'WARNING: Number of runs exceeded. Omitting file %s' %bgsFile
                            break
                        
                            
                        numTouchedBest[memSizeIdx, ociTypeIdx, archTypeIdx, run, :] = content.numTouchedBest
                        numTouchedBestOverall[memSizeIdx, ociTypeIdx, archTypeIdx, run] = content.numTouchedBest[content.bestModelIdx]
                        numTouchedRnd[memSizeIdx, ociTypeIdx, archTypeIdx, run, :] = content.numTouchedRnd
                        
                        run = run + 1
                #print run
                        
    
    def plotHist(top, dataBest, dataBestOA, dataRnd, figTitle, figName):
        
        numBins = log2(top)
        step = log(top) / numBins
        histBins = exp(arange(0, log(top)+step, step))
        
        histBest, _ = histogram(dataBest, bins = histBins)
        histBestOA, _ = histogram(dataBestOA, bins = histBins)
        histRnd, _ = histogram(dataRnd, bins = histBins)
        
        # normalize histogram    
        histBest = histBest.astype(float32)
        histBest /= sum(histBest)
        histBestOA = histBestOA.astype(float32)
        histBestOA /= sum(histBestOA)
        histRnd = histRnd.astype(float32)
        histRnd /= sum(histRnd)
        
        print histBest
        print histBestOA
        print histRnd
        print ''
        
        # find max value of hist to draw (round to within 5%)
        yMax = ceil(max(append(append(histBest, histBestOA), histRnd)) * (1 / 0.05)) / (1 / 0.05)
        
        dotCenters = arange(numBins) + .5
        
        figure()
        title(figTitle, size=24, y=1.07)
        
        plot(dotCenters, histRnd, label='Initial gen.',
                                color='#806860', linestyle='--', linewidth=3,
                                marker='*', markersize=12)
        fill_between(dotCenters, histRnd, where = histRnd>=0, color=(0.65, 0.25, 0.2, 0.05))
        plot(dotCenters, histBest, label='Final gen.',
                                color='#608068', linestyle='-.', linewidth=2,
                                marker='o', markersize=8)
        fill_between(dotCenters, histBest, where = histBest>=0, color=(0.2, 0.65, 0.25, 0.25))
        plot(dotCenters, histBestOA, label='Final best',
                                color='#686080', linestyle=':', linewidth=1,
                                marker='^', markersize=8)
        fill_between(dotCenters, histBestOA, where = histBestOA>=0, color=(0.25, 0.2, 0.65, 0.1))
        
        xlabel('Number of touched bytes', fontsize=19)
        ylabel('Percentage of genetic strings', fontsize=20)
        xticks(arange(numBins+1))
        yticks(arange(0.0, yMax + 0.1, 0.05))
        
        gca().set_xticklabels([r'$\mathregular{2^{%d}}$' %(f) for f in round_(log2(histBins)).astype(uint8)])
        gca().set_yticklabels(['%.0f%%' %(f * 100) for f in arange(0.0, yMax + 0.1, 0.05)])
        
        for tick in gca().xaxis.get_major_ticks():
            tick.label.set_fontsize(18)
        for tick in gca().yaxis.get_major_ticks():
            tick.label.set_fontsize(16)
        
        legend(fontsize=18, loc=2, framealpha=0.0)
            
        xlim([0, numBins])
        ylim([0, yMax + 0.05])
        tight_layout()
        
        #savefig(figName + '.svg')
        savefig(figName + '.pdf')
        
        
    
    
    numTouchedBest.shape = (memSizesSize, ociTypesSize, archTypesSize * numRuns * numUnits)
    numTouchedBestOverall.shape = (memSizesSize, ociTypesSize, archTypesSize * numRuns)
    numTouchedRnd.shape = (memSizesSize, ociTypesSize, archTypesSize * numRuns * numUnits)
    
    for memSizeIdx, memSize in enumerate(allMemSizes):
        for ociTypeIdx, ociType in enumerate(allOciTypes):
        
            if memSizeIdx is not 2:
                continue
            
            plotHist(memSize,
                     dataBest = numTouchedBest[memSizeIdx, ociTypeIdx],
                     dataBestOA = numTouchedBestOverall[memSizeIdx, ociTypeIdx],
                     dataRnd = numTouchedRnd[memSizeIdx, ociTypeIdx],
                     figTitle = "%s instruction set" %(allOciTypesPretty[ociTypeIdx]),
                     figName = 'numtouched-%s' %(ociType))


    '''
    numTouchedBest.shape = (memSizesSize, ociTypesSize * archTypesSize * numRuns * numUnits)
    numTouchedBestOverall.shape = (memSizesSize, ociTypesSize * archTypesSize * numRuns)
    numTouchedRnd.shape = (memSizesSize, ociTypesSize * archTypesSize * numRuns * numUnits)
    
    for memSizeIdx, memSize in enumerate(allMemSizes):
        if memSizeIdx is not 2:
            continue
        plotHist(memSize,
                 dataBest = numTouchedBest[memSizeIdx],
                 dataBestOA = numTouchedBestOverall[memSizeIdx],
                 dataRnd = numTouchedRnd[memSizeIdx],
                 figTitle = None,
                 figName = 'numtouched')
                 
    '''
    #show()
        