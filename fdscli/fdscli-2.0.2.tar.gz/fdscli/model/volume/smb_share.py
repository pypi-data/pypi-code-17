'''
Created on Mar 13, 2017

@author: nate
'''

class SmbShare(object):
    '''
    Represents an SMB share today
    '''


    def __init__(self, share_name=None, use_home_dir=False, home_dir=None, 
        smb_signing=False, continuous_availability=False, share_encryption=None):
        
        self.share_encryption = share_encryption
        self.share_name = share_name
        self.use_home_dir = use_home_dir
        self.home_dir = home_dir
        self.continuous_availability = continuous_availability
        self.smb_signing = smb_signing

    @property
    def share_name(self):
        return self.__share_name
    
    @share_name.setter
    def share_name(self, a_name):
        self.__share_name = a_name
    
    @property
    def use_home_dir(self):
        return self.__use_home_dir
    
    @use_home_dir.setter
    def use_home_dir(self, should_i):
        self.__use_home_dir = should_i
        
    @property
    def home_dir(self):
        return self.__home_dir
    
    @home_dir.setter
    def home_dir(self, a_dir):
        self.__home_dir = a_dir
        
    @property
    def share_encryption(self):
        return self.__share_encryption
    
    @share_encryption.setter
    def share_encryption(self, enc_type):
        
        acceptable_value = (None, "AES_GCM", "AES_CCM")
        
        if enc_type not in acceptable_value:
            raise TypeError( "{} is not a valid type.  (None, AES_GCM, AES_CCM)".format( enc_type) )
        
        self.__share_encryption = enc_type
        
    @property
    def continuous_availability(self):
        return self.__continuous_availability
    
    @continuous_availability.setter
    def continuous_availability(self, is_it):
        self.__continuous_availability = is_it
        
    @property
    def smb_signing(self):
        return self.__smb_signing
    
    @smb_signing.setter
    def smb_signing(self, is_it):
        self.__smb_signing = is_it