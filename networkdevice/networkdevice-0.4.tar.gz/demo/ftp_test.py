#!/usr/bin/env python

from networkdevice import cisco, junos, linux

tangshan = {
        "name": "tangshan",
        "host": "tangshan",
        "username": "regress",
        "password": "MaRtInI",
        "root_password": "Embe1mpls",
        "color": "purple",
        "noconfig":  True,
        "interface": [
            { "ip": "4.4.4.1/24", "ip6": "2004::1/64", "name": "fe-0/0/6.0", "zone": "trust" },
            { "ip": "2.2.2.2/24", "ip6": "2002::2/64", "name": "fe-0/0/2.0", "zone": "untrust" },
            { "ip": "3.3.3.2/24", "ip6": "2003::2/64", "name": "fe-0/0/3.0", "zone": "untrust" }],
        "preconfig": [ "set routing-options static route 1.1.1.0/24 next-hop 2.2.2.1",
            "set routing-options static route 2001::/64 next-hop 2002::1"] 
        }

ent_vm01 = {
        "name": "ent-vm01",
        "host": "ent-vm01",
        "prompt": "root@ent-vm01 ~",
        "username": "root",
        "password": "Embe1mpls",
        "color": "green",
        "noconfig": True,
        "interface": [ { 'name': 'eth1', 'ip': '4.4.4.2/24', 'ip6': '2004::2/64'} ],
        "preconfig": [
            "ip route add 1.1.1.0/24 via 4.4.4.1 dev eth1",
            "ip -6 route add 2001::/64 via 2004::1 dev eth1"]
        }

ent_vm02 = {
        "name": "ent-vm02",
        "host": "ent-vm02",
        "prompt": "root@ent-vm02 ~",
        "username": "root",
        "password": "Embe1mpls",
        "color": "yellow",
        "noconfig": True,
        "interface": [{'name': 'eth1', 'ip': '1.1.1.2/24', 'ip6': '2001::2/64'}],
        "preconfig": [
            "ip route add 4.4.4.0/24 via 1.1.1.1 dev eth1",
            "ip -6 route add 2004::/64 via 2001::1 dev eth1"]
        }

if __name__ == '__main__':
    '''
    Topology:

                         +----------+
                         |  server  |
                         +----+-----+
                              | int0
                              |
                              | int0
                         +----+-----+
                         |   DUT    |
                         +----------+
                              | int1
                              |
                              | int0
                         +----+-----+
                         |  client  |
                         +----------+
    '''
    # Use device descriptor to create a linux and junos device
    dut = junos.JunosDevice(tangshan)
    client = linux.LinuxDevice(ent_vm01)
    # Use parameter list to create a linux device
    #server = linux.LinuxDevice(name = "ent-vm02", host = "ent-vm02",
    #        prompt = "root@ent-vm02 ~", username = "root", password = "5678")
    server = linux.LinuxDevice(ent_vm02)

    # Dump all the dut's attributes
    dut.dumps()
    # check Juniper srx firewall release version
    print dut.cli('show version')

    # execute a non-interactive command and return the result
    print client.cmd('date')

    # execute an interactive command
    client.cmd('ftp 1.1.1.2', expect = "Name")
    client.cmd('%s' %(server["username"]), expect = "Password")
    client.cmd('%s' %(server["password"]), expect = "ftp")
    print client.cmd('pwd', expect = "ftp")

    # check session in dict format
    displayed = dut.cli('show security flow session application ftp',
            format = "dict",
            force_list=('flow-session'))
    if int(displayed['flow-session-information']['displayed-session-count']) > 0:
        print "session found:"
        for session in displayed['flow-session-information']['flow-session']:
            print "Session ID: %s, Policy name: %s, Timeout: %s, %s"\
                    %(session['session-identifier'],
                            session['policy'],
                            session['timeout'],
                            session['sess-state'])
            for f in session['flow-information']:
                print "  %s: %s/%s --> %s/%s;%s, If: %s, Pkts: %s, Bytes: %s" \
                        %(f['direction'],
                                f['source-address'],
                                f['source-port'],
                                f['destination-address'],
                                f['destination-port'],
                                f['protocol'],
                                f['interface-name'],
                                f['pkt-cnt'],
                                f['byte-cnt'])

    # tear down the ftp session
    client.cmd('bye')
