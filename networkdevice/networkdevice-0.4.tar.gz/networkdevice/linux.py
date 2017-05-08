#!/usr/bin/env python
import sys
import pexpect
import collections
from StringIO import StringIO

LOG_EMERG = 0
LOG_ALERT = 1
LOG_CRIT = 2
LOG_ERR = 3
LOG_WARNING = 4
LOG_NOTICE = 5
LOG_INFO = 6
LOG_DEBUG = 7

device0 = {
    # mandtory, if not given, it will fail to construct a device
    "name":          "",     # A name of the devices, used for log and
                             # shell prompt;
    "host":          "",     # A ip address or hostname that can connect;
    "username":      "",     # Usename to login;
    "password":      "",     # Password to login;
    "root_password": "",     # Root password, optional for linux devices,
                             # mandtory for Junos devices;

    # Optional, if not given, use the default
    "prompt":    None,       # A shell prompt, if not given, use
                             # username@name, it's not correct, it's better
                             # destinate;
    "fd":        sys.stdout, # log files, default is the stdout;
    "mode":      "ssh",      # login method, default is ssh, support ssh
                             # and telnet now;
    "interface": [],         # A list interface the device will configure;
    "preconfig": [],         # A list of cmd/configuration the device will
                             # configure before test;
    "postconfig": [],        # A list of cmd/configuration the device will
                             # configure after test;
    "noconfig":  False,      # If ture, will not configure the interface
                             # and preconfig before test;
    "color":     "blue",     # log color
    "log_level": LOG_INFO,   # log level
}

