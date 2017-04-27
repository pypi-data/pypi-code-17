'''
JSON serializer for web applications.
Dynamically adds URI to returned dicts.
@author Csaba Sulyok
'''

import json

from monitoring.monitor import monitorState
from emc.helper.serializeutils import fromDict, toDict, Serializer


def _decorateWithUris(objDict, uri):
    '''
    Parse dict recursively and add uri to each member.
    '''
    if isinstance(objDict, list):
        for idx, value in enumerate(objDict):
            uriIdx = value['uid'] if 'uid' in value else idx
            subUri = '%s.%d' %(uri, uriIdx)
            _decorateWithUris(value, subUri)
    elif isinstance(objDict, dict):
        innerListNames = []
        for name, value in objDict.iteritems():
            if isinstance(value, list):
                innerListNames.append(name)
            subUri = '%s.%s' %(uri, name)
            _decorateWithUris(value, subUri)
        objDict['uri'] = uri
        for name in innerListNames:
            objDict[name + '_uri'] = subUri = '%s.%s' %(uri, name)


def _removeUris(objDict):
    '''
    Remove URI fields from dict so it can then be properly
    deserialized.
    '''
    if isinstance(objDict, list):
        for _, value in enumerate(objDict):
            _removeUris(value)
    elif isinstance(objDict, dict):
        if 'uri' in objDict:
            del objDict['uri']
        for _, value in objDict.iteritems():
            _removeUris(value)


def toJsonWithUri(obj):
    '''
    Serialize to JSON, but before serializing converted dict,
    add URIs to each field.
    '''
    objDict = toDict(obj, preserveClassData = False)
    if 'currentUri' in monitorState:
        _decorateWithUris(objDict, monitorState['currentUri'])
    return json.dumps(objDict)


def fromJsonWithUri(jsonStr):
    '''
    Deserialize JSON, ommitting all URI values.
    '''
    objDict = json.loads(jsonStr)
    _removeUris(objDict)
    return fromDict(objDict, checkForClassData = False)


'''
Define extra serializer.
'''
jsonSerializerWithUri = Serializer(serializeMethod=toJsonWithUri, 
                                   deserializeMethod=fromJsonWithUri,
                                   contentType='application/json')