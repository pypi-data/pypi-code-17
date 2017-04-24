'''
Created on Mar 15, 2017

@author: nate
'''
from fdscli.model.admin.connectors.connector_domain_info import ConnectorDomainInfo

class ActiveDirectory(ConnectorDomainInfo):
    '''
    classdocs
    '''


    def __init__(self, an_id=None, a_name=None, enabled=True, domain_controllers=[],
        administrator="Administrator", administrator_password=None, ou=None, auth_engine=None):
        '''
        Constructor
        '''
        ConnectorDomainInfo.__init__(self, an_id, a_name, "AD", enabled)
        
        self.domain_controllers = domain_controllers
        self.administrator = administrator
        self.administrator_password = administrator_password
        self.ou = ou
        self.auth_engine = auth_engine
        
    @property
    def domain_controllers(self):
        return self.__domain_controllers
    
    @domain_controllers.setter
    def domain_controllers(self, controllers):
        self.__domain_controllers = controllers
        
    @property
    def administrator(self):
        return self.__administrator
    
    @administrator.setter
    def administrator(self, admin):
        self.__administrator = admin
    
    @property    
    def administrator_password(self):
        return self.__administrator_password
    
    @administrator_password.setter
    def administrator_password(self, admin_password):
        self.__administrator_password = admin_password
        
    @property
    def ou(self):
        return self.__ou
    
    @ou.setter
    def ou(self, an_ou):
        self.__ou = an_ou
        
    @property
    def auth_engine(self):
        return self.__auth_engine
    
    @auth_engine.setter
    def auth_engine(self, ae):
        self.__auth_engine = ae