from matplotlib.pyplot import plot, show
from numpy import zeros, float32, arange, sort

from emc.core.core.model import Model
from emc.core.integ.modeldir import ModelDirectory
from emc.cpp.wrapper.descriptor import DescriptorDirectoryWrapper, normalize
from emc.cpp.wrapper.modelbuilder import ModelBuilderWrapper
from emc.cpp.wrapper.oci.immediateoci import ImmediateOciWrapper
from emc.cpp.swig.emcpp import randomByteArray


if __name__ == '__main__':
    
    md = ModelDirectory('../../../../midi/bach_1track')
    dd = DescriptorDirectoryWrapper(md, numClusters = 30, gamma = 1.0)
    oci = ImmediateOciWrapper(25000, 2500, False)
    mb = ModelBuilderWrapper(numTracks = 1)
    
    num = 1000
    geneticStringSize = oci.geneticStringSize 
    
    best_model = None
    best_grade = -1.0
    
    grades = zeros(num, dtype=float32)
    
    for i in arange(num):
        data = randomByteArray(geneticStringSize)
        vmResult = oci.geneticStringToOutput(data)
        model = mb.bytesToModel(Model, vmResult)
        grades[i] = dd.modelFitness(model)[0, 8]
        if grades[i] > best_grade:
            best_grade = grades[i]
            best_model = model
    
    
    print sort(grades)[:-10:-1]
    
    good_model = md.models[16]
    
    good_model_pitch = dd.descriptor(good_model)[0, 8,:]
    normalize(good_model_pitch)
    best_model_pitch = dd.descriptor(best_model)[0, 8,:]
    normalize(best_model_pitch)
    
    plot(good_model_pitch)
    plot(best_model_pitch)
    show()