class LinuxDevice(object):
    '''
    A base class for common linux devices.
    '''
    version = '0.1'
    color_dict = {'black': '\033[0;30m', 'dark_gray': '\033[1;30m', 'light_gray': '\033[0;37m',
            'blue': '\033[0;34m', 'light_blue': '\033[1;34m', 'green': '\033[0;32m',
            'light_green': '\033[1;32m', 'cyan': '\033[0;36m', 'light_cyan': '\033[1;36m',
            'red': '\033[0;31m', 'light_red': '\033[1;31m', 'purple': '\033[0;35m',
            'light_purple': '\033[1;35m', 'brown': '\033[0;33m', 'yellow': '\033[1;33m',
            'white': '\033[1;37m', 'default_color': '\033[00m', 'red_bold': '\033[01;31m',
            'endc': '\033[0m' }

    def __init__(self, device = None, **kwargs):
        """LinuxDevice constructor with ([field=val,...]) prototype.

        Arguments:

        Devices members to set, every member has a dfault value, if there is no
        such name input, the default value is used.

        officer = {
            # mandtory, if not given, it will fail to construct a device
            "name":          "",     # A name of the devices, used for log and shell prompt;
            "host":          "",     # A ip address or hostname that can connect;
            "username":      "",     # Usename to login;
            "password":      "",     # Password to login;
            "root_password": "",     # Root password, optional for linux devices, mandtory for Junos devices;

            # Optional, if not given, use the default
            "prompt":    None,       # A shell prompt, if not given, use username@name, it's not correct, it's better destinate;
            "fd":        sys.stdout, # log files, default is the stdout;
            "mode":      "ssh",      # login method, default is ssh, support ssh and telnet now;
            "interface": [],         # A list interface the device will configure;
            "preconfig": [],         # A list of cmd/configuration the device will configure before test;
            "postconfig": [],        # A list of cmd/configuration the device will configure after test;
            "noconfig":  False,      # If ture, will not configure the interface and preconfig before test;
            "color":     "blue",     # log color
            "log_level": LOG_INFO,   # log level
        }

        pc1 = LinuxDevice(**officer)

        Example:

            dut = LinuxDevice(host = "ent-vm01", username = "root",
                password = "1234", color = "green")

        After it is constructured, you can add or change the members as
        dictionary, For example:
            
            vm01['color'] = 'brown'
            vm01['interface'] = [
                { "int0": { 'name': 'eth1', 'ip': '1.1.1.2/24', 'zone': 'trust' }
                ]
        """

        self.__items__ = collections.OrderedDict()
        # Default value:
        for k,v in device0.iteritems():
            self[k] = v
        # Device input:
        if device:
            for k,v in device.iteritems():
                self[k] = v
        # kwargs input:
        for k,v in kwargs.iteritems():
            self[k] = v

        if not self["prompt"]:
            self["prompt"] = "\[%s@%s .*\]# " %(self["username"], self["name"])
        if not self["mode"]:
            self["mode"] = 'ssh'

        self.prompt = [pexpect.EOF, pexpect.TIMEOUT, "Are you sure you want to continue connecting",
                "(?i)password:", self['prompt']]
        self.psession = pexpect.spawn('%s -l %s %s' %(self["mode"], self["username"], self["host"]))
        #NOTE: Enable the following line to show the log
        #self.psession.logfile = sys.stdout
        i = self.psession.expect(self.prompt)
        if i == 0 or i == 1:
            tmp = "Login %s failed due to %s\n" %(self["name"], (i == 2) and "EOF" or "TIMEOUT")
            self.log(tmp)
            self.psession.close(force=True)
            raise Exception(tmp)
        elif i == 2:
            self.psession.sendline ('yes')
            i = self.psession.expect(self.prompt)
            if i == 3:
                self.psession.sendline (self["password"])
        elif i == 3:
            self.psession.sendline (self["password"])
        self.log("ssh login succeed.\n")
        self.configure_interface()

    def __del__(self):
        '''
        Recycle resource when the object is destroied.
        '''
        # postconfig
        if self['postconfig']:
            for c in self['postconfig']:
                self.cmd(c)
        self.psession.close(force=True)
        #self.log("%s.%s() finished\n" %(self.__class__.__name__, sys._getframe().f_code.co_name))
        #self.log("destroy complete\n")

    def cmd(self, cmd, expect = None,  **kwargs):
        '''
        Type a cmd line into the Linuxdevice and return the execution result,
        if it timeout or error occur, None is return.

        If the modes is provided, then the expect will include the pattern
        insteading of the shell pattern.

        Supported options include:

            timeout: time to wait for the execute command return. default is 3
                     seconds

        '''
        self.log("%s\n" %(cmd))

        if expect:
            prompt = [pexpect.EOF, pexpect.TIMEOUT, expect]
        else:
            prompt = self.prompt
        self.psession.expect(self.prompt, kwargs.get("timeout", 0.5))
        self.psession.sendline(cmd)
        i = self.psession.expect(prompt, kwargs.get("timeout", 3))

        if (i == 1):
            # If timeout, return None
            self.log('command timeout: %s\n' %(cmd))
            return None

        len1 = self.psession.before.find('%s' %(cmd))
        output = self.psession.before[len1:].strip()
        if output:
            # output might be colorful, so remove the color.
            output += self.color_dict['default_color']
            self.log('%s\n' %(output), LOG_DEBUG)

        return output

    def configure_interface (self):
        """
        Re-configure the interface with the given parameters.
        """
        if self["noconfig"]:
            return
        s = set()
        if self['interface']:
            for i in self['interface']:
                if i['name'] not in s:
                    s.add(i['name'])
                    self.cmd("ip address flush dev %s" %(i['name']))

            for i in self['interface']:
                self.cmd("ip address add %s dev %s" %(i['ip'], i['name']))
                if i.get('ip6') is not None:
                    self.cmd("ip -6 address add %s dev %s" %(i['ip6'], i['name']))
        #preconfig
        if self['preconfig']:
            for c in self['preconfig']:
                self.cmd(c)

    def log (self, message, level = LOG_INFO):
        '''
        Log the message.
        '''
        if level > self["log_level"]:
            return

        color = self.color_dict.get(self['color'], '\033[00m')
        f = StringIO(message)
        for i in f.readlines():
            self["fd"].write("[%s %s \033[0m]: %s" %(color, self['name'], message))
        f.close()

    def dumps(self):
        '''
        dump the attributes.
        '''
        # Default value:
        print "{"
        for k,v in self.__items__.iteritems():
            self[k] = v
            print '    %s: %s' %(k, v)
        print "}"

    def get_file(self, filename, localname = '.'):
        '''
        Get file from remote host, only support scp now, will support other
        methods.
        '''
        self.log("scp %s@%s:%s %s\n" %(self["username"], self["host"], filename, localname))
        clild = pexpect.spawn('scp %s@%s:%s %s' %(self["username"], self["host"], filename, localname))
        i = clild.expect(self.prompt)
        if i == 3:
            clild.sendline ('%s' %(self["password"]))
            clild.expect(pexpect.EOF, timeout=10)
        else:
            print "Failed to get file, i = %d" %(i)

    def put_file(self, filename, remotedir):
        '''
        Put local file to remote host, only support scp now, will support other
        methods.
        '''
        print 'scp %s %s@%s:%s' %(filename, self["username"], self["host"], remotedir)
        clild = pexpect.spawn('scp %s %s@%s:%s' %(filename, self["username"], self["host"], remotedir))
        i = clild.expect(self.prompt)
        if i == 3:
            clild.sendline ('%s' %(self["password"]))
            clild.expect(pexpect.EOF, timeout=10)
        else:
            print "Failed to put file"

    def __getitem__(self, name):
        """
        Get members of the object.
        """
        if name not in self.__items__:
            return None
        else:
            return self.__items__[name]

    def __setitem__(self, name, value):
        """
        Set members to the object.
        """
        self.__items__[name] = value

    def test_color (self):
        print "%sblack%s, %swhite%s" %(linux.Devices.color_dict['black'],
                linux.Devices.color_dict['endc'],
                linux.Devices.color_dict['white'],
                linux.Devices.color_dict['endc'])
        print "%sdark_gray%s, %slight_gray%s" %(linux.Devices.color_dict['dark_gray'],
                linux.Devices.color_dict['endc'],
                linux.Devices.color_dict['light_gray'],
                linux.Devices.color_dict['endc'])
        print "%sblue%s, %slight_blue%s" %(linux.Devices.color_dict['blue'],
                linux.Devices.color_dict['endc'],
                linux.Devices.color_dict['light_blue'],
                linux.Devices.color_dict['endc'])
        print "%sgreen%s, %slight_green%s" %(linux.Devices.color_dict['green'],
                linux.Devices.color_dict['endc'],
                linux.Devices.color_dict['light_green'],
                linux.Devices.color_dict['endc'])
        print "%scyan%s, %slight_cyan%s" %(linux.Devices.color_dict['cyan'],
                linux.Devices.color_dict['endc'],
                linux.Devices.color_dict['light_cyan'],
                linux.Devices.color_dict['endc'])
        print "%sred%s, %slight_red%s" %(linux.Devices.color_dict['red'],
                linux.Devices.color_dict['endc'],
                linux.Devices.color_dict['light_red'],
                linux.Devices.color_dict['endc'])
        print "%spurple%s, %slight_purple%s" %(linux.Devices.color_dict['purple'],
                linux.Devices.color_dict['endc'],
                linux.Devices.color_dict['light_purple'],
                linux.Devices.color_dict['endc'])
        print "%sbrown%s, %syellow%s" %(linux.Devices.color_dict['brown'],
                linux.Devices.color_dict['endc'],
                linux.Devices.color_dict['yellow'],
                linux.Devices.color_dict['endc'])
        print "%sdefault_color%s, %sred_bold%s" %(linux.Devices.color_dict['default_color'],
                linux.Devices.color_dict['endc'],
                linux.Devices.color_dict['red_bold'],
                linux.Devices.color_dict['endc'])

if __name__ == '__main__':
    ent_vm01 = { "host": "ent-vm01",
            "username": "root",
            "password": "1234",
            "color": "green",
            "interfaces": [ { 'name': 'eth1', 'ip': '1.1.1.2/24', 'zone': 'trust' } ]
            }
    pc1 = LinuxDevice(host = "alg-vm11", username = "root", password = "1234", color = "green")
    pc2 = LinuxDevice(ent_vm01)
    print pc1.cmd("pwd")
    print pc2.cmd("ifconfig")
