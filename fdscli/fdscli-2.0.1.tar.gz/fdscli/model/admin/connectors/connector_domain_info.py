'''
Created on Mar 15, 2017

@author: nate
'''
from fdscli.model.base_model import BaseModel

class ConnectorDomainInfo(BaseModel):
    '''
    classdocs
    '''


    def __init__(self, an_id=None, a_name=None, a_type="AD", enabled=True):
        '''
        Constructor
        '''
        
        BaseModel.__init__(self, an_id, a_name)
        
        self.__domain_type = a_type
        self.__enabled = enabled
        
    @property
    def domain_type(self):
        return self.__domain_type
    
    @domain_type.setter
    def domain_type(self, a_type):
        
        if a_type not in ("AD"):
            raise TypeError
        
        self.__domain_type = a_type
        
    @property
    def enabled(self):
        return self.__enabled
    
    @enabled.setter
    def enabled(self, is_it):
        self.__enabled = is_it