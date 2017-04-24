'''
Created on Mar 27, 2017

@author: nate
'''
from test.base_cli_test import BaseCliTest
from fdscli.model.volume.volume import Volume
from fdscli.model.volume.settings.nfs_settings import NfsSettings
from mock import patch
from fdscli.plugins.volume_plugin import VolumePlugin
from fdscli.model.volume.settings.smb_settings import SmbSettings
from fdscli.model.volume.smb_share import SmbShare

class Test(BaseCliTest):

    @patch( "fdscli.services.response_writer.ResponseWriter.writeTabularData", return_values=None )
    def test_smb_printing(self, mock_writer):
        
        volume = Volume()
        volume.settings = NfsSettings()
        
        vp = VolumePlugin()
        
        vp.pretty_print_volume(volume)
        
        assert mock_writer.call_count is 4, "Should print 4 sections - not 5."
        
        volume.settings = SmbSettings()
        
        share_1 = SmbShare( "Foo", False, None, False, True, "AES_CCM" )
        share_2 = SmbShare( "Fighters", True, "\\home\on\the\range", True, False, None )
        shares = [ share_1, share_2 ]
        
        volume.settings.shares = shares
        
        vp.pretty_print_volume( volume )
        
        assert mock_writer.call_count is 9, "Should print 4 sections from the first and 5 from the second because its SMB."
        
        smbCall = mock_writer.call_args_list[7][0][0]
        
        assert len(smbCall) is 2, "Should be 2 shares but {} were found.".format( len(smbCall) )
        assert smbCall[0]["Name"] is "Foo", "Expected the first to be 'Foo' but was {}".format( smbCall[0]["Name"] )
        assert smbCall[1]["Name"] is "Fighters", "Expected the first to be 'Fighters' but was {}".format( smbCall[1]["Name"] )
        assert smbCall[0]["SMB Signing"] is False, "Expected SMB Signing for 0 to be false but was {}".format( smbCall[0]["SMB Signing"] )
        assert smbCall[1]["SMB Signing"] is True, "Expected SMB Signing for 1 to be true but was {}".format( smbCall[1]["SMB Signing"] )
        assert smbCall[0]["Cont. Availability"] is True, "Expected Cont. Availability for 0 to be true but was {}".format( smbCall[0]["Cont. Availability"] )
        assert smbCall[1]["Cont. Availability"] is False, "Expected Cont. Availability for 1 to be false but was {}".format( smbCall[1]["Cont. Availability"] )
        assert smbCall[0]["Encryption"] is "AES_CCM", "Expected Encryption for 0 to be AES_CCM but was {}".format( smbCall[0]["Encryption"] )
        assert smbCall[1]["Encryption"] is None, "Expected Encryption for 1 to be None but was {}".format( smbCall[1]["Encryption"] )
        assert smbCall[0]["Use Home Dir."] is False, "Expected Use Home Dir. for 0 to be false but was {}".format( smbCall[0]["Use Home Dir."] )
        assert smbCall[1]["Use Home Dir."] is True, "Expected Use Home Dir. for 1 to be true but was {}".format( smbCall[1]["Use Home Dir."] )
        assert smbCall[1]["Home Dir."] is "\\home\on\the\range", "Expected home dir to be '\\home\on\the\range' but was {}".format( smbCall[1]["Home Dir."] )
        
        pass
