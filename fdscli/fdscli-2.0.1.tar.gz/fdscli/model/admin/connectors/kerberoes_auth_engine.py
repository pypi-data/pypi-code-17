'''
Created on Mar 15, 2017

@author: nate
'''
from fdscli.model.admin.connectors.auth_engine import AuthEngine

class KerberosAuthEngine(AuthEngine):
    '''
    classdocs
    '''


    def __init__(self, kdc_servers=[], realm=None):
        '''
        Constructor
        '''
        AuthEngine.__init__(self, "KERBEROS")
        self.kdc_servers = kdc_servers
        self.realm= realm
        
    @property
    def kdc_servers(self):
        return self.__kdc_servers
    
    @kdc_servers.setter
    def kdc_servers(self, servers):
        self.__kdc_servers = servers
        
    @property
    def realm(self):
        return self.__realm
    
    @realm.setter
    def realm(self, a_realm):
        self.__realm = a_realm