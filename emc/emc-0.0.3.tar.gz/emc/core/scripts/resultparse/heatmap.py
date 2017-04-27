from matplotlib.pyplot import *
from numpy import *

from os import chdir
from os.path import abspath, dirname

from emc.cpp.swig.emcpp import randomByteArray
from emc.helper.serializeutils import fromFile
from emc.core.integ.midi import writeToMidi
from emc.core.core.model import Model
from emc.cpp.wrapper.oci.immediateoci import ImmediateOciWrapper


set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)},
                 linewidth=150)


def heatmap(values, gamma = 1.0, figName = None):
    
    figure(figsize=(5,5))
    
    s = round_(sqrt(values.shape[0]))
    values = values.astype(float32)
    values = values ** gamma
    values /= values.max()
    
    if len(values.shape) > 1:
        l = values.shape[1]
        values.shape = (s, s, values.shape[1])
    else:
        l = 1
        values.shape = (s, s)
    
    grid('on')
    
    # put the major ticks at the middle of each cell
    ticks = arange(s).astype(uint8)
    gca().set_xticks(ticks + 0.5)
    gca().set_yticks(ticks + 0.5)
    
    # invert
    gca().invert_yaxis()
    gca().xaxis.tick_top()
    gca().xaxis.set_label_position('top')
    #xticks(rotation=90)
    #yticks(rotation=90)
    rcParams.update({'font.size': 24})
    
    # hex tick labels
    #title('High byte', fontsize=32, y=1.15)
    #+ylabel('Low byte', fontsize=32)
    
    labels = array([r'{:01x}'.format(i) for i in ticks])
    labels[1::2] = r''
    gca().set_xticklabels(labels, minor=False, fontdict={'family':'monospace'})
    gca().set_yticklabels(labels, minor=False, fontdict={'family':'monospace'})
    
    if l is 1:
        pcolor(values, cmap = cm.Greys, alpha = 0.8)
    else:
        cmaps = [cm.Reds, cm.Greens, cm.Blues]
        for i in arange(l):
            pcolor(values[:,:,i], cmap = cmaps[i], alpha = 0.8)
            
    tight_layout(pad=0.1)
    
    if figName:
        savefig(figName)
    

if __name__ == '__main__':
    
    gamma = .5
    
    chdir(abspath("%s/../../.." % (dirname(__file__))))
    alg = fromFile('/media/csaba/emc/2017-04-ecal/emc-ecal2017-ociImmediate-mem256/emc_time20170408-134127_revf23ef1b/alg/emc_gen09999.emc')
    bestModelIdx = argmax(alg.population.grades)
    data = alg.population.genotypes[bestModelIdx].data
    oci = alg.phenotypeRenderer.opCodeInterpreter
    _, touched = oci.geneticStringToTouched(data)
    heatmap(touched, gamma=gamma, figName='heatmaplast.pdf')
    
    
    N = 1000
    numTouched = zeros(N)
    oci = ImmediateOciWrapper(256, 760, False, 8.0)
    for i in arange(N):
        data = randomByteArray(oci.geneticStringSize)
        numTouched[i], touched = oci.geneticStringToTouched(data)
        #print numTouched
        #print ','.join(["%d" %t for t in touched])
        #heatmap(touched, gamma = gamma)
        
    expectedNumTouched = mean(numTouched)
    for i in arange(N):
        data = randomByteArray(oci.geneticStringSize)
        numTouched, touched = oci.geneticStringToTouched(data)
        if abs(numTouched - expectedNumTouched) <= 1:
            #print numTouched
            print ','.join(["%d" %t for t in touched])
            heatmap(touched, gamma = gamma)
    
    
    # generated above    
    touched = array([5,4,6,4,1,3,4,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,2,0,0,0,1,1,1,1,1,1,1,1,2,3,2,3,1,0,0,0,0,0,1,2,1,2,1,2,1,2,0,1,4,5,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,1,2,0,0,0,0,0,0,2,4,2,4,0,0,0,0,0,1,2,1,2,0,0,0,0,1,1,1,1,1,1,1,4,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,2,2,4,2,4,0,0,0,1,3,3,3,2,0,0,0,0,0,0,0,0,0,0,1,3,3,3,2,0,0,1,2,1,2,35,35,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,0,2,5,4,38,35,34,34,35,35,35,35,35,35,35,35,36,36,1,1,1,1,0,0,0,0,1,2,1,1,0,0,1,2,1,2,0,0,2,4,3,4,1,3,2,1,2,0,0,1,2,1,2,0,0,0,0,0,0,0,2])
    heatmap(touched, gamma=gamma, figName='heatmaprnd.pdf')
    #show()
