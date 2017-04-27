'''
Parse command line options and configure an algorithm run
based on it.
@author Csaba Sulyok
'''

from emc.helper.cmdparser import parseCmdLine, _leaveAsIs, _castToInt, _castToFloat32, \
    _castToBool, _castToInt16, _castToOciClass



def parseForEmcAlgRun():   
    return parseCmdLine({
                  
        # corpus-based fitness test container
        'corpusPath' : _leaveAsIs,
        'numClusters' : _castToInt,
        'alpha' : _castToFloat32,
        'gamma' : _castToFloat32,
        'expectedLength' : _castToFloat32,
        
        # OCI
        'ociClass' : _castToOciClass,
        'memSizeInBytes' : _castToInt,
        'maxCommandsRatio' : _castToFloat32,
        'haltAllowed' : _castToBool,
        
        # population breeder
        'numUnits' : _castToInt,
        'survivalRate' : _castToFloat32,
        
        # general algorithm props
        'targetGeneration' : _castToInt16,
        'numberOfRuns' : _castToInt16,
        'loggingCycle' : _castToInt16,
        
        # saving
        'fileToResume' : _leaveAsIs,
        'savePeriodically' : _castToBool,
        'outputDir' : _leaveAsIs,
        'cycleSize' : _castToInt16,
        
        # monitoring
        'monitorPort' : _castToInt16
        
    })


def parseForEmcAgent():   
    return parseCmdLine({
        'agentFileName' : _leaveAsIs,
        'mainScriptName' : _leaveAsIs,
        'monitorPort' : _castToInt,
        'instanceStartPort' : _castToInt,
        'pollPeriod' : _castToInt
    })
