# Copyright (c) 2015, Formation Data Systems, Inc. All Rights Reserved.
#

import json
from fdscli.model.volume.settings.block_settings import BlockSettings
from fdscli.utils.converters.common.size_converter import SizeConverter
from fdscli.model.volume.settings.object_settings import ObjectSettings
from fdscli.utils.converters.common.credential_converter import CredentialConverter
from fdscli.utils.converters.volume.lun_permission_converter import LunPermissionConverter
from fdscli.model.volume.settings.iscsi_settings import ISCSISettings
from fdscli.model.volume.settings.nfs_settings import NfsSettings
from fdscli.model.volume.settings.smb_settings import SmbSettings
from fdscli.utils.converters.volume.smb_share_converter import SmbShareConverter

class SettingsConverter(object):
    '''
    Created on Jun 1, 2015
    
    @author: nate
    '''

    @staticmethod
    def to_json(settings):
        '''
        Parameters
        ----------
        :type settings: ``model.volume.settings.VolumeSettings`` or a subclass
        '''

        j_settings = dict()
        j_settings["type"] = settings.type
        j_settings["compressed"] = settings.compression
        j_settings["encrypted"] = settings.encryption
        j_settings["allowMount"] = settings.allow_mount
        j_settings["replica"] = settings.replica
        
        if ( settings.type is "BLOCK" or settings.type is "ISCSI"):
            
            j_settings["capacity"] = json.loads(SizeConverter.to_json(settings.capacity))
            
            if settings.block_size is not None:
                j_settings["blockSize"] = json.loads(SizeConverter.to_json(settings.block_size))
            
            if ( settings.type is "ISCSI" ):
                
                d_target = dict()
                
                incoming_creds = []
                for in_cred in settings.incoming_credentials:
                    incoming_creds.append( json.loads( CredentialConverter.to_json(in_cred) ) )
                    
                d_target["incomingUsers"] = incoming_creds
                
                outgoing_creds = []
                for out_cred in settings.outgoing_credentials:
                    outgoing_creds.append( json.loads( CredentialConverter.to_json(out_cred) ) )
                    
                d_target["outgoingUsers"] = outgoing_creds
                
                lun_permissions = []
                for lun in settings.lun_permissions:
                    lun_permissions.append( json.loads( LunPermissionConverter.to_json( lun ) ) )
                    
                d_target["luns"] = lun_permissions
                
                initiators = []
                for initiator in settings.initiators:
                    j_init = dict()
                    j_init["wwn_mask"] = initiator
                    initiators.append( j_init )
                    
                d_target["initiators"] = initiators
                
                j_settings["target"] = d_target
            
        else:
            
            if settings.max_object_size is not None:
                j_settings["maxObjectSize"] = json.loads(SizeConverter.to_json(settings.max_object_size))
                
            if settings.type is "NFS":
                    options = ''
                    
                    if settings.use_acls is True or settings.use_acls == 'true':
                        options += 'acl,'
                    else:
                        options += 'noacl,'
                        
                    if settings.use_root_squash is True or settings.use_root_squash == 'true':
                        options += 'root_squash,'
                    else:
                        options += 'no_root_squash,'
                        
                    if settings.synchronous is True or settings.synchronous == 'true':
                        options += 'sync'
                    else:
                        options += 'async'
                        
                    j_settings["capacity"] = json.loads( SizeConverter.to_json(settings.capacity) )
                        
                    j_settings['options'] = options
                    
                    j_settings['clients'] = settings.clients;
                    
            #fi
            elif settings.type is "SMB":
                options = ''
                
                if settings.use_acls is True or settings.use_acls == 'true':
                    options += 'acl,'
                else:
                    options += 'noacl'
                    
                j_settings['options'] = options
                j_settings['clients'] = settings.clients;
                j_settings['supported_version'] = settings.supported_version
                j_settings["capacity"] = json.loads( SizeConverter.to_json(settings.capacity) )
                j_shares = []
                
                for share in  settings.shares:
                    j_share = json.loads( SmbShareConverter.to_json( share ) )
                    j_shares.append( j_share )
                    
                j_settings['shares'] = j_shares
                
            
        j_settings = json.dumps(j_settings)
        
        return j_settings
    
    @staticmethod
    def build_settings_from_json(j_str):
        
        settings = None
        
        if not isinstance( j_str, dict ):
            j_str = json.loads(j_str)
        
        volume_type = j_str.pop( "type" )
        
        if volume_type == "BLOCK" or volume_type == "ISCSI":
            
            if volume_type == "BLOCK":
                settings = BlockSettings()
            elif volume_type == "ISCSI":
                settings = ISCSISettings()
            
            if "blockSize" in j_str:
                settings.block_size = SizeConverter.build_size_from_json( j_str.pop("blockSize", settings.block_size) )
                
            settings.capacity = SizeConverter.build_size_from_json( j_str.pop("capacity", settings.capacity) )
            
            if ( volume_type == "ISCSI" ):
                
                set_str = j_str.pop( "target" );
                
                initiators = set_str.pop( "initiators", [] )
                
                for initiator in initiators:
                    settings.initiators.append( initiator.pop( "wwn_mask" ) )
                
                luns = set_str.pop( "luns", [] )
                real_luns = []
                for lun in luns:
                    real_luns.append( LunPermissionConverter.build_lun_permission_from_json( lun ) )
                
                settings.lun_permissions = real_luns
                
                incoming_strs = set_str.pop( "incomingUsers", [] )
                real_incoming = []
                for incoming_str in incoming_strs:
                    real_incoming.append( CredentialConverter.build_credential_from_json( incoming_str ) )
                    
                settings.incoming_credentials = real_incoming
                
                outgoing_strs = set_str.pop( "outgoingUsers", [] )
                real_outgoing = []
                for outgoing_str in outgoing_strs:
                    real_outgoing.append( CredentialConverter.build_credential_from_json( outgoing_str ) )
                    
                settings.outgoing_credentials = real_outgoing
            
        else:
            
            if volume_type == "OBJECT":
                settings = ObjectSettings()
            elif volume_type == "NFS":
                settings = NfsSettings()
            elif volume_type == "SMB":
                settings = SmbSettings()
            
            if "maxObjectSize" in j_str:
                settings.max_object_size = SizeConverter.build_size_from_json( j_str.pop("maxObjectSize", settings.max_object_size) )
                
            if volume_type == "NFS":
                options = j_str.pop( "options", [])
                
                settings.use_acls = ( options.find( 'noacl' ) == -1 )
                settings.use_root_squash = ( options.find( 'no_root_squash' ) == -1)
                settings.synchronous = ( options.find( 'async' ) == -1 )
                settings.clients = j_str.pop( "clients", "*" )
                settings.capacity = SizeConverter.build_size_from_json( j_str.pop( "capacity", settings.capacity ) )
                
            if volume_type == "SMB":
                options = j_str.pop( "options", [])
                
                settings.use_acls = ( options.find( 'noacl' ) == -1 )  
                settings.clients = j_str.pop( "clients", "*" )
                settings.capacity = SizeConverter.build_size_from_json( j_str.pop( "capacity", settings.capacity ) )
                settings.supported_version = j_str.pop( "supported_version", "all" )
                
                shares = j_str.pop( "shares", [] )
                v_shares = [];
                
                for share in shares:
                    v_share = SmbShareConverter.build_from_json( share )
                    v_shares.append( share )
                
                settings.shares = v_shares   
                

        settings.encryption = j_str.pop( "encrypted", settings.encryption)
        settings.compression = j_str.pop( "compressed", settings.compression)
        settings.allow_mount = j_str.pop( "allowMount", settings.allow_mount)
        settings.replica = j_str.pop( "replica", settings.replica)
        return settings
