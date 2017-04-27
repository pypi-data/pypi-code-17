'''
Parsing results, and saving mean/max grades.
'''

from numpy import array, float32, zeros, arange, mean, max, sum, std
from os import listdir, makedirs
from os.path import join, exists
from re import search
from time import time

from emc.cpp.wrapper.descriptor import normalize
from emc.helper.numpyba import NumpyArrayBA
from emc.helper.serializeutils import fromFile, toFile


if __name__ == '__main__':
    resultsDir = '/media/csaba/emc/2017-04-ecal'
    outputDir = join(resultsDir, 'fitness')
    if not exists(outputDir):
        makedirs(outputDir)
    
    importances = array([8,1,8, 8,2,3,1, 3,2,1,1, 15,6,6,1], dtype=float32)
    normalize(importances)
    
    numGens = 10000
    numTests = len(importances)
    numRuns = 20
    numUnits = 1024
    
    forceRewrite = False
    
    print "Used importances: %s" % str(importances)
    print "Assuming %d runs and %d generations" %(numRuns, numGens)
    
    
    allOciTypes = ['Immediate', 'SingleRisc', 'Stack']
    allArchTypes = ['', 'Harvard'] # '' = Von Neumann
    allMemSizes = [256, 4096, 65536]
    
    for ociTypeIdx, ociType in enumerate(allOciTypes):
        for archTypeIdx, archType in enumerate(allArchTypes):
            for memSizeIdx, memSize in enumerate(allMemSizes):
                
                testDir = join(resultsDir, 'emc-ecal2017-oci%s%s-mem%d' %(ociType, archType, memSize))
                
                maxGradesFile = '%s/emc-ecal2017-oci%s%s-mem%d-avgStdGrades.bin' %(outputDir, ociType, archType, memSize)
                if exists(maxGradesFile) and not forceRewrite:
                    print "Test run already completed: ociType=%s, archType=%s, memSize=%d" %(ociType, archType, memSize)
                    print ''
                    continue
        
                timestamps = []
                fitnessDirs = []
                
                grades = zeros((numGens, numUnits, numTests), dtype=float32)
                overallGrades = zeros((numRuns, numGens, numUnits), dtype=float32)
                maxGrades = zeros((numRuns, numGens), dtype=float32)
                meanGrades = zeros((numRuns, numGens), dtype=float32)
                stdGrades = zeros((numRuns, numGens), dtype=float32)
                lastGenGrades = zeros((numRuns, numUnits, numTests), dtype=float32)
                
                avgMaxGrades = zeros(numGens, dtype=float32)
                avgMeanGrades = zeros(numGens, dtype=float32)
                avgStdGrades = zeros(numGens, dtype=float32)
                
                print "Searching for test runs in %s (ociType=%s, archType=%s, memSize=%d)" %(testDir, ociType, archType, memSize)
                st = time()
                
                for subDir in listdir(testDir):
                    match = search('emc_time([0-9\-]*)_rev.*', subDir)
                    if match:
                        timestamps.append(match.group(1))
                        fitnessDirs.append('%s/%s/fitness' %(testDir, subDir))
                
                
                for run, fitnessDir in enumerate(fitnessDirs):
                    if run >= numRuns:
                        print 'WARNING: Number of runs exceeded. Omitting folder %s' %fitnessDir
                        break
                    
                    sst = time()
                    
                    for fitnessFileName in listdir(fitnessDir):
                        match = search('emc_fitness([0-9]*)\-([0-9]*)\.bin', fitnessFileName)
                        startGen = int(match.group(1))
                        endGen = int(match.group(2)) + 1
                        fitnessFile = '%s/%s' %(fitnessDir, fitnessFileName)
                        
                        #print "    Reading results for run %s, gens %d-%d" %(timestamps[run], startGen, endGen)
                        ssst = time()
                        
                        partialGrades = fromFile(fitnessFile)
                        grades[startGen:endGen, :, :] = partialGrades.data
                        
                        print "    Read fitness values for run %s, gens %d-%d in %.3f seconds" %(timestamps[run], startGen, endGen, time() - ssst)
                    
                    print "  Read fitness values for run %s in %.3f seconds" %(timestamps[run], time() - sst)
                    sst = time()
                    
                    overallGrades[run, :, :] = sum(grades * importances, axis = 2)
                    maxGrades[:, :] = max(overallGrades, axis = 2)
                    meanGrades[:, :] = mean(overallGrades, axis = 2)
                    stdGrades[:, :] = std(overallGrades, axis = 2)
                    
                    for fitnessFileName in listdir(fitnessDir):
                        match = search('emc_fitness([0-9]*)\-([0-9]*)\.bin', fitnessFileName)
                        endGen = int(match.group(2)) + 1
                        if endGen == numGens:
                            fitnessFile = '%s/%s' %(fitnessDir, fitnessFileName)
                            
                            print "    Reading last generation results for run %s" %(timestamps[run])
                            ssst = time()
                            
                            partialGrades = fromFile(fitnessFile)
                            lastGenGrades[run, :, :] = partialGrades.data[-1, :, :]
                            
                            print "    Read last generation fitness values for run %s in %.3f seconds" %(timestamps[run], time() - ssst)
                    
                    print "  Calculated mean/avg fitness values for run %s in %.3f seconds" %(timestamps[run], time() - sst)
                    print ''
                    
                
                print "Read all fitness values in %.3f seconds" %(time() - st)
                
                
                for gen in arange(numGens):
                    avgMaxGrades[gen] = mean(maxGrades[:, gen])
                    avgMeanGrades[gen] = mean(meanGrades[:, gen])
                    avgStdGrades[gen] = mean(stdGrades[:, gen])
                   
                
                print "Writing average values to files"
                st = time()
                
                baMaxGrades = NumpyArrayBA(data = maxGrades)
                baMeanGrades = NumpyArrayBA(data = meanGrades)
                baStdGrades = NumpyArrayBA(data = stdGrades)
                baAvgMaxGrades = NumpyArrayBA(data = avgMaxGrades)
                baAvgMeanGrades = NumpyArrayBA(data = avgMeanGrades)
                baAvgStdGrades = NumpyArrayBA(data = avgStdGrades)
                baLastGenGrades = NumpyArrayBA(data = lastGenGrades)
                
                toFile(baMaxGrades,     '%s/emc-ecal2017-oci%s%s-mem%d-maxGrades.bin'     %(outputDir, ociType, archType, memSize))
                toFile(baMeanGrades,    '%s/emc-ecal2017-oci%s%s-mem%d-meanGrades.bin'    %(outputDir, ociType, archType, memSize))
                toFile(baStdGrades,     '%s/emc-ecal2017-oci%s%s-mem%d-stdGrades.bin'     %(outputDir, ociType, archType, memSize))
                toFile(baAvgMaxGrades,  '%s/emc-ecal2017-oci%s%s-mem%d-avgMaxGrades.bin'  %(outputDir, ociType, archType, memSize))
                toFile(baAvgMeanGrades, '%s/emc-ecal2017-oci%s%s-mem%d-avgMeanGrades.bin' %(outputDir, ociType, archType, memSize))
                toFile(baAvgStdGrades,  '%s/emc-ecal2017-oci%s%s-mem%d-avgStdGrades.bin'  %(outputDir, ociType, archType, memSize))
                toFile(baLastGenGrades, '%s/emc-ecal2017-oci%s%s-mem%d-lastGenGrades.bin' %(outputDir, ociType, archType, memSize))
                
                print "Wrote all values in %.3f seconds" %(time() - st)