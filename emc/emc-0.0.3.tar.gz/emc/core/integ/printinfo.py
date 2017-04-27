'''
Print info/help on process.
'''


def printMainHeader():
    print '''EMC - Evolutionary Music Composition
------------------------------------
    '''
    

def printAgentHeader():
    print '''Agent for EMC - Evolutionary Music Composition
----------------------------------------------
    '''
    
        
def printMainHelp():
    print '''A program that uses genetic programming to create pieces of music. Call as:

    emc [-h] [<optionKey>=<optionValue>]

Options:
    KEY               DESCRIPTION
    
    corpusPath        Folder containing corpus MIDI files
    numClusters       Number of corpus clusters
    expectedLength    Expected length (in seconds) of output musical pieces
    ociClass          Python class name of OCI interpreter.
    memSizeInBytes    Size of flexible memory (RAM/ROM) used in opcode interpretation.
    maxCommandsRatio  Maximum ratio of VM instructions to be executed relative to expected number for output instructions 
    numUnits          Population size 
    maxAge            Maximum times any unit may be survived
    survivalProb      Weight of survival probability applied to overall grades
    targetGeneration  The algorithm will run until it reaches this target generation.
    numberOfRuns      How many times the algorithm shall be run
    fileToResume      Resume previous run stored in given file. Everything else ignored in this case
    savePeriodically  Flag signalling whether to store models/MIDI files or not
    outputDir         Folder to store output models/MIDI files (savePeriodically must be set)
    cycleSize         Save status/best MIDI file every cycleSize generations (savePeriodically must be set)
    loggingCycle      Print status information every loggingCycle generations
    monitorPort       If set, process is monitorable through http calls to this port
'''
    
    
def printAgentHelp():
    print '''An agent that maintains multiple instances of emc algrun running on local machine.
Uses http calls towards methods and can also be polled via http.

    emc-agent [-h] [<optionKey>=<optionValue>]

Options:
    KEY               DESCRIPTION
    
    agentFileName     File where to load/save the agent's configuration
    mainScriptName    Name of main script to call when launching instances
    monitorPort       Port where the agent itself can be monitored
    instanceStartPort Port assigned to first monitored instance, then incremented for each new one 
    pollPeriod        Number of seconds for loop polling all running instances for their data
'''