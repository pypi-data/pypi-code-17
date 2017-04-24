'''
Created on Mar 15, 2017

@author: nate
'''
from fdscli.services.abstract_service import AbstractService
from fdscli.model.admin.connectors.active_directory import ActiveDirectory

class ConnectorDomainInfoService( AbstractService ):
    '''
    Created on Apr 23, 2015
    
    @author: nate
    '''
    
    def __init__(self, session):
        AbstractService.__init__(self, session)
        
    def set_configuration( self, cdi ):
        '''
        Set the state of the configuration
        '''
        
    def get_configuration(self):
        '''
        retrieve the configuration
        '''
        return ActiveDirectory()
        