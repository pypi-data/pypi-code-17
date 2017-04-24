from .abstract_plugin import AbstractPlugin
from fdscli.services.fds_auth import FdsAuth
from fdscli.services.connector_domain_info_service import ConnectorDomainInfoService
from fdscli.model.admin.connectors.active_directory import ActiveDirectory
from fdscli.model.admin.connectors.kerberoes_auth_engine import KerberosAuthEngine
from fdscli.utils.converters.admin.connectors.connector_domain_info_converter import ConnectorDomainInfoConverter
from fdscli.services import response_writer
from collections import OrderedDict
from cProfile import label


class ConnectorDomainPlugin(AbstractPlugin):    
    '''
    Created on Apr 13, 2015
    
    Plugin to handle the parsing of all user related tasks and the calls
    to the corresponding REST endpoints to manage users
    
    @author: nate
    '''    
    
    def __init__(self):
        AbstractPlugin.__init__(self)
        
    def detect_shortcut(self, args):
        '''
        @see: AbstractPlugin
        '''  
        
        return None        
    
    def get_user_service(self):
        
        return self.__user_service
    
    def build_parser(self, parentParser, session): 
        '''
        @see: AbstractPlugin
        '''
        
        self.session = session
        
        if not self.session.is_allowed( FdsAuth.USER_MGMT ):
            return
        
        self.__connector_domain_service = ConnectorDomainInfoService( self.session )         
        
        p_parser = parentParser.add_parser( "smb_admin", help="Manage your SMB domain information." )
        subparser = p_parser.add_subparsers(help="The sub-commands that are available")
        self.create_configure_parser( subparser )
        self.create_enablement_parser( subparser )
        self.create_list_configuration_parser( subparser )

    
# define the parser commands    
    
    def create_configure_parser(self, subparser ):
        '''
        Create the command to configure active directory / kerberos
        '''
        
        __ad_parser = subparser.add_parser( "configure", help="Configure Active Directory for use with the SMB connector." )
        self.add_format_arg( __ad_parser )
        __ad_parser.add_argument( self.arg_str + AbstractPlugin.domain_name_str, default=None, help="The name of the ActiveDirectory domain you would like to join." )
        __ad_parser.add_argument( self.arg_str + AbstractPlugin.administrator_str, default=None, help="The user name for the administrator account to use." )
        __ad_parser.add_argument( self.arg_str + AbstractPlugin.domain_controllers_str, default=None, nargs="*", help="A list of domain controllers to use.")
        __ad_parser.add_argument( self.arg_str + AbstractPlugin.ou_str, default=None, help="The organizational unit that you would like to join." )
        __ad_parser.add_argument( self.arg_str + AbstractPlugin.realm_str, default=None, help="The kerberos realm to authenticate under." )
        __ad_parser.add_argument( self.arg_str + AbstractPlugin.kdc_server_str, default=None, help="The KDC servers to use for authentication.", nargs="*" )
        __ad_parser.add_argument( self.arg_str + AbstractPlugin.administrator_password_str, default="", help="The administrator password.  (You will be prompted if this is left unspecified for security reasons)" )
        
        __ad_parser.set_defaults(func=self.configure_ad)
    
    def create_enablement_parser(self, subparser):
        '''
        Build the parser to enable or disable the domain
        '''
        __e_parser = subparser.add_parser( "enable", help="Enable the current configuration and cause a 'Domain Join' operation." )
        self.add_format_arg( __e_parser )
        __e_parser.set_defaults( func=self.enable_config )
        
        __d_parser = subparser.add_parser( "disable", help="Disable the current configuration and cause a 'Domain Leave' operation." )
        self.add_format_arg( __d_parser )
        __d_parser.set_defaults( func=self.disable_config )
        
    def create_list_configuration_parser(self, subparser):
        '''
        create the parser for listing the current configuration
        '''
        __list_parser = subparser.add_parser( "list", help="List out the current Active Directory configuration" )
        self.add_format_arg( __list_parser )
        
        __list_parser.set_defaults( func=self.list_config )
        
