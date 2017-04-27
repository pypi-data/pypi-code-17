'''
Wrapper for cPickle & json,
cPickle is a fast C-based file serializer based on Python's pickle.
JSON is slower but is needed for web.
Contains utility methods to serialize/deserialize arbitrary objects
to/from binary format.

@author Csaba Sulyok
'''

import cPickle
import json

from emc.helper.uid import UidDict


def toDict(obj, preserveClassData = True):
    '''
    Create dict from arbitrary object.
    If a class instance is found, it is dictified together with its module & class name.
    '''
    if isinstance(obj, list):
        ret = obj[:]
        # recurse through list members to dictify children
        for idx, value in enumerate(ret):
            ret[idx] = toDict(value, preserveClassData)
    elif isinstance(obj, UidDict):
        ret = obj.copy().values()
        # handle UidDict as list so Knockout can observe it
        for idx, value in enumerate(ret):
            ret[idx] = toDict(value, preserveClassData)
    elif isinstance(obj, dict):
        ret = obj.copy()
        # recurse through dict members to dictify children
        for name, value in ret.iteritems():
            ret[name] = toDict(value, preserveClassData)
    elif hasattr(obj, '__dict__'):
        # if class instance, save class name in dict
        ret = obj.__dict__.copy()
        # recurse through dict members to dictify children which are class instances
        for name, value in ret.iteritems():
            ret[name] = toDict(value, preserveClassData)
        # code in class data to json if needed
        if preserveClassData:
            ret['__moduleName__'] = obj.__module__
            ret['__className__'] = obj.__class__.__name__
    else:
        ret = obj
        
    return ret
    
    
def fromDict(objDict, checkForClassData = True):
    '''
    Inverse of toDict, takes a dict and finds members with module & class names,
    and builds their instances.
    '''
    if isinstance(objDict, list):
        ret = objDict[:]
        # recurse through list members to de-dictify children
        for idx, value in enumerate(ret):
            ret[idx] = fromDict(value, checkForClassData)
    elif isinstance(objDict, dict):
        ret = objDict.copy()
        
        # iterate through children first
        for name, value in ret.iteritems():
            ret[name] = fromDict(value, checkForClassData)
        
        # check if class & module name given, otherwise it's just an actual dict
        if checkForClassData and '__className__' in ret:
            # find module & class declared in dict, and load it
            module = __import__(ret['__moduleName__'], globals(), locals(), ret['__className__'])
            clazz = getattr(module, ret['__className__'])
            
            # remove extra fields from dict and call constructor using what remains
            del ret['__moduleName__']
            del ret['__className__']
            
            obj = clazz()
            for name, value in ret.iteritems():
                if hasattr(obj, name):
                    setattr(obj, name, value)
                else:
                    raise Exception('Cannot deserialize: %s has no member %s' %(clazz, name))
            ret = obj
    else:
        ret = objDict
    
    return ret
    

def toJson(obj):
    '''
    Serialize to JSON.
    Change classes to dicts.
    '''
    return json.dumps(toDict(obj))


def fromJson(jsonStr):
    '''
    Deserialize from JSON
    Builds classes held in JSON dicts.
    '''
    return fromDict(json.loads(jsonStr))
    
        
def toString(obj):
    '''
    Serialize object.
    '''
    return cPickle.dumps(obj)


def fromString(string):
    '''
    Deserializes object.
    '''
    return cPickle.loads(string)


def toFile(obj, filename, mode = 'wb'):
    '''
    Serializes object and writes to file.
    '''
    _file = open(filename, mode)
    cPickle.dump(obj, _file)
    

def fromFile(filename, mode = 'rb'):
    '''
    Deserializes object from file.
    Reads and decodes.
    '''
    _file = open(filename, mode)
    return cPickle.load(_file)



class Serializer(object):
    '''
    General class describing serializing behavior.
    Must be given functions as arguments.
    '''
    def __init__(self, serializeMethod, deserializeMethod, contentType):
        self.serializeMethod = serializeMethod
        self.deserializeMethod = deserializeMethod
        self.contentType = contentType
    
    def _to(self, obj):
        return self.serializeMethod(obj)
    
    def _from(self, objStr):
        return self.deserializeMethod(objStr)
        

'''
Define basic serializers which can be used in web services.
'''
pickleSerializer = Serializer(serializeMethod=toString, 
                              deserializeMethod=fromString,
                              contentType='text/cPickle')

jsonSerializer = Serializer(serializeMethod=toJson, 
                            deserializeMethod=fromJson,
                            contentType='application/json')