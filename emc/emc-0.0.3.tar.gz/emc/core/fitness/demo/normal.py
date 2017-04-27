from matplotlib.pyplot import plot, show, bar, figure, \
    xlabel, ylabel, tight_layout
from numpy import histogram, arange, zeros, float32
from emc.core.integ.modeldir import ModelDirectory
from emc.core.fitness.corpus import CorpusBasedFitnessTestContainer


def plotNormal(data, ft):
    hist, histBins = histogram(data, bins = 20)
    histCenters = (histBins[:-1] + histBins[1:]) / 2
    histWidth = 0.5 * (histBins[1] - histBins[0])
    hist = hist.astype(float32) / max(hist)
    
    normX = arange(int(ft.mu * 2))
    normY = zeros(int(ft.mu * 2))
    for x in normX: normY[x] = ft.normalValueOf([x])
    
    bar(histCenters, hist, align='center', width=histWidth, label='Scaled histogram\nof corpus lengths', color='#706860')
    plot(normX, normY, 'k', linewidth=5, label='Deduced normal')
    #legend(fontsize=11)


if __name__ == '__main__':
    md = ModelDirectory('../../../../../../midi/bach_1track')
    ftc = CorpusBasedFitnessTestContainer(md)
    
    
    figure(figsize=(8,5))
    
    #subplot(1,2,1)
    plotNormal(md.lengths(), ftc.glft)
    #title("Length normal deduction by corpus")
    xlabel('Length (ticks)', fontsize=20)
    ylabel('Fitness', fontsize=20)
    
    tight_layout()
    
    '''
    subplot(1,2,2)
    plotNormal(md.numNotes(), ftc.gnnft)
    title("Number of notes normal deduction by corpus")
    xlabel('Number of notes')
    ylabel('Fitness')
    '''
    
    #savefig('corpusnormallength.pdf')
    show()