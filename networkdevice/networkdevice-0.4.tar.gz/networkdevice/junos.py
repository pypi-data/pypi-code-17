#!/usr/bin/env python

import linux
import json
import pexpect
import xmltodict
import sys

class JunosDevice(linux.LinuxDevice):
    '''
    A base class for common Juniper Junos devices.
    '''
    version = '0.1'
    def __init__(self, device = None, **kwargs):

        linux.LinuxDevice.__init__(self, device, **kwargs)
        if self["username"] != 'root':
            prompt = 'root@%s%%' %(self["name"])
            self.prompt.append(prompt)

            self.psession.sendline('start shell')
            i = self.psession.expect('%')

            self.psession.sendline('su')
            i = self.psession.expect('(?i)password:')
            self.psession.sendline(self['root_password'])
            i = self.psession.expect(self.prompt)

        # Junos is always in configure mode.
        self.psession.sendline("cli")
        i = self.psession.expect("%s@%s>" %(self["username"], self["name"]))
        self.prompt.append("\[edit\]\r\n%s@%s#" %(self["username"], self["name"]))
        self.prompt.append("%s@%s%%" %("root", self["name"]))
        self.psession.sendline("configure")
        i = self.psession.expect(self.prompt)
        self.configure_junos_interface()

    def __del__(self):
        '''
        Recycle resource when the object is destroied.
        '''
        #postconfig
        if self['postconfig']:
            for c in self['postconfig']:
                self.configure(c)
            self.configure("commit")
        linux.LinuxDevice.__del__(self)

    def cmd(self, cmd, mode = "shell",  **kwargs):
        '''
        There are total 4 modes for junos devices:

            1) shell: execute the command in shell mode and return the result,
                this is the default mode and it looks like linux.cmd().

            2) cli: execute the command in cli mode and return the result,
                self.cmd(cmd, mode = "cli") equal to self.cli(cmd), see detail
                in seld.cli()

            3) configure: execute the command in configure mode and return the
                result, self.cmd(cmd, mode = "configure") equal to
                self.configure(cmd), see detail in seld.configure()

            4) vty: execute the command in vty mode and return the result,
                self.cmd(cmd, mode = "vty") equal to self.vty(cmd), see detail
                in seld.vty()

        Supported options include:

            timeout: time to wait for the execute command return. default is 5
                     seconds

        '''
        if mode == "shell":
            self.configure("run start shell csh")
            self.log("%s\n" %(cmd))
            self.psession.sendline(cmd)
            i = self.psession.expect(self.prompt, 5)
            if (i == 1):
                # If timeout, return None
                self.log('command timeout: %s\n' %(cmd))
                output = None
            else:
                len1 = self.psession.before.find('\n')
                output = self.psession.before[len1:].strip()
                self.log("%s\n" %(output), level = linux.LOG_DEBUG)

            self.configure("exit")
            return output
        elif mode == "cli":
            return self.cli(cmd, **kwargs)
        elif mode == "configure":
            return self.configure(cmd, **kwargs)
        elif mode == "vty":
            return self.vty(cmd, **kwargs)

        return None

    def cli(self, cmd, **kwargs):
        '''
        Execute a cli command and return the result.

        Supported options include:

            timeout: time to wait for the execute command return. default is 5
                     seconds

            display: Junos command options, Show additional kinds of
                information, possible completions are "xml" and "json". Please
                note that "json" is supported since X49.

            format: Which kind object you'd like the cmd return. Options
                include "text", "dict" and "json". Default is "text" and it's
                return directly from the cmd result. if "dict" or "json" is
                selected, the result will be parsed to python dict or json
                object.

            force_list: When we parse the dictionaly from xml output, to force
                lists to be created even when there is only a single child of a
                given level of hierarchy. The force_list argument is a tuple of
                keys. If the key for a given level of hierarchy is in the
                force_list argument, that level of hierarchy will have a list
                as a child (even if there is only one sub-element). The
                index_keys operation takes precendence over this. This is
                applied after any user-supplied postprocessor has already run.

                For example, given this input:

                    <servers>
                      <server>
                        <name>host1</name>
                        <os>Linux</os>
                        <interfaces>
                          <interface>
                            <name>em0</name>
                            <ip_address>10.0.0.1</ip_address>
                          </interface>
                        </interfaces>
                      </server>
                    </servers>

               If called with:

                   dut.cmd("balabala", display = "xml", force_list=('interface',))
                      
              it will produce this dictionary:

                  {'servers':
                    {'server':
                      {'name': 'host1',
                       'os': 'Linux'},
                       'interfaces':
                        {'interface':
                          [ {'name': 'em0', 'ip_address': '10.0.0.1' } ] } } }
        '''

        cmd = 'run ' + cmd
        return self.configure(cmd, **kwargs)


    def configure(self, cmd, **kwargs):
        '''
        Execute a configure command and return the result. Sematics is like
        self.cli, see detail in self.cli()
        '''

        if kwargs.get("display"):
            cmd += ' | display %s | no-more' %(kwargs.get("display"))
        elif kwargs.get("format") == "dict":
            cmd += ' | display xml | no-more'
        elif kwargs.get("format") == "json":
            cmd += ' | display json | no-more'

        self.log("%s\n" %(cmd))
        self.psession.sendline(cmd)
        i = self.psession.expect(self.prompt, kwargs.get("timeout", 30))
        if (i == 1):
            # If timeout, return None
            self.log('command timeout: %s\n' %(cmd))
            return None

        len1 = self.psession.before.find('\n')
        output = self.psession.before[len1:].strip()
        if not output:
            return None

        self.log("%s\n" %(output), level = linux.LOG_DEBUG)
        if kwargs.get("format") == "dict":
            if kwargs.get("display") == "json":
                result = dict(json.loads(output))
            else:
                result = xmltodict.parse(output, force_list = kwargs.get("force_list")).get("rpc-reply")
        elif kwargs.get("format") == "json":
            if kwargs.get("display") == "xml":
                dic = xmltodict.parse(output).get("rpc-reply")
                result = json.dumps(dic)
            else:
                result = json.loads(output)
        else:
            result = output

        return result

    def vty(self, cmd, **kwargs):
        '''
        Execute a vty command and return the result.

        Supported options include:

            timeout: time to wait for the execute command return. default is 5
                     seconds

            tnp_addr: tnp address to login.
        '''
        #self.log("%s %s\n" %(cmd, str(kwargs)))
        if kwargs.get("tnp_addr"):
            vty_cmd = 'cprod -A %s -c "%s"' %(kwargs.get("tnp_addr"), cmd)
        else:
            vty_cmd = 'cprod -c "%s"' %(cmd)
        return self.cmd(vty_cmd)

    def configure_interface (self):
        """
        Must be empty for overload.
        """
        #print "%s.%s(%d) invoked" %(self.__class__.__name__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)
        return

    def configure_junos_interface (self):
        """
        Re-configure the interface with the given parameters.
        """
        #print "%s.%s(%d) invoked" %(self.__class__.__name__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)
        if self["noconfig"]:
            return

        if self['interface']:
            self.configure('delete security zones')

            s = set()
            for i in self['interface']:
                if i['name'] not in s:
                    s.add(i['name'])
                    name = i['name'].split('.')
                    self.configure("delete interfaces %s unit %s family inet" %(name[0], name[1]))
                    self.configure("delete interfaces %s unit %s family inet6" %(name[0], name[1]))

            for i in self['interface']:
                # configure interface.
                name = i['name'].split('.')
                self.configure("set interfaces %s unit %s family inet address %s" %(name[0], name[1], i["ip"]))
                if i.get('ip6') is not None:
                    self.configure("set interfaces %s unit %s family inet6 address %s" %(name[0], name[1], i["ip6"]))

                # configure zone.
                z = i.get('zone')
                if z is not None:
                    self.configure('set security zones security-zone %s host-inbound-traffic system-services all' %(z))
                    self.configure('set security zones security-zone %s host-inbound-traffic protocols all' %(z))
                    self.configure('set security zones security-zone %s interfaces %s' %(z, i['name']))

        #preconfig
        if self['preconfig']:
            for c in self['preconfig']:
                self.configure(c)

        self.configure("commit")

    def install_image (self, image):
        '''
        To be implemented.
        '''
        self.cli("request system software add %s no-copy no-validate reboot" %(image))
        #self.dut.put_file('~/client.pcap')

    def print_session (self, sessions):
        for session in sessions:
            print "Session ID: %s, Policy name: %s, Timeout: %s, %s"\
                    %(session['session-identifier'], session['policy'],
                            session['timeout'], session['sess-state'])
            for f in session['flow-information']:
                print "  %s: %s/%s --> %s/%s;%s, Conn tag: %s, If: %s, Pkts: %s, Bytes: %s" \
                        %(f['direction'], f['source-address'], f['source-port'],
                        f['destination-address'], f['destination-port'],
                        f['protocol'], f['conn-tag'],
                        f['interface-name'], f['pkt-cnt'],
                        f['byte-cnt'])

if __name__ == '__main__':
    dut = {
            "name": "tangshan",
            "host": "tangshan",
            "username": "dev",
            "password": "1234",
            "root_password": "5678",
            "noconfig":  True,
            "interface": [
                { "ip": "2.2.2.2/24", "ip6": "2002::2/64", "name": "fe-0/0/2.0", "zone": "untrust" },
                { "ip": "4.4.4.1/24", "ip6": "2004::1/64", "name": "fe-0/0/6.0", "zone": "trust" }],
            "preconfig": [ "set routing-options static route 1.1.1.0/24 next-hop 2.2.2.1"] 
            }
    print dut.cli("show version")

