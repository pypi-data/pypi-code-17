'''
Created on Mar 15, 2017

@author: nate
'''
from fdscli.model.admin.connectors.active_directory import ActiveDirectory
from fdscli.model.admin.connectors.kerberoes_auth_engine import KerberosAuthEngine
from fdscli.utils.converters.admin.connectors.connector_domain_info_converter import ConnectorDomainInfoConverter
from mock import patch
from test.base_cli_test import BaseCliTest

class TestConnectorDomainInfo(BaseCliTest):

    test_cdi = ActiveDirectory()
    
    
    @classmethod
    def setUp(self):

        self.test_cdi.name = "fake.domain"
        self.test_cdi.administrator = "fdsadmin"
        self.test_cdi.domain_controllers = ["1.1.1.1", "2.2.2.2", "3.3.3.3"]
        self.test_cdi.enabled =  True
        self.test_cdi.ou = "Legal\Eagles"
        
        test_auth = KerberosAuthEngine()
        test_auth.kdc_servers = ["1.2.3.4", "5.6.7.8"]
        test_auth.realm = "insincerity"
    
        self.test_cdi.auth_engine = test_auth

    def test_marshalling(self):
        
        engine = KerberosAuthEngine( ["1.2.3.4", "5.6.7.8"], "ice")
        cdi = ActiveDirectory( "5", "super_ad", False, ["localhost", "host4"], "fdsadmin", "fdsadmin", "me\legal", engine )
        
        j_str = ConnectorDomainInfoConverter.to_json(cdi)
        
        print( j_str )
        
        new_cdi = ConnectorDomainInfoConverter.build_from_json( j_str )
        
        assert new_cdi.name == "super_ad"
        assert new_cdi.enabled is False
        assert len(new_cdi.domain_controllers) is 2
        assert new_cdi.domain_controllers[0] == "localhost"
        assert new_cdi.administrator == "fdsadmin"
        assert new_cdi.administrator_password == "fdsadmin"
        assert new_cdi.ou == "me\legal"
        
        new_engine = new_cdi.auth_engine
        
        assert new_engine.auth_type == "KERBEROS"
        assert new_engine.kdc_servers[0] == "1.2.3.4"
        assert len( new_engine.kdc_servers ) is 2
        
    @patch( "fdscli.services.connector_domain_info_service.ConnectorDomainInfoService.get_configuration", return_value=ActiveDirectory())
    @patch( "fdscli.services.connector_domain_info_service.ConnectorDomainInfoService.set_configuration", return_value=True)
    def test_create_config(self, mock_set, mock_get):
        ''' 
        test configuring for the first time
        '''
        args = ["smb_admin", "configure", "-domain_name", "NatesWorld", "-ou", "my/you", 
            "-domain_controllers", "123.123.123.123", "45.34.23.12", "-admin", "admin",
            "-realm", "mars", "-kdc_servers", "1.1.1.1", "2.2.2.2", "-admin_password",
            "password"]
        
        self.cli.run( args )
        self.callMessageFormatter(args)

        cdi = mock_set.call_args[0][0]
        
        assert cdi.name == "NatesWorld"
        assert cdi.ou == "my/you"
        assert cdi.administrator == "admin"
        assert cdi.administrator_password == "password"
        assert len( cdi.domain_controllers ) is 2
        assert cdi.domain_controllers[1] == "45.34.23.12"
        assert cdi.auth_engine.realm == "mars"
        assert len( cdi.auth_engine.kdc_servers ) is 2
        assert cdi.auth_engine.kdc_servers[1] == "2.2.2.2"
        assert cdi.enabled is True
        
    @patch( "fdscli.services.connector_domain_info_service.ConnectorDomainInfoService.get_configuration", return_value=test_cdi)
    @patch( "fdscli.services.connector_domain_info_service.ConnectorDomainInfoService.set_configuration", return_value=True)    
    def test_edit_configuration(self, mock_set, mock_get):
        '''
        test that it correctly edits an already configured active directory
        '''
        
        args = ["smb_admin", "configure", "-domain_name", "real.domain", "-realm", "nirvana"]
        self.cli.run( args )
        self.callMessageFormatter( args )
        
        cdi = mock_set.call_args[0][0]
        
        assert cdi.name == "real.domain"
        assert cdi.ou == "Legal\Eagles"
        assert cdi.administrator == "fdsadmin"
        assert len( cdi.domain_controllers ) is 3
        assert cdi.domain_controllers[1] == "2.2.2.2"
        assert cdi.auth_engine.realm == "nirvana"
        assert len( cdi.auth_engine.kdc_servers ) is 2
        assert cdi.auth_engine.kdc_servers[1] == "5.6.7.8"   
        assert cdi.enabled is True     
        
    @patch( "fdscli.services.connector_domain_info_service.ConnectorDomainInfoService.get_configuration", return_value=test_cdi)
    @patch( "fdscli.services.connector_domain_info_service.ConnectorDomainInfoService.set_configuration", return_value=True)        
    def test_disable_ad(self, mock_set, mock_get):
        '''
        try to disable active directory
        '''
        
        assert self.test_cdi.enabled is True
        
        args = [ "smb_admin", "disable" ]
        self.cli.run( args )
        self.callMessageFormatter( args )
        
        cdi = mock_set.call_args[0][0]
        
        assert cdi.enabled is False
        
    @patch( "fdscli.services.connector_domain_info_service.ConnectorDomainInfoService.get_configuration", return_value=test_cdi)
    @patch( "fdscli.services.connector_domain_info_service.ConnectorDomainInfoService.set_configuration", return_value=True)        
    def test_enable_ad(self, mock_set, mock_get):
        '''
        try to disable active directory
        '''
        self.test_cdi.enabled = False
        assert self.test_cdi.enabled is False
        
        args = [ "smb_admin", "enable" ]
        self.cli.run( args )
        self.callMessageFormatter( args )
        
        cdi = mock_set.call_args[0][0]
        
        assert cdi.enabled is True        