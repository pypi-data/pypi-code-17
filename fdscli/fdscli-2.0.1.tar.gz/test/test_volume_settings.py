# Copyright 2017 Formation Data Systems, Inc. All Rights Reserved.
#

from test.base_cli_test import BaseCliTest
from fdscli.model.common.size import Size
from fdscli.model.volume.settings.block_settings import BlockSettings
from fdscli.model.volume.settings.iscsi_settings import ISCSISettings
from fdscli.model.volume.settings.nfs_settings import NfsSettings
from fdscli.model.volume.settings.object_settings import ObjectSettings
from fdscli.model.volume.settings.volume_settings import VolumeSettings
from fdscli.model.volume.settings.smb_settings import SmbSettings

class VolumeSettingsTests(BaseCliTest):
    '''Tests for the entire hierarchy of volume settings types.
    '''

    def test_block_settings(self):
        '''Settings common to block volume types
        '''

        # Defaults
        s = BlockSettings();
        assert s.type == "BLOCK"
        assert s.capacity.size == 10
        assert s.capacity.unit == "GB"
        assert s.block_size == None
        assert s.encryption == False
        assert s.compression == False
        assert s.allow_mount == True
        assert s.replica == False

        # Positional arguments
        size1 = Size(42, "TB")
        size2 = Size(1028, "MB")
        s1 = BlockSettings(size1, size2, True, True, False, True);
        assert s1.type == "BLOCK"
        assert s1.capacity.size == 42
        assert s1.capacity.unit == "TB"
        assert s1.block_size.size == 1028
        assert s1.block_size.unit == "MB"
        assert s1.encryption == True
        assert s1.compression == True
        assert s1.allow_mount == False
        assert s1.replica == True

    def test_iscsi_settings(self):
        '''Settings for concrete ISCSI volume type
        '''

        # Defaults
        s = ISCSISettings();
        assert s.type == "ISCSI"
        assert s.capacity.size == 10
        assert s.capacity.unit == "GB"
        assert s.block_size == None
        assert s.encryption == False
        assert s.compression == False
        assert s.allow_mount == True
        assert s.replica == False

        # Positional arguments
        size1 = Size(42, "TB")
        size2 = Size(1028, "MB")
        s1 = ISCSISettings(size1, size2, True, True, False, True);
        assert s1.type == "ISCSI"
        assert s1.capacity.size == 42
        assert s1.capacity.unit == "TB"
        assert s1.block_size.size == 1028
        assert s1.block_size.unit == "MB"
        assert s1.encryption == True
        assert s1.compression == True
        assert s1.allow_mount == False
        assert s1.replica == True

    def test_nfs_settings(self):
        '''Settings for concrete NFS volume type
        '''

        # Defaults
        s = NfsSettings();
        assert s.type == "NFS"
        assert s.use_acls == False
        assert s.use_root_squash == False
        assert s.synchronous == False
        assert s.clients == "*"
        assert s.max_object_size.size == 1048576
        assert s.max_object_size.unit == "B"
        assert s.capacity.size == 1
        assert s.capacity.unit == "TB"
        assert s.encryption == False
        assert s.compression == False
        assert s.allow_mount == True
        assert s.replica == False

        # Positional arguments
        size1 = Size(16, "GB")
        size2 = Size(4, "TB")
        s1 = NfsSettings(False, True, True, "them", size1, size2, True, True, False, True)
        assert s1.type == "NFS"
        assert s1.use_acls == False
        assert s1.use_root_squash == True
        assert s1.synchronous == True
        assert s1.clients == "them"
        assert s1.max_object_size.size == 16
        assert s1.max_object_size.unit == "GB"
        assert s1.capacity.size == 4
        assert s1.capacity.unit == "TB"
        assert s1.encryption == True
        assert s1.compression == True
        assert s1.allow_mount == False
        assert s1.replica == True
        
    def test_smb_settings(self):
        
        s1 = SmbSettings()
        
        assert s1.type == "SMB"
        assert s1.use_acls == False
        
        self.assertRaises( AttributeError, lambda: s1.use_root_squash )
        self.assertRaises( AttributeError, lambda: s1.synchronous )
        assert s1.clients == "*"
        assert s1.max_object_size.size == 1048576
        assert s1.max_object_size.unit == "B"
        assert s1.capacity.size == 1
        assert s1.capacity.unit == "TB"
        assert s1.encryption == False
        assert s1.compression == False
        assert s1.allow_mount == True
        assert s1.replica == False
        assert len(s1.shares) == 0
        assert s1.supported_version == "all"
        
        s2 = SmbSettings( "3.0.0", True, "123.*", Size(2, "MB"), Size( 500, "GB" ),
            True, True, False, True )
        
        assert s2.type == "SMB"
        assert s2.use_acls == True
        assert s2.clients == "123.*"
        assert s2.max_object_size.size == 2, "Expected 2 MB but got {}".format( s2.max_object_size.size )
        assert s2.max_object_size.unit == "MB"
        assert s2.capacity.size == 500
        assert s2.capacity.unit == "GB"
        assert s2.encryption == True
        assert s2.compression == True
        assert s2.allow_mount == False
        assert s2.replica == True
        assert len(s2.shares) == 0
        assert s2.supported_version == "3.0.0"        

    def test_object_settings(self):
        '''Settings common to all object volume types
        '''

        # Defaults
        s = ObjectSettings();
        assert s.type == "OBJECT"
        assert s.max_object_size == None
        assert s.encryption == False
        assert s.compression == False
        assert s.allow_mount == True
        assert s.replica == False

        # Positional arguments
        size1 = Size(32, "GB")
        s1 = ObjectSettings(size1, True, True, False, True)
        assert s1.max_object_size.size == 32
        assert s1.max_object_size.unit == "GB"
        assert s1.encryption == True
        assert s1.compression == True
        assert s1.allow_mount == False
        assert s1.replica == True

    def test_volume_settings(self):
        '''Settings common to all volume types
        '''

        # Defaults
        s = VolumeSettings();
        assert s.type == "OBJECT"
        assert s.encryption == False
        assert s.compression == False
        assert s.allow_mount == True
        assert s.replica == False

        # Positional arguments
        s1 = VolumeSettings("BLOCK", True, True, False, True)
        assert s1.type == "BLOCK"
        assert s1.encryption == True
        assert s1.compression == True
        assert s1.allow_mount == False
        assert s1.replica == True

        # Named arguments
        s2 = VolumeSettings(encryption=True)
        assert s2.type == "OBJECT"
        assert s2.encryption == True
        assert s2.compression == False
        assert s2.allow_mount == True
        assert s2.replica == False

        s3 = VolumeSettings(compression=True)
        assert s3.type == "OBJECT"
        assert s3.encryption == False
        assert s3.compression == True
        assert s3.allow_mount == True
        assert s3.replica == False

        s4 = VolumeSettings(allow_mount=False)
        assert s4.type == "OBJECT"
        assert s4.encryption == False
        assert s4.compression == False
        assert s4.allow_mount == False
        assert s4.replica == False

        s5 = VolumeSettings(replica=True)
        assert s5.type == "OBJECT"
        assert s5.encryption == False
        assert s5.compression == False
        assert s5.allow_mount == True
        assert s5.replica == True

        s6 = VolumeSettings(a_type="NFS")
        assert s6.type == "NFS"
        assert s6.encryption == False
        assert s6.compression == False
        assert s6.allow_mount == True
        assert s6.replica == False
        
        s7 = VolumeSettings(a_type="SMB")
        assert s7.type == "SMB"
        assert s7.encryption == False
        assert s7.compression == False
        assert s7.allow_mount == True
        assert s7.replica == False        
