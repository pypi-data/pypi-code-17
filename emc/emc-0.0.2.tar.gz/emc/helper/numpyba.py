'''
NumPy object to bytearray for more compressed serialization.

@author: Csaba Sulyok
'''
from numpy import float32, zeros, frombuffer


class NumpyArrayBA(object):
    
    def __init__(self, shape=None, data=None, dtype=float32):
        if shape is not None:
            self.data = zeros(shape, dtype=dtype)
        elif data is not None:
            self.data = data
        
    def __getitem__(self, key):
        return NumpyArrayBA(data = self.data.__getitem__(key))
    
    def __setitem__(self, key, value):
        return self.data.__setitem__(key, value)
    
    def __delitem__(self, key):
        return self.data.__delitem__(key)
    
    def __getstate__(self):
        return (self.data.shape, self.data.dtype, bytearray(self.data))
    
    def __setstate__(self, state):
        shape, dtype, dataBA = state
        self.data = frombuffer(dataBA, dtype=dtype)
        self.data.shape = shape
    
    def __str__(self):
        return self.data.__str__()
    
    def __repr__(self):
        return self.data.__str__()