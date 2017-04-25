'''
Created on Mar 13, 2017

@author: nate
'''
from fdscli.plugins.abstract_plugin import AbstractPlugin
from fdscli.services.volume_service import VolumeService
from fdscli.model.fds_error import FdsError
from fdscli.model.volume.smb_share import SmbShare
from __builtin__ import True

class SmbSharePlugin(AbstractPlugin):
    '''
    This is a pseudo plugin because its a sub-plugin for the volume plugin
    '''
    def detect_shortcut(self, args):
        '''
    @see: AbstractPlugin
        '''
        return None

    def get_parser(self, parent_parser ):

        s_parser = parent_parser.add_parser( "share", help="Manage the shares on your SMB volumes." )
        self.add_add_parser(s_parser)
        self.add_remove_parser(s_parser)
        self.add_edit_parser(s_parser)

    def add_add_parser(self, parent_parser):

        a_parser = parent_parser.add_parser( "add", help="Add a share to an existing volume")
        a_parser.add_argument( self.arg_str + AbstractPlugin.volume_id_str, help="The ID of the volume to add the share to." )
        a_parser.add_argument( self.arg_str + AbstractPlugin.name_str, help="The name of the new share.  (This must be globally unique in the cluster).")
        a_parser.add_argument( self.arg_str + AbstractPlugin.continuous_availability_str, choices=["true", "false"], default="false", help="Configure share with continuous availability configured (Only available in version 3.0.0+)" )
        a_parser.add_argument( self.arg_str + AbstractPlugin.share_encryption_str, choices=["AES_GCM", "AES_CCM", "None"], default="None", help="The method of encryption for this share.")
        a_parser.add_argument( self.arg_str + AbstractPlugin.smb_signing_str, choices=["true", "false"], default="false", help="Enable SMB signing for the share. (Only available for versions 3.0.0+)")
        a_parser.add_argument( self.arg_str + AbstractPlugin.use_home_dir_str, choices=["true", "false"], default="false", help="Enable home directory usage.")
        a_parser.add_argument( self.arg_str + AbstractPlugin.home_dir_str, help="The home directory name.")

        a_parser.set_defaults(func=self.add_share)

    def add_remove_parser(self, parent_parser):

        a_parser = parent_parser.add_parser( "delete", help="Delete a share from an existing volume.")
        a_parser.add_argument( self.arg_str + AbstractPlugin.volume_id_str, help="The ID of the volume that controls the share in question." )
        a_parser.add_argument( self.arg_str + AbstractPlugin.name_str, "The name of the share to delete." )

        a_parser.set_defaults(func=self.remove_share)

    def add_edit_parser(self, parent_parser):

        a_parser = parent_parser.add_parser( "edit", help="Edit an existing share.")
        a_parser.add_argument( self.arg_str + AbstractPlugin.volume_id_str, help="The ID of the volume that controls the share in question." )
        a_parser.add_argument( self.arg_str + AbstractPlugin.name_str, help="The name of the share to edit.")
        a_parser.add_argument( self.arg_str + AbstractPlugin.continuous_availability_str, choices=["true", "false"], default="false", help="Configure share with continuous availability configured (Only available in version 3.0.0+)" )
        a_parser.add_argument( self.arg_str + AbstractPlugin.share_encryption_str, choices=["AES_GCM", "AES_CCM", "None"], default="None", help="The method of encryption for this share.")
        a_parser.add_argument( self.arg_str + AbstractPlugin.smb_signing_str, choices=["true", "false"], default="false", help="Enable SMB signing for the share. (Only available for versions 3.0.0+)")
        a_parser.add_argument( self.arg_str + AbstractPlugin.use_home_dir_str, choices=["true", "false"], default="false", help="Enable home directory usage.")
        a_parser.add_argument( self.arg_str + AbstractPlugin.home_dir_str, help="The home directory name.")

        a_parser.set_defaults(func=self.edit_share)

    def build_share(self, args):
        '''
        little utility method to conjure up a share from params
        '''

        share = SmbShare()
        share.share_name = args[AbstractPlugin.name_str]
        share.continuous_availability = self.convertToBool( args[AbstractPlugin.continuous_availability_str] )
        share.smb_signing = self.convertToBool( args[AbstractPlugin.smb_signing_str] )
        share.use_home_dir = self.convertToBool( args[AbstractPlugin.use_home_dir_str] )
        share.home_dir = args[AbstractPlugin.home_dir_str]
        share.share_encryption = args[AbstractPlugin.share_encryption_str]

        return share

    def add_share(self, args):
        '''
        add a share to a volume
        '''

        vs = VolumeService()
        volume = vs.get_volume( args[AbstractPlugin.volume_id_str])

        if ( isinstance( volume, FdsError ) or volume is None ):
            print("Could not find a volume that matched your entry.\n")
            return

        share = self.build_share(args)

        volume.settings.shares.append( share )

        vs.edit_volume(volume)

    def edit_share(self, args):
        '''
        edit a share on a volume
        '''
        vs = VolumeService()
        volume = vs.get_volume( args[AbstractPlugin.volume_id_str])

        if ( isinstance( volume, FdsError ) or volume is None ):
            print("Could not find a volume that matched your entry.\n")
            return

        share = self.build_share(args)
        v_shares = volume.settings.shares

        for v_share in v_shares:
            if v_share.name == share.name:
                v_share = share
            #fi
        #for

        volume.settings.shares = v_shares

        vs.edit_volume(volume)

    def remove_share(self, args):
        '''
        remove a share from a Volume
        '''
        vs = VolumeService()
        volume = vs.get_volume( args[AbstractPlugin.volume_id_str])

        if ( isinstance( volume, FdsError ) or volume is None ):
            print("Could not find a volume that matched your entry.\n")
            return

        for share in enumerate( volume.settings.shares ):
            if share.name == args[AbstractPlugin.name_str]:
                volume.settings.shares.remove( share )
                break

        vs.edit_volume(volume)

    def convertToBool(self, s):

        if ( s.lower() == "true" ):
            return True

        return False

    @property
    def arg_str(self):
        return "-"

