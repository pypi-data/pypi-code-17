'''
Parsing mean/max results, plotting diagrams
'''

from django.conf import settings
from django.template.base import Template
from django.template.context import Context
from matplotlib.pyplot import *
from numpy import *

from emc.helper.serializeutils import fromFile


if __name__ == '__main__':
    resultsDir = '/media/csaba/emc/2017-04-ecal/fitness'
    numGens = 10000
    numUnits = 1024
    numRuns = 20
    
    allOciTypes = ['Immediate', 'SingleRisc', 'Stack']
    allArchTypes = ['VonNeumann', 'Harvard'] # '' = Von Neumann
    allMemSizes = [256, 4096, 65536]
    
    markers = ['o', '*', 'v', 'd', '>', 'v', '<', '^']
    colors = ['#a07060', '#7060a0', '#60a070']
    stdColors = ['#f0e0d0', '#e0d0f0', '#d0f0e0']
    
    ociTypesSize = size(allOciTypes)
    archTypesSize = size(allArchTypes)
    memSizesSize = size(allMemSizes)
    
    allAvgMaxGrades = zeros((ociTypesSize, archTypesSize, memSizesSize, numGens), dtype=float32)
    allAvgMeanGrades = zeros((ociTypesSize, archTypesSize, memSizesSize, numGens), dtype=float32)
    allAvgStdGrades = zeros((ociTypesSize, archTypesSize, memSizesSize, numGens), dtype=float32)
    #allMaxGrades = zeros((ociTypesSize, archTypesSize, memSizesSize, numRuns, numGens), dtype=float32)
    #allMeanGrades = zeros((ociTypesSize, archTypesSize, memSizesSize, numRuns, numGens), dtype=float32)
    #allStdGrades = zeros((ociTypesSize, archTypesSize, memSizesSize, numRuns, numGens), dtype=float32)
    
    
    # READ RESULTS FILES
    
    for ociTypeIdx, ociType in enumerate(allOciTypes):
        for archTypeIdx, archType in enumerate(allArchTypes):
            for memSizeIdx, memSize in enumerate(allMemSizes):
                
                if archType =='VonNeumann':
                    archTypeFileName = ''
                else:
                    archTypeFileName = archType
                    
                prefix = 'emc-ecal2017-oci%s%s-mem%d' %(ociType, archTypeFileName, memSize)
                
                print 'Reading', prefix
                allAvgMaxGrades[ociTypeIdx, archTypeIdx, memSizeIdx, :]  = fromFile('%s/%s-avgMaxGrades.bin'  %(resultsDir, prefix)).data
                allAvgMeanGrades[ociTypeIdx, archTypeIdx, memSizeIdx, :] = fromFile('%s/%s-avgMeanGrades.bin' %(resultsDir, prefix)).data
                allAvgStdGrades[ociTypeIdx, archTypeIdx, memSizeIdx, :]  = fromFile('%s/%s-avgStdGrades.bin'  %(resultsDir, prefix)).data
                #allMaxGrades[ociTypeIdx, archTypeIdx, memSizeIdx, :, :]  = fromFile('%s/%s-maxGrades.bin'  %(resultsDir, prefix)).data
                #allMeanGrades[ociTypeIdx, archTypeIdx, memSizeIdx, :, :] = fromFile('%s/%s-meanGrades.bin' %(resultsDir, prefix)).data
                #allStdGrades[ociTypeIdx, archTypeIdx, memSizeIdx, :, :]  = fromFile('%s/%s-stdGrades.bin'  %(resultsDir, prefix)).data
    
    
    # EXTRACT DATA FOR FIGURES
    
    avgMaxGradesPerOciType = mean(mean(allAvgMaxGrades, axis=2), axis=1)
    avgMeanGradesPerOciType = mean(mean(allAvgMeanGrades, axis=2), axis=1)
    avgStdGradesPerOciType = mean(mean(allAvgStdGrades, axis=2), axis=1)
    avgMaxGradesPerArchType = mean(mean(allAvgMaxGrades, axis=2), axis=0)
    avgMeanGradesPerArchType = mean(mean(allAvgMeanGrades, axis=2), axis=0)
    avgStdGradesPerArchType = mean(mean(allAvgStdGrades, axis=2), axis=0)
    avgMaxGradesPerMemSize = mean(mean(allAvgMaxGrades, axis=1), axis=0)
    avgMeanGradesPerMemSize = mean(mean(allAvgMeanGrades, axis=1), axis=0)
    avgStdGradesPerMemSize = mean(mean(allAvgStdGrades, axis=1), axis=0)
    lastGenMaxGrades = allAvgMaxGrades[:, :, :, -1]
    lastGenMeanGrades = allAvgMeanGrades[:, :, :, -1]
    lastGenStdGrades = allAvgStdGrades[:, :, :, -1]
    #allLastGenMaxGrades = allMaxGrades[:, :, :, :, -1]
    #allLastGenMeanGrades = allMeanGrades[:, :, :, :, -1]
    #allLastGenStdGrades = allStdrades[:, :, :, :, -1]
    
    
    # PRINT FIGURES
    
    x = arange(0, numGens, 50)
    X = arange(0, numGens, 500)
    
    
    def plotOne(labels,
                maxData = None,
                meanData = None,
                stdData = None,
                pdfName = None):
        figure()
        
        if maxData is not None:
            for idx, label in enumerate(labels):
                plot(x, maxData[idx, x],
                     color=colors[idx])
                plot(X, maxData[idx, X],
                     label='Max %s' %(labels[idx]), 
                     linestyle=' ',
                     color=colors[idx],
                     marker=markers[2*idx],
                     markersize=8)
        
        if meanData is not None:
            for idx, label in enumerate(labels):
                plot(x, meanData[idx, x],
                     color=colors[idx],
                     linestyle='--')
                plot(X, meanData[idx, X],
                     label='Mean %s' %(labels[idx]), 
                     linestyle=' ',
                     color=colors[idx],
                     marker=markers[2*idx+1],
                     markersize=8)
                
                if stdData is not None:
                    fill_between(x, meanData[idx, x] - stdData[idx, x],
                                    meanData[idx, x] + stdData[idx, x],
                                    color=colors[idx],
                                    alpha=0.1)
                 
        grid('on')
        xticks(arange(0,10001,1000))
        yticks(arange(0,1.3,0.1))
        
        xlabel('Generation index', fontsize=20)
        ylabel('Fitness test grades', fontsize=20)
        ylim([0, 1])
        
        legend(loc=2, ncol=1, numpoints=1,
               fontsize=18,
               framealpha = 0.5,
               labelspacing = 0.2)
        tight_layout()
        
        if pdfName:
            savefig(pdfName)
        else:
            pass
            #show()

    # FIGURE 1: mean/max based on memory
    '''
    plotOne(maxData = avgMaxGradesPerMemSize,
            meanData = avgMeanGradesPerMemSize,
            labels = allMemSizes,
            pdfName = 'resultsByMemSize.pdf')
    show()
    '''


    # FIGURE 2: bar graph for OCI types
    
    lastGenMaxGradesByOciType = mean(lastGenMaxGrades, axis=2)
    lastGenMaxGradesByOciType.shape = (ociTypesSize * archTypesSize)
    lastGenMeanGradesByOciType = mean(lastGenMeanGrades, axis=2)
    lastGenMeanGradesByOciType.shape = (ociTypesSize * archTypesSize)
    lastGenStdGradesByOciType = mean(lastGenStdGrades, axis=2)
    lastGenStdGradesByOciType.shape = (ociTypesSize * archTypesSize)
    
    
    figure()
    y = array([1, 0, -1])
    y = array([1.05, 0.65, 0.05, -0.35, -0.95, -1.35])
    
    barh(y + 0.05, lastGenMaxGradesByOciType,
         height=0.2, color='#c0c0f0', linewidth=2, linestyle='--')
    
    barh(y, lastGenMeanGradesByOciType,
         height=0.3, color='#80a080', linewidth=2,
         xerr=lastGenStdGradesByOciType, ecolor='#aa0000', capsize=10, 
         error_kw={'elinewidth':3, 'capthick':3} )
    
    
    yticks(y+0.15, ['Complex VN', 'Complex Harvard', 'Single VN', 'Single Harvard', 'Stack VN', 'Stack Harvard'])
    ylim([-1.5,1.5])
    xlim([0,1])
    
    xlabel('Grades', fontsize=20)
    
    for tick in gca().yaxis.get_major_ticks():
        tick.label.set_fontsize(18)
            
    tight_layout()
    savefig('results.pdf')
    show()
    
    
    
    # LATEX TABLE OF AVERAGE LAST GEN MAX/MEAN GRADES
    
    settings.configure()
    context = Context({'maxGrades' : lastGenMaxGrades,
                       'meanGrades' : lastGenMeanGrades,
                       'stdGrades' : lastGenStdGrades,
                       'caption' : 'Caption here',
                       'label' : 'results'})
                       
    texTemplate = Template(open('maxmeantable.text', 'rb').read())
    htmlTemplate = Template(open('maxmeantable.htmlt', 'rb').read())
    print texTemplate.render(Context(context))
    #print htmlTemplate.render(Context(context))
    
