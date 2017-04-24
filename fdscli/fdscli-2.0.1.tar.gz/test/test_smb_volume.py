from test.base_cli_test import BaseCliTest
import mock_functions
from mock import patch
from fdscli.model.common.size import Size
from fdscli.model.volume.settings.nfs_settings import NfsSettings
from fdscli.utils.fds_cli_configuration_manager import FdsCliConfigurationManager
from fdscli.utils.converters.volume.settings_converter import SettingsConverter
from fdscli.model.volume.settings.smb_settings import SmbSettings
from fdscli.model.volume.smb_share import SmbShare
from fdscli.utils.converters.volume.smb_share_converter import SmbShareConverter

class TestSmbVolume( BaseCliTest ):
    '''
    Created on Nov 9, 2015
    
    @author: nate
    '''
    def test_share_marshalling(self):
        
        s1 = SmbShare()
        
        assert s1.continuous_availability is False
        assert s1.use_home_dir is False
        assert s1.home_dir is None
        assert s1.smb_signing is False
        assert s1.share_encryption is None        
        
        j_share = SmbShareConverter.to_json( s1 )
        print( j_share )
        
        re_share = SmbShareConverter.build_from_json( j_share )
        
        assert re_share.continuous_availability is False
        assert re_share.use_home_dir is False
        assert re_share.home_dir is None
        assert re_share.smb_signing is False
        assert re_share.share_encryption is None
        
        s2 = SmbShare( "share_me", True, "/home/nate", True, True, "AES_GCM" )
        
        assert s2.continuous_availability is True
        assert s2.use_home_dir is True
        assert s2.home_dir is "/home/nate"
        assert s2.smb_signing is True
        assert s2.share_encryption is "AES_GCM"        
        
        j_share = SmbShareConverter.to_json( s2 )
        print( j_share )
        
        re_share = SmbShareConverter.build_from_json( j_share )
        
        assert re_share.continuous_availability is True
        assert re_share.use_home_dir is True
        assert re_share.home_dir == "/home/nate"
        assert re_share.smb_signing is True
        assert re_share.share_encryption == "AES_GCM"  
        assert re_share.share_name == "share_me"
        
    def test_bad_encryption_in_share(self):
        
        share = SmbShare()
        
        share.share_encryption = "AES_GCM"
        assert share.share_encryption == "AES_GCM"
        share.share_encryption = "AES_CCM"
        assert share.share_encryption == "AES_CCM"
        share.share_encryption = None
        assert share.share_encryption is None
        
        self.assertRaises( TypeError, lambda: share.share_encryption, "Something" )


    def test_marshalling(self):
        
        settings = SmbSettings()
        
        settings.use_acls = True
        settings.clients ="localhost*::[0-3]"
        settings.allow_mount = "false"
        settings.replica = "true"
        settings.supported_version = "3.0.0"
        
        shares = [SmbShare("MyShare", False, None, True, False, "AES_GCM")]
        
        settings.shares = shares
        
        j_str = SettingsConverter.to_json(settings)
        
        print( j_str )
        
        m_settings = SettingsConverter.build_settings_from_json( j_str )
        
        assert m_settings.type == "SMB"
        assert m_settings.clients == "localhost*::[0-3]"
        assert m_settings.allow_mount == False
        assert m_settings.replica == True
        assert m_settings.use_acls is True
        assert m_settings.supported_version == "3.0.0"
        assert len(m_settings.shares) is 1, "Expected 1 share but got {}".format( len(m_settings.shares) )
        
        # Checking the defaults
        assert settings.capacity != None, "Expected to have a capacity setting but found none."
        assert settings.capacity.size == 1, "Expected 1 but got {}".format( settings.capacity.size )
        assert settings.capacity.unit == "TB", "Expected TB as a size unit but got {}".format( settings.capacity.unit )
        
        settings.capacity = Size( size=3, unit="EB" )
        settings.use_acls = False
        settings.supported_version = "all"
        
        j_str = SettingsConverter.to_json( settings )
        print( j_str )
        m_settings = SettingsConverter.build_settings_from_json(j_str)
        
        # Checking settings
        assert m_settings.capacity != None, "Expected to have a capacity setting but found none."
        assert m_settings.capacity.size == 3, "Expected 3 but got {}".format( m_settings.capacity.size )
        assert m_settings.capacity.unit == "EB", "Expected EB as a size unit but got {}".format( settings.capacity.unit )
        
        #make sure we're marshalling to the right version acls
        assert j_str.find( "noacl" ) != -1, "Expected to find 'noacl' in the string but did not."
        assert m_settings.use_acls is False
        assert m_settings.supported_version == "all"
        
    @patch( "fdscli.services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "fdscli.services.volume_service.VolumeService.create_volume", side_effect=mock_functions.createVolume )        
    def test_smb_creation(self, volumeCreate, listVolumes ):
        '''
        This test will make sure the settings look right after a volume create call
        '''
        print( "Testing SMB volume creation through the plugin with default size settings." )
        
        config = FdsCliConfigurationManager()
        self.cli.loadmodules()
        args = ['volume', 'create', 'smb', '-name', 'smb_max_ob_size', '-max_object_size', '2','-max_object_size_unit', 'MB']
        self.callMessageFormatter(args)
        self.cli.run(args)
        volume = volumeCreate.call_args[0][0]
        assert volume.settings.max_object_size.size == 2
        assert volume.settings.max_object_size.unit == 'MB'
        args = ['volume', 'create', 'smb', '-name', 'smbness', '-acls', 'true', '-supported_version', '2.1',
                '-clients', '128.*2*.[6-9]::ab']
         
        self.callMessageFormatter(args)
        self.cli.run(args)
         
        volume = volumeCreate.call_args[0][0]
        settings = volume.settings
     
        assert settings.type == 'SMB'
        assert settings.clients == "128.*2*.[6-9]::ab"
        # default max_object_size is 1 MB for NFS
        assert settings.max_object_size.size == 1048576
        assert settings.max_object_size.unit == 'B'
        assert settings.use_acls is True
        assert settings.supported_version == "2.1"
        
        # Checking the defaults
        assert settings.capacity != None, "Expected to have a capacity setting but found none."
        assert settings.capacity.size == 524288, "Expected 524288 but got {}".format( settings.capacity.size )
        assert settings.capacity.unit == "GB", "Expected GB as a size unit but got {}".format( settings.capacity.unit )
        assert settings.allow_mount == True
        assert settings.replica == False

        print( "Testing SMB volume creation through the plugin with explicit size settings." )
        
        args = ['volume', 'create', 'smb', '-name', 'smbness', '-acls', 'false',
                '-clients', '228.*2*.[6-9]::ab', '-size', '243', '-size_unit', 'GB']
        
        self.callMessageFormatter(args)
        self.cli.run(args)
         
        volume = volumeCreate.call_args[0][0]
        settings = volume.settings
     
        assert settings.type == 'SMB'
        assert settings.clients == "228.*2*.[6-9]::ab"
        assert settings.use_acls is False
        
        # Checking the defaults
        assert settings.capacity != None, "Expected to have a capacity setting but found none."
        assert settings.capacity.size == 243, "Expected 243 but got {}".format( settings.capacity.size )
        assert settings.capacity.unit == "GB", "Expected GB as a size unit but got {}".format( settings.capacity.unit )
        
    @patch( "fdscli.services.volume_service.VolumeService.get_volume", side_effect=mock_functions.getSmbVolume)
    @patch( "fdscli.services.volume_service.VolumeService.list_volumes", side_effect=mock_functions.listVolumes )
    @patch( "fdscli.services.volume_service.VolumeService.edit_volume", side_effect=mock_functions.editVolume )                 
    def test_smb_edit(self, mock_edit, mock_list, mock_get_vol):
        '''
        This test will try to edit an SMB Volume
        '''
        
        print( "Testing the editing of an SMB volume" )
        
        config = FdsCliConfigurationManager()
        
        self.cli.loadmodules()
        
        args = ['volume', 'edit', '-volume_id', '3', '-clients', '10.1.1.1', '-supported_version', '2.0.2']
        
        self.callMessageFormatter(args)
        self.cli.run(args)
        
        volume = mock_edit.call_args[0][0]
        settings = volume.settings
        
        assert volume.id == 3
        assert settings.clients == '10.1.1.1'
        assert settings.supported_version == '2.0.2'
