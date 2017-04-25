'''
Created on Mar 13, 2017

@author: nate
'''
from fdscli.model.volume.settings.nfs_settings import NfsSettings
from fdscli.model.common.size import Size

class SmbSettings(NfsSettings):
    '''
    The settings for the SMB volume type which are remarkably close to those of NFS.
    
    A few properties are added and two options are different.
    '''


    def __init__(self, supported_version="all", use_acls=False, clients="*",
        max_object_size=None, capacity=None, encryption=False, compression=False,
        allow_mount=True, replica=False, shares=None):
        '''
        Constructor
        '''
        # Default parameter values are evaluated once when the def statement
        # executes. Do not initialize objects in the def statement unless you
        # intentionally wish to refer to the same object everywhere.
        if capacity is None:
            capacity = Size(1, "TB")

        if max_object_size is None:
            max_object_size = Size(1048576, "B")
            
        if shares is None:
            shares = []
        
        self.type="SMB"
        self.max_object_size = max_object_size
        self.use_acls = use_acls
        self.compression = compression
        self.encryption = encryption
        self.allow_mount = allow_mount
        self.clients = clients
        self.capacity = capacity
        self.shares = shares
        self.replica = replica
        self.supported_version = supported_version
        
    @property
    def shares(self):
        return self.__shares
    
    @shares.setter
    def shares(self, share_list):
        self.__shares = share_list
        
    @property
    def supported_version(self):
        return self.__version
    
    @supported_version.setter
    def supported_version(self, a_version):
        self.__version = a_version
        