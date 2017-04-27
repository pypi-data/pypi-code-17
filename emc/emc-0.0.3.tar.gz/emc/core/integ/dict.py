'''
@author: Csaba Sulyok
'''

class DDict:
    '''
    Dynamic dictionary class.
    Like a dict but with dot access.
    '''
    def __init__(self, **kwds):
        self.__dict__.update(kwds)