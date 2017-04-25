'''
Created on Mar 15, 2017

@author: nate
'''
import json
from fdscli.model.admin.connectors.active_directory import ActiveDirectory
from fdscli.model.admin.connectors.kerberoes_auth_engine import KerberosAuthEngine

class ConnectorDomainInfoConverter(object):
    '''
    classdocs
    '''

    @staticmethod
    def to_json( cdi ):
        '''
        Convert connector domain into to json
        
        right now there is only one CDI implementation and only one
        auth implementation so assumptions will be made here.        
        '''
        
        j_dict = dict()
        j_dict["uid"] = cdi.id 
        j_dict["name"] = cdi.name
        j_dict["type"] = cdi.domain_type
        j_dict["enabled"] = cdi.enabled
        j_dict["domainControllers"] = cdi.domain_controllers
        j_dict["administrator"] = cdi.administrator
        j_dict["administratorPassword"] = cdi.administrator_password
        j_dict["ou"] = cdi.ou
        
        j_auth = dict()
        j_auth["type"] = cdi.auth_engine.auth_type
        j_auth["kdcServers"] = cdi.auth_engine.kdc_servers
        j_auth["realm"] = cdi.auth_engine.realm
        
        j_dict["authEngine"] = j_auth
        
        j_dict = json.dumps( j_dict )
        
        return j_dict
        
        
    @staticmethod
    def build_from_json( j_cdi ):
        '''
        Convert j_string to a full connector object
        
        right now there is only one CDI implementation and only one
        auth implementation so assumptions will be made here.
        '''
        
        cdi = ActiveDirectory()
        
        if not isinstance(j_cdi, dict):
            j_cdi = json.loads(j_cdi)
            
        cdi.id = j_cdi.pop( "uid", cdi.id )
        cdi.name = j_cdi.pop( "name", cdi.name )
        cdi.administrator = j_cdi.pop( "administrator", cdi.administrator )
        cdi.administrator_password = j_cdi.pop( "administratorPassword", cdi.administrator_password )
        cdi.ou = j_cdi.pop( "ou", cdi.ou )
        cdi.enabled = j_cdi.pop( "enabled", cdi.enabled )
        cdi.domain_controllers = j_cdi.pop( "domainControllers", cdi.domain_controllers )
        
        j_auth = j_cdi.pop( "authEngine", None )
        
        if j_auth is not None:
            engine = KerberosAuthEngine()
            engine.kdc_servers = j_auth.pop( "kdcServers", [] )
            engine.realm = j_auth.pop( "realm", None )
            cdi.auth_engine = engine
            
        return cdi