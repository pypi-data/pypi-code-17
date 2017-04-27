'''
Created on Feb 24, 2015

@author: Administrator
'''
from matplotlib.pyplot import plot, show
from numpy import mean, std, zeros, float32, arange, histogram

from emc.core.core.model import Model
from emc.core.fitness.normal import GivenNumNotesFitnessTest
from emc.core.integ.cd import cdr
from emc.core.integ.modeldir import ModelDirectory
from emc.cpp.swig.emcpp import randomByteArray
from emc.cpp.wrapper.modelbuilder import ModelBuilderWrapper
from emc.cpp.wrapper.oci.immediateoci import ImmediateOciWrapper


if __name__ == '__main__':
        
    cdr()
    md = ModelDirectory('../../../midi/bach_1track')
    gnnft = GivenNumNotesFitnessTest(mu  =  mean(md.numNotes(), axis=0),
                                     sig =  std (md.numNotes(), axis=0))
    print gnnft.mu
    
    oci = ImmediateOciWrapper(25000, 2600, True)
    mb = ModelBuilderWrapper(numTracks = md.numTracks)
    
    num = 1000
    
    grades = zeros(num, dtype=float32)
    
    for i in arange(num):
        data = randomByteArray(oci.geneticStringSize)
        
        vmResult = oci.geneticStringToOutput(data)
            
        model = mb.bytesToModel(Model, vmResult)
        grades[i] = gnnft.normalValueOf(model.numNotes())
    
    
    hist = histogram(grades)
    plot(hist[1][:-1], hist[0])
    show()
