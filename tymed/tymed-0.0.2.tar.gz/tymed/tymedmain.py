'''
Timer utility for functions and bound methods.
Annotate a function to activate timing for it.
The execution will be incrementally timed for every iteration, until consumed using the lap method.

@author: Csaba Sulyok <csaba.sulyok@gmail.com>
'''

from time import time
import inspect


def _id(mtd):
    '''
    The ID scheme we use for a function.
    If regular function, use it's Python ID.
    If bound function, use concatenation of its object's ID and it's own.
    '''
    if not hasattr(mtd, '__origMtd__'):
        raise FunctionNotTymedException(mtd)
    
    if hasattr(mtd, '__self__'):
        return "%d.%d" %(id(mtd.__origMtd__), id(mtd.__self__))
    else:
        return "%d" %(id(mtd.__origMtd__))
    
    
    
class TymedMethod(object):
    
    def __init__(self, mtdId):
        self.mtdId = mtdId
        self.lastStartedAt = 0.0
        self.lastTyme = 0.0
        self.allTyme = 0.0
    
    def reset(self):
        self.lastStartedAt = 0.0
        self.lastTyme = 0.0
        self.allTyme = 0.0
        


class TymedMethodContainer(dict):
    
    def __getitem__(self, mtd = None):
        '''
        Access method based on method ID or method itself.
        '''
        
        if isinstance(mtd, str):
            mtdId = mtd
        else:
            mtdId = _id(mtd)
            
        if not self.has_key(mtdId):
            if self.has_key(mtdId.split('.')[0]):
                raise BoundMethodNotInTymedClassException(mtd)
            self.__setitem__(mtdId, TymedMethod(mtdId))
            
        return dict.__getitem__(self, mtdId)
    
    
    def __delitem__(self, mtd = None):
        '''
        Delete method based on method ID or method itself.
        '''
        tymedMtd = self.__getitem__(mtd)
        if tymedMtd:
            return dict.__delitem__(self, tymedMtd.mtdId)
        
    

class TymedMethodController(object):
    '''
    Annotate a method to activate timing for it.
    The function's execution will be incrementally timed for every iteration,
    until consumed using the lap method.
    '''
        
    def __init__(self):
        self.mtds = TymedMethodContainer()
        
    def onMtdStart(self, mtdId):
        self.mtds[mtdId].lastStartedAt = time()
    
    def onMtdFinish(self, mtdId):
        self.mtds[mtdId].lastTyme = time() - self.mtds[mtdId].lastStartedAt
        self.mtds[mtdId].allTyme += self.mtds[mtdId].lastTyme
    
    def lastTyme(self, mtdId):
        return self.mtds[mtdId].lastTyme
    
    def allTyme(self, mtdId):
        return self.mtds[mtdId].allTyme
    
    def resetTyme(self, mtdId = None):
        if mtdId:
            del self.mtds[mtdId]
        else:
            self.mtds.clear()
    
    def lap(self, mtdId):
        ret = self.mtds[mtdId].allTyme
        self.resetTyme(mtdId)
        return ret


# default instance & methods
_defaultTymedMethodController = TymedMethodController()

lastTyme = _defaultTymedMethodController.lastTyme
allTyme = _defaultTymedMethodController.allTyme
resetTyme = _defaultTymedMethodController.resetTyme    
lap = _defaultTymedMethodController.lap


def tymedCls(cls):
    for _, val in cls.__dict__.iteritems():
        if callable(val) and hasattr(val, '__tymed__'):
            val.__boundtymed__ = True
               
    return cls

    
def tymed(mtd):
    def wrappedMtd(*args, **kwargs):
        if hasattr(wrappedMtd, '__boundtymed__'):
            mtdId = "%d.%d" %(id(mtd), id(args[0]))
        else:
            mtdId = "%d" %(id(mtd))
            
        _defaultTymedMethodController.onMtdStart(mtdId)
        try:
            ret = mtd(*args, **kwargs)
        finally:
            _defaultTymedMethodController.onMtdFinish(mtdId)
        
        return ret
    
    wrappedMtd.__tymed__ = True
    wrappedMtd.__origMtd__ = mtd
    return wrappedMtd



class FunctionNotTymedException(Exception):
    
    def __init__(self, mtd):
        self.mtd = mtd
        self.message = "Following item not tymed: " + str(self.mtd)
        
    def __repr__(self):
        return self.message
    
    

class BoundMethodNotInTymedClassException(Exception):
    
    def __init__(self, mtd):
        self.mtd = mtd
        self.message = "Following bound method part of non-tymed class: " + str(self.mtd) + ". Please annotate class with @tymedCls"
        
    def __repr__(self):
        return self.message
    