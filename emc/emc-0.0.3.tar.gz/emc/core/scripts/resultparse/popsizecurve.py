'''
Parsing mean/max results, plotting diagrams
'''

from matplotlib.pyplot import xlabel, ylabel, show, ylim, legend, \
    xlim, tight_layout, grid, xticks, yticks, gca,\
    semilogx
from numpy import *
from emc.helper.serializeutils import fromFile
from scipy.optimize.minpack import curve_fit

if __name__ == '__main__':
    resultsDir = 'i:/2015-07-evocomp/fitness'
    numGens = 20000
    numRuns = 20
    
    allNumUnits = array([16,32,64,128,256,512,1024], dtype=uint16)
    allOciTypes = ['Immediate', 'Indirect']
    allTrackTypes = ['single', 'multi']
    
    numUnitsSize = size(allNumUnits)
    ociTypesSize = size(allOciTypes)
    trackTypesSize = size(allTrackTypes)
    
    allAvgMaxGrades = zeros((numUnitsSize, ociTypesSize, trackTypesSize, numGens), dtype=float32)
    allAvgMeanGrades = zeros((numUnitsSize, ociTypesSize, trackTypesSize, numGens), dtype=float32)
    
    
    # READ RESULTS FILES
    
    for numUnitsIdx, numUnits in enumerate(allNumUnits):
        for ociTypeIdx, ociType in enumerate(allOciTypes):
            for trackTypeIdx, trackType in enumerate(allTrackTypes):
                prefix = 'oci%s-%sTrack-pop%04d' %(ociType, trackType, numUnits)
                allAvgMaxGrades[numUnitsIdx, ociTypeIdx, trackTypeIdx, :]  = fromFile('%s/emc_%s_avgMaxGrades.bin' %(resultsDir, prefix)).data
                allAvgMeanGrades[numUnitsIdx, ociTypeIdx, trackTypeIdx, :] = fromFile('%s/emc_%s_avgMeanGrades.bin' %(resultsDir, prefix)).data
    
    
    
    # EXTRACT DATA
    
    avgMaxGradesPerPop = mean(mean(allAvgMaxGrades, axis=2), axis=1)
    avgMeanGradesPerPop = mean(mean(allAvgMeanGrades, axis=2), axis=1)
    allLastGenMaxGrades = allAvgMaxGrades[:, :, :, -1]
    allLastGenMeanGrades = allAvgMeanGrades[:, :, :, -1]
    lastGenMaxGrades = mean(mean(allLastGenMaxGrades, axis=2), axis=1)
    lastGenMeanGrades = mean(mean(allLastGenMeanGrades, axis=2), axis=1)
    
    
    def f0(x, a):
        return 1 - a ** (-log2(x))
    
    def f1(x, m, a):
        return m - m * a ** (-log2(x))
    
    def f2(x, m, a, b):
        return m - m * a ** (-log2(x + b))
    
    
    x = allNumUnits
    X = 2 ** arange(2, 14, 0.1)
    
    maxCoef0, _ = curve_fit(f0, x, lastGenMaxGrades, maxfev=10000)
    maxError0 = abs(lastGenMaxGrades - f0(x, *maxCoef0))
    meanCoef0, _ = curve_fit(f0, x, lastGenMeanGrades, maxfev=10000)
    meanError0 = abs(lastGenMeanGrades - f0(x, *meanCoef0))
    print 'f0 error', mean(maxError0), std(maxError0), mean(meanError0), std(meanError0)
    
    maxCoef1, _ = curve_fit(f1, x, lastGenMaxGrades, maxfev=10000)
    maxError1 = abs(lastGenMaxGrades - f1(x, *maxCoef1))
    meanCoef1, _ = curve_fit(f1, x, lastGenMeanGrades, maxfev=10000)
    meanError1 = abs(lastGenMeanGrades - f1(x, *meanCoef1))
    print 'f1 error', mean(maxError1), std(maxError1), mean(meanError1), std(meanError1)
    
    maxCoef2, _ = curve_fit(f2, x, lastGenMaxGrades, maxfev=10000)
    maxError2 = abs(lastGenMaxGrades - f2(x, *maxCoef2))
    meanCoef2, _ = curve_fit(f2, x, lastGenMeanGrades, maxfev=10000)
    meanError2 = abs(lastGenMeanGrades - f2(x, *meanCoef2))
    print 'f2 error', mean(maxError2), std(maxError2), mean(meanError2), std(meanError2)
    
    
    print ''
    print 'Max'
    print 'f1(1024)=%.3f, f1(2048)=%.3f, f1(4096)=%.3f, f1(8192)=%.3f' %(
           f1(1024, *maxCoef1), f1(2048, *maxCoef1), f1(4096, *maxCoef1), f1(8192, *maxCoef1)) 
    print 'delta_f1(2048,1024)=%.3f, delta_f1(4096,2048)=%.3f, delta_f1(8192,4096)=%.3f' %(
           f1(2048, *maxCoef1) - f1(1024, *maxCoef1),
           f1(4096, *maxCoef1) - f1(2048, *maxCoef1),
           f1(8192, *maxCoef1) - f1(4096, *maxCoef1))
    print 'Mean' 
    print 'f1(1024)=%.3f, f1(2048)=%.3f, f1(4096)=%.3f, f1(8192)=%.3f' %(
           f1(1024, *meanCoef1), f1(2048, *meanCoef1), f1(4096, *meanCoef1), f1(8192, *meanCoef1)) 
    print 'delta_f1(2048,1024)=%.3f, delta_f1(4096,2048)=%.3f, delta_f1(8192,4096)=%.3f' %(
           f1(2048, *meanCoef1) - f1(1024, *meanCoef1),
           f1(4096, *meanCoef1) - f1(2048, *meanCoef1),
           f1(8192, *meanCoef1) - f1(4096, *meanCoef1)) 
    print ''
    
    print 'Max:  f1 = %.3f * (1 - %.3f ^ (-log2(x)))' %(maxCoef1[0], maxCoef1[1])
    print 'Mean: f1 = %.3f * (1 - %.3f ^ (-log2(x)))' %(meanCoef1[0], meanCoef1[1])
    print 'Max:  f2 = %.3f * (1 - %.3f ^ (-log2(x) + %.3f))' %(maxCoef2[0], maxCoef2[1], maxCoef2[2])
    print 'Mean: f2 = %.3f * (1 - %.3f ^ (-log2(x) + %.3f))' %(meanCoef2[0], meanCoef2[1], meanCoef2[2])
    
    semilogx(x, lastGenMaxGrades, '*', markersize=12, color='#502010', label='Max grades')
    semilogx(x, lastGenMeanGrades, 'x', markeredgewidth=1.5, markersize=12, color='#305070', label='Mean grades')
    semilogx(X, f1(X, *maxCoef1), color='#A08060', label='Estimated max grades')
    semilogx(X, f1(X, *meanCoef1), color='#60A080', label='Estimated mean grades')
    
    xlabel('Population size', fontsize=20)
    ylabel('Fitness test grades', fontsize=20)
    legend(loc=4, fontsize=18)
    grid('on')
    xticks(2 ** arange(4,13))
    yticks(arange(0,1.1,0.1))
    gca().set_xticklabels(2 ** arange(4,13))
    xlim(8, 8192)
    ylim([0, 1])
    tight_layout()
    
    #savefig('popSizeEstimate.pdf')
    show()