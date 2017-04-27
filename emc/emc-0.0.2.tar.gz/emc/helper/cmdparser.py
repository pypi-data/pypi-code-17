'''
Parse and limit command line arguments and return a dictionary based on it.
@author Csaba Sulyok
'''

from re import search
from sys import stderr, argv

from numpy import float32, int16, int32


# Transformer methods for command line arguments

def _leaveAsIs(value):     return value
def _castToInt16(value):   return int16(value)
def _castToInt32(value):   return int32(value)
def _castToInt(value):     return int(value)
def _castToFloat32(value): return float32(value)
def _castToBool(value):    return bool(value)

def _castToClass(value):
    '''
    Resolve a class based on its full name (module name included).
    '''
    # find last dot - module is before it
    lastDotIdx = value.rfind('.')
    
    # distinguish between local and external classes
    if lastDotIdx != -1:
        moduleName = value[:lastDotIdx]
    else:
        moduleName = '__main__'

    className = value[lastDotIdx+1:]
    
    #import module and class
    module = __import__(moduleName, globals(), locals(), className)
    clazz = getattr(module, className)
    return clazz


def _castToOciClass(value):
    return _castToClass("cpp.wrapper.oci.%soci.%sOciWrapper" %(value.lower(), value))

    
def parseCmdLine(argTransformMethods = {}):
    '''
    Parse system arguments to set properties of an algorithm
    Parse command-line options and return map and props to use in initializing a script.
    '''
    argsDict = {}
    
    for arg in argv[1:]:
        # search for pattern opt=value
        match = search('(.*)=(.*)', arg)
        
        if not match:
            stderr.write('Unrecognized program argument: %s\n' %arg)
        else:
            argKey = match.group(1)
            argValue = match.group(2)
            
            if argKey not in argTransformMethods:
                stderr.write('Unrecognized configuration key: %s\n' %argKey)
            else:
                argTransformMethod = argTransformMethods[argKey]
                print 'Configuring using argument key=%s, value=%s, method=%s' %(
                                     argKey, argValue, argTransformMethod.__name__)
                argValue = argTransformMethod(argValue)
                argsDict[argKey] = argValue
    
    print 'Final args dictionary', argsDict
    print ''
    return argsDict
        

