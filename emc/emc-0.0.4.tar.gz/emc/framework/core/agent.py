'''
Allows the starting of a watchdog agent,
which can manage run instances.
@author Csaba Sulyok
'''

import os
import socket
from datetime import datetime
from os.path import isfile
from subprocess import Popen
from sys import stderr
from time import time, sleep
from traceback import print_exc

from emc.helper.git import gitRevision
from monitoring.monitor import request, isPortListening
from emc.helper.reprdecorate import prettyPrint
from emc.helper.uid import UidDict

# null stream - redirect subprocess' outputs here
_devnull = open(os.devnull, 'w')


@prettyPrint
class Instance(object):
    '''
    Representation of an instance running under this agent's supervision.
    Can be started/stopped/paused/resumed and monitored from the exterior.
    '''
    
    def __init__(self, name, config, uid = None, gitRevision = None):
        self.uid = uid
        self.name = name
        self.monitorPort = None
        
        if isinstance(config, dict):
            self.config = config
        elif hasattr(config, '__dict__'):
            self.config = config.__dict__
        else:
            raise Exception('Config must be either a dict or a class')
        
        self.gitRevision = gitRevision
        self.processRunning = False
        self.data = None
    

    def start(self, mainScriptName, monitorPort, currentGitRevision):
        '''
        Start given instance.
        Will try to resume its previously started instance if there is a serialized file available.
        Otherwise will use local config to create a new run.
        '''
        if not self.processRunning:
            cmdArgs = ['python', mainScriptName]
            if isfile(self.name + '.emc'):
                if currentGitRevision is not self.gitRevision:
                    stderr.write('Cannot resume run from different git revision: %s!=%s' %(currentGitRevision, self.gitRevision))
                    return
                cmdArgs.append('fileToResume=%s.emc' %(self.fileName))
            else:
                cmdArgs.extend(['%s=%s'%(name, value) for name, value in self.config.iteritems()])
                
            self.monitorPort = monitorPort
            cmdArgs.append('monitorPort=%d' %(self.monitorPort))
            
            print 'Calling process', cmdArgs
            Popen(cmdArgs, shell=True, stdin=None, stdout=_devnull, stderr=_devnull)
            while not isPortListening(port = monitorPort):
                sleep(1)
            self.data = request('algorithm.data', port = self.monitorPort)
            self.processRunning = True
    
    
    def stop(self, saveFile = True):
        '''
        Stop instance if currently running.
        Also saves file optionally so it can be recalled later.
        '''
        if self.processRunning:
            if saveFile:
                request('pause', port = self.monitorPort, method = 'POST')
                # WAIT HERE FOR PAUSE?
                request('algorithm.save', port = self.monitorPort, method = 'POST', fileName = self.name + '.emc')
            request('exit', port = self.monitorPort, method = 'POST')
            self.processRunning = False
            self.monitorPort = None
    
    
    def pause(self):
        '''
        Signal instance to pause. Process remains in-memory.
        '''
        if self.processRunning:
            request('pause', port = self.monitorPort, method = 'POST')
    
    
    def resume(self):
        '''
        Signals resuming a paused instance.
        '''
        if self.processRunning:
            request('resume', port = self.monitorPort, method = 'POST')
    
    
    def _poll(self):
        '''
        Poll information of instance from its process.
        Asks for InstanceData serialized from the respective process.
        '''
        if self.processRunning:
            try:
                self.data = request('algorithm.data', port = self.monitorPort)
            except:
                print_exc()
                self.processRunning = False
                self.monitorPort = None
        
    

@prettyPrint
class Agent(object):
    '''
    An agent can monitor and maintain a set of instances all running on the local machine.
    Only one agent should be run per machine.
    '''
    
    def __init__(self, mainScriptName = 'emc-agent.bin', instanceStartPort = 12345):
        self.mainScriptName = mainScriptName
        self.instanceStartPort = instanceStartPort
        
        self.instances = UidDict(dataType = Instance)
        self.gitRevision = gitRevision()
        self.name = socket.gethostname()
    
    
    def __getstate__(self):
        return (self.mainScriptName, self.instanceStartPort, self.instances, self.name)
    
    
    def __setstate__(self, state):
        self.mainScriptName, self.instanceStartPort, self.instances, self.name = state
        self.gitRevision = gitRevision()
    
    
    def createInstance(self, config):
        '''
        Can be externally called using a config dict.
        Creates a new instance which it will then monitor.
        '''
        timeStamp = datetime.fromtimestamp(time()).strftime('%Y%m%d-%H%M%S')
        name = 'emc_host%s_time%s_rev%s' %(self.name, timeStamp, self.gitRevision)
        newInstance = Instance(name = name, config = config, gitRevision = self.gitRevision)
        self.instances.append(newInstance)
        newInstance.start(self.mainScriptName, self._nextAvailablePort(), self.gitRevision)
        return newInstance
    
    
    def _pollInstances(self):
        '''
        Poll changing data from each maintained emc subprocess.
        '''
        for instance in self.instances:
            instance._poll()


    def _nextAvailablePort(self):
        '''
        Find available port where new instance can be set to be monitored.
        '''
        ret = self.instanceStartPort
        while isPortListening(port = ret):
            ret += 1
        return ret
    