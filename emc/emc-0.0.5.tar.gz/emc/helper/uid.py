class UidDict(dict):
    '''
    A dict representing a list with UID indices.
    Can be used as a list, but indexes do not get reused/shifted.
    Data added to it must be classes with a 'uid' field.
    '''
    
    def __init__(self, dataType, *args, **kwargs):
        self._dataType = dataType
        self._nextUid = 0
        dict.__init__(self, *args, **kwargs)
    
    def append(self, data):
        if isinstance(data, dict):
            obj = self._dataType(**data)
        elif hasattr(data, '__dict__'):
            if type(data) is self._dataType:
                obj = data
            else:
                raise Exception('UidDict data types do not match. %s != %s' %(type(data), self._dataType))
        else:
            raise Exception('Only dicts and %s s can be appended to this UidDict' %(self._dataType))
            
        obj.uid = self._nextUid
        self[obj.uid] = obj
        self._nextUid += 1
        return obj
    
    def __getitem__(self, uid):
        return dict.__getitem__(self, int(uid))
        
    def __setitem__(self, uid, data):
        data.uid = int(uid)
        dict.__setitem__(self, data.uid, data)
        
    def __delitem__(self, uid):
        dict.__delitem__(self, int(uid))
    
    def __contains__(self, uid):
        return dict.__contains__(self, int(uid))
        
    def __iter__(self):
        for _, value in self.iteritems():
            yield value