#########################

    def configure_ad(self, args ):
        '''
        configure the active directory
        '''
        
        #start with what's there and build
        cdi = self.__connector_domain_service.get_configuration()
        
        if cdi.auth_engine is None:
            cdi.auth_engine = KerberosAuthEngine()
        
        if args[AbstractPlugin.domain_name_str] is not None:
            cdi.name = args[AbstractPlugin.domain_name_str]
        
        if args[AbstractPlugin.domain_controllers_str] is not None:
            cdi.domain_controllers = args[AbstractPlugin.domain_controllers_str]
            
        if args[AbstractPlugin.administrator_str] is not None:
            cdi.administrator = args[AbstractPlugin.administrator_str]
            
        if args[AbstractPlugin.administrator_password_str] is not None:
            cdi.administrator_password = args[AbstractPlugin.administrator_password_str]
            
        if args[AbstractPlugin.ou_str] is not None:
            cdi.ou = args[AbstractPlugin.ou_str]
            
        if args[AbstractPlugin.kdc_server_str] is not None:
            cdi.auth_engine.kdc_servers = args[AbstractPlugin.kdc_server_str]  
            
        if args[AbstractPlugin.realm_str] is not None:
            cdi.auth_engine.realm = args[AbstractPlugin.realm_str]                              

        self.__connector_domain_service.set_configuration( cdi )
        
        self.list_config(args)
        
    def enable_config(self, args):
        '''
        enable the configuration
        '''
        
        cdi = self.__connector_domain_service.get_configuration()
        cdi.enabled = True
        
        self.__connector_domain_service.set_configuration(cdi)
        self.list_config(args)
        
    def disable_config(self, args):
        '''
        disable the configuration
        '''
        
        cdi = self.__connector_domain_service.get_configuration()
        cdi.enabled = False
        
        self.__connector_domain_service.set_configuration(cdi)
        self.list_config(args)
        
    def list_config(self, args):
        '''
        list the current configuration out
        '''
        
        cdi = self.__connector_domain_service.get_configuration()
        
        if args[AbstractPlugin.format_str] == "json":
            #do json
            j_str = ConnectorDomainInfoConverter.to_json( cdi )
            response_writer.ResponseWriter.writeJson( j_str )
            return
        
        en = "enabled"
        
        if cdi.enabled is False:
            en = "disabled"
        
        print( "Active Directory is currently {}\n".format( en ) )
        
        # JSON block returns so this is tabular
        values = []
        
        d_name = OrderedDict()
        d_name["Item"] = "Domain Name"
        d_name["Value"] = cdi.name
        values.append( d_name )
        
        d_ou = OrderedDict()
        d_ou["Item"] = "Organizational Unit"
        d_ou["Value"] = cdi.ou
        values.append( d_ou )
        
        for i, dc in enumerate( cdi.domain_controllers ):
            d_dcs = OrderedDict()
            
            label = ""
            
            if i is 0:
                label = "Domain Controllers"
            d_dcs["Item"] = label
            d_dcs["Value"] = dc
            values.append( d_dcs )
        #for
        
        d_admin = OrderedDict()
        d_admin["Item"] = "Administrator"
        d_admin["Value"] = cdi.administrator
        values.append( d_admin )
        
        for i, kdc in enumerate( cdi.auth_engine.kdc_servers ):
            d_kdc = OrderedDict()
            
            label = ""
            
            if i is 0:
                label = "KDC Servers"
            
            d_kdc["Item"] = label
            d_kdc["Value"] = kdc
            values.append( d_kdc )
        #for
        
        d_realm = OrderedDict()
        d_realm["Item"] = "Kerberos Realm"
        d_realm["Value"] = cdi.auth_engine.realm
        values.append( d_realm )
        
        response_writer.ResponseWriter.writeTabularData( values )
        