from contextlib import contextmanager
from paramiko import SSHClient, SFTPClient, AutoAddPolicy
from invoke import run as local_run

try:
    import hdv_logging as logging
except ImportError as e:
    from hdv_dummy import Dummy
    logging = Dummy()
log = logging.hdvlogging()

settings_container = list()

class ParamikoClientFactory():
    
    def __init__(self):
        self.settings = None
        
    def get_object(self, name, settings):
        self.settings = settings
        method = getattr(self, name + '_client')
        return method()
        
    def ssh_client(self):
        from paramiko import SSHClient
        key_filename = None
        if self.settings.key_file:
            key_filename = self.settings.key_file
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(self.settings.host, port=self.settings.port, username=self.settings.user_name, key_filename=key_filename)
        return client
    
    def sftp_client(self):
        from paramiko import SFTPClient, Transport, RSAKey
        # key_file = '/Users/hotdev/.ssh/id_rsa'
        key_file = self.get_user_key_file()
        my_key = RSAKey.from_private_key_file(key_file)
        transport = Transport((self.settings.host, self.settings.port))
        transport.connect(username=self.settings.user_name, pkey=my_key)
        client = SFTPClient.from_transport(transport)
        return client
    
    def get_user_key_file(self):
        if self.settings.key_file is not None:
            return self.settings.key_file
        # try to get users key file from user's home directory
        import os
        home = os.getenv('HOME')
        expecting_key_file = home + '/.ssh/id_rsa'
        if not os.path.isfile(expecting_key_file):
            raise EnvironmentError("Could not load key file")
        return expecting_key_file
        
class Setting():
    def __init__(self, host=None, user_name=None, password=None, key_file=None, name=None, port=22, quiet=False, capture=False):
        self.host = host
        self.user_name = user_name
        self.passoword = password
        self.key_file = key_file
        self.port = port
        self.quiet = quiet
        self.capture = capture
        # for run command on specific setting
        self.name = name
        if self.name is None:
            self.name = host
        # paramiko instance
        self.ssh = ParamikoClientFactory()
        self.sftp = ParamikoClientFactory()

    def __getattribute__(self, name):
        attr = super().__getattribute__(name);
        if isinstance(attr, ParamikoClientFactory):
            return self.init_for_paramiko(name)
        return attr
    
    def init_for_paramiko(self, name):
        attr = super().__getattribute__(name)
#         client = attr.get_object(name)
#         client.set_missing_host_key_policy(AutoAddPolicy())
#         client.connect(self.host, port=self.port, username=self.user_name)
        super().__setattr__(name, attr.get_object(name, self))
        return super().__getattribute__(name)
        
    def connect_to_host(self, client):
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(self.host, port=self.port, username=self.user_name)
        
    def prepare_pm(self):
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(self.host, port=self.port, username=self.user_name)
        pass
    

@contextmanager
def settings(host, user_name='', password='', key_file=None, setting_object=None, quiet=False, capture=False):
    global settings_container
    if isinstance(host, list):
        for h in host:
            settings_container.append(Setting(host=h, user_name=user_name, password=password, key_file=key_file, quiet=quiet, capture=capture))
    else:
        settings_container = [Setting(host=host, user_name=user_name, password=password, key_file=key_file, quiet=quiet, capture=capture)]
    if setting_object is not None:
        if isinstance(setting_object, list):
            for s in setting_object:
                add_setting(s)
        else:
            add_setting(setting_object)
    yield

def add_setting(setting_object):
    global settings_container
    if setting_object is not None:
        if not isinstance(setting_object, Setting) :
            raise TypeError('setting_object has to be instance of Setting()')
        settings_container.append(setting_object)

def run(command, quiet=False, only_for=None, exclude_for=None, output=True, capture=False):
    if isinstance(command, list) :
        command = ';'.join(command)
    captured_result = []
    
    def context(s):
        host_info = s.user_name + "@" + s.host
        stdin, stdout, stderr = s.ssh.exec_command(command)
        err = stderr.readlines()
#         if err:
#             log.info(stderr.channel.__dict__)
#             log.info(stderr.__dict__)
#             log.info(dir(stderr))
        if (quiet or s.quiet) and (capture is False and s.capture is False):
            return
        
        #print("stdin->{0}".format(stdin))
        should_capture = False
        if capture is True or s.capture is True:
            should_capture = True
            error = []
            result = []
            
        print("[{0}] {1}".format(host_info, command), end="\n")
        if err:
            for e in err:
                if should_capture:
                    error.append(e)
                else:
                    print("[{0}] error: {1}".format(host_info, e), end="")
        out = stdout.readlines()
        if out:
            for r in out:
                if should_capture:
                    result.append(r)
                else:
                    print("[{0}] out: {1}".format(host_info, r), end="")
        
        if should_capture:
            captured_result.append(
                                   {
                                    'host':s.host,
                                    'user':s.user_name,
                                    'command':command,
                                    'result':result,
                                    'error':error
                                    })
            
    run_command(context)
    if captured_result:
        return captured_result

def upload(local, remote):

    def context(s):
        s.sftp.put(local, remote)
    
    run_command(context)

def download(local, remote):
    
    def context(s):
        s.sftp.get(remote, local)
    
    run_command(context)

def run_command(command):
    for s in settings_container:
        command(s)
        
def local(command):
    if isinstance(command, list):
        command = ';'.join(command)
    return local_run(command)
