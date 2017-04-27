'''
Virtual machine which populates a model (musical piece, i.e. phenotype)
based on the code on a genetic string (genotype).
Executes genetic string and builds score from output.

@author: Csaba Sulyok
'''

from emc.core.core.model import Model
from emc.cpp.wrapper.modelbuilder import ModelBuilderWrapper
from emc.cpp.wrapper.oci.immediateoci import ImmediateOciWrapper
from emc.framework.core.model import PhenotypeRenderer
from tymed import tymedCls, tymed


@tymedCls
class VirtualMachine(PhenotypeRenderer):
    '''
    Virtual machine which populates a model (musical piece, i.e. phenotype)
    based on the code on a genetic string (genotype).
    Executes genetic string and builds score from output.
    '''
    
    def __init__(self,
                 opCodeInterpreter = None,
                 modelBuilder = None):
        '''
        Initialize the C++ wrappers we use.
        '''
        if opCodeInterpreter is None:
            opCodeInterpreter = ImmediateOciWrapper(flexibleMemSize = 65536, expectedOutputs = 2600,
                                                    haltAllowed = False, maxCommandsRatio = 2.0)
        if modelBuilder is None:
            modelBuilder = ModelBuilderWrapper()
            
        self.opCodeInterpreter = opCodeInterpreter
        self.modelBuilder = modelBuilder
        
    
    @tymed
    def run(self, geneticString):
        '''
        Builds new model with class' own arguments of sample rate and number of tracks,
        then executes genotype's code to fire events into the model.
        '''
        # step 1 - interpret genetic string and gather output
        vmResult = self.opCodeInterpreter.geneticStringToOutput(geneticString.data)
        # step 2 - build model based on genetic string output
        return self.modelBuilder.bytesToModel(Model, vmResult)
