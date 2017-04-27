'''
Parsing results, printing fitness diagrams.
'''
from matplotlib.pyplot import plot, xlabel, ylabel, show, ylim, legend, \
    bar, xlim, figure, tight_layout, grid, xticks, yticks
from numpy import histogram, arange

from emc.helper.serializeutils import fromFile


if __name__ == '__main__':

    
    outputDir = 'i:/2015-03-ecal'
    
    print 'Reading overall results files'
    
    maxGrades = fromFile('%s/emc_maxGrades.bin' %(outputDir)).data
    meanGrades = fromFile('%s/emc_meanGrades.bin' %(outputDir)).data
    avgMaxGrades = fromFile('%s/emc_avgMaxGrades.bin' %(outputDir)).data
    avgMeanGrades = fromFile('%s/emc_avgMeanGrades.bin' %(outputDir)).data
    lastGenGrades = fromFile('%s/emc_lastGenGrades.bin' %(outputDir)).data
    
    
    # FIGURE 1 - MAX AND MEAN GRADES PROGRESSION
    
    figure()
    
    length = len(avgMaxGrades)
    x = arange(0, length, 50)
    
    plot(x, avgMaxGrades[x], label='Maximum grades', color='#602010')
    plot(x, avgMeanGrades[x], label='Average grades', color='#206010')
    
    grid('on')
    xticks(arange(0,length+1,2500))
    yticks(arange(0,1.1,0.1))
    
    xlabel('Generation index', fontsize=20)
    ylabel('Fitness test grades', fontsize=20)
    #title('Progression of maximum and average grades\nwithin each generation, across all runs')
    ylim([0, 1])
    legend(loc=4, fontsize=18)
    tight_layout()
    
    #savefig('results.pdf')
    print avgMaxGrades[-1]
    print avgMeanGrades[-1]
    
    
    
    # FIGURE 2 - DISTRIBUTION OF LAST GENERATION MAXIMA
    
    maxLastGrades = maxGrades[:,-1]
    
    hist, histBins = histogram(maxLastGrades, bins = 6)
    histCenters = (histBins[:-1] + histBins[1:]) / 2
    histWidth = 0.5 * (histBins[1] - histBins[0])
    
    figure()
    bar(histCenters, hist, align='center', width=histWidth, color='#706860')
    xlabel('Fitness test grade', fontsize=20)
    ylabel('Number of last generation units', fontsize=20)
    #title('Distribution of maximum grade in last generation per run')
    xlim([0,1])
    tight_layout()
    
    #savefig('results2.pdf')
    show()
    
    
    '''
    # FIGURE 3 - BEST LAST GEN UNITS - MAX AND MEAN GRADES PER TEST
    
    importances = array([10,8,12, 8,2,3,1,3,2,1,1,15,8,4,1], dtype=float32)
    normalize(importances)
    
    #print maxGrades[: ,-1]
    #overallGrades[run, :, :] = sum(grades * importances, axis = 2)
    
    numRuns, numUnits, numTests = lastGenGrades.shape
    lastGenOverallGrades = sum(lastGenGrades * importances, axis = 2)
    lastGenBestOverallGradeIdxs = argmax(lastGenOverallGrades, axis = 1)
    
    lastGenBestGrades = zeros((numRuns, numTests), dtype=float32)
    for run in arange(numRuns):
        lastGenBestGrades[run, :] = lastGenGrades[run, lastGenBestOverallGradeIdxs[run], :]
        
    maxLastGenBestGrades = max(lastGenBestGrades, axis = 0)
    meanLastGenBestGrades = mean(lastGenBestGrades, axis = 0)
    
    bar(arange(numTests), maxLastGenBestGrades, align='center', width=0.5)
    tight_layout()
    
    show()
    '''