'''
Created on Mar 15, 2017

@author: nate
'''

class AuthEngine(object):
    '''
    classdocs
    '''


    def __init__(self, a_type="KERBEROS"):
        '''
        Constructor
        '''
        
        self.__type = a_type
        
    @property
    def auth_type(self):
        return self.__type
    
    @auth_type.setter
    def auth_type(self, a_type):
        self.__type = a_type
        