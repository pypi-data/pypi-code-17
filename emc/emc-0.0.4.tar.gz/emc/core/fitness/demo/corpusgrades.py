'''
Demo of changing number of clusters.

Given a model directory (corpus), we test the scores the models themselves
would get when tested, given we change the number of clusters used.

1 cluster means we always compare to the mean of all descriptors.
n clusters (for n models) means we compare to each of the descriptors, and
the minimal distance wins each time.

@author Csaba Sulyok
'''

from matplotlib.pyplot import plot, legend, xlabel, ylabel, show, ylim, tight_layout, grid
from numpy import set_printoptions, array, zeros, mean, argsort

from emc.core.integ.modeldir import ModelDirectory
from emc.cpp.wrapper.descriptor import DescriptorDirectoryWrapper

if __name__ == '__main__':
        
    set_printoptions(threshold='nan', precision=3, suppress=True)
    
    allNumClusters = array([1, 3, 5, 10, 20, 30])
    
    
    md = ModelDirectory('../../../../midi/bach_1track')
    modelGrades = zeros((md.models.size, allNumClusters.size))
    
    
    # precalculate sorting order
    dd = DescriptorDirectoryWrapper(md, numClusters = 1)
    
    for modelIdx, model in enumerate(md.models):
        modelGrades[modelIdx, 0] = mean(dd.modelFitness(model))
    
    sortingOrder = argsort(modelGrades[:,0])
    
    
    markers = ['o', '<', 'v', '>', 'v', 'd']
    colors = ['#903030',
              '#309030',
              '#303090',
              '#808040',
              '#804080',
              '#408080']
    
    for numClusterIdx, numClusters in enumerate(allNumClusters):
        dd = DescriptorDirectoryWrapper(md, numClusters = numClusters)
    
        for modelIdx, model in enumerate(md.models):
            modelGrades[modelIdx, numClusterIdx] = mean(dd.modelFitness(model))
        
        label = '%d cluster' %(numClusters)
        if numClusters > 1: label += 's'
        plot(modelGrades[:, numClusterIdx][sortingOrder], 
             linestyle=':', 
             marker=markers[numClusterIdx], 
             color=colors[numClusterIdx],
             label=label)
    
    
    grid('on')
    legend(loc=4, fontsize=18)
    
    #title("Similarity test results of corpus\n for different numbers of clusters", fontsize=22)
    xlabel("Model index from corpus", fontsize=20)
    ylabel("Fitness test results", fontsize=20)
    ylim([0, 1.1])
    
    tight_layout()
    
    #savefig('corpusgrades.pdf')
    show()