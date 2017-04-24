'''
Created on Mar 14, 2017

@author: nate
'''
import json
from fdscli.model.volume.smb_share import SmbShare

class SmbShareConverter(object):
    '''
    Converts shares to and from JSON
    '''


    @staticmethod
    def to_json( share ):
        '''
        convert to JSON string
        '''
        j_share = dict()
        
        j_share["name"] = share.share_name
        j_share["smb_signing"] = share.smb_signing
        j_share["continuous_availability"] = share.continuous_availability
        j_share["use_home_dir"] = share.use_home_dir
        j_share["home_dir"] = share.home_dir
        j_share["share_encryption"] = share.share_encryption
        
        j_share = json.dumps( j_share )
        
        return j_share
        
    @staticmethod
    def build_from_json( j_share ):
        
        share = SmbShare();
        
        if not isinstance( j_share, dict ):
            j_share = json.loads( j_share )
            
        share.smb_signing = j_share.pop( "smb_signing", share.smb_signing )
        share.continuous_availability = j_share.pop( "continuous_availability", share.continuous_availability )
        share.use_home_dir = j_share.pop( "use_home_dir", share.use_home_dir )
        share.home_dir = j_share.pop( "home_dir", share.home_dir )
        share.share_encryption = j_share.pop( "share_encryption", share.share_encryption )
        share.share_name = j_share.pop( "name", share.share_name )
        
        return share