#
# SSH support for Rumba
#
#    Sander Vrijders  <sander.vrijders@intec.ugent.be>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301  USA
import os
import paramiko

import rumba.log as log


logger = log.get_logger(__name__)


def get_ssh_client():
    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    return ssh_client


def _print_stream(stream):
        o = str(stream.read()).strip('b\'\"\\n')
        if o != "":
            o_array = o.split('\\n')
            for oi in o_array:
                logger.debug(oi)
        return o


def execute_commands(testbed, ssh_config, commands, time_out=3):
    """
    Remote execution of a list of shell command on hostname. By
    default this function will exit (timeout) after 3 seconds.

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param commands: *nix shell command
    @param time_out: time_out value in seconds, error will be generated if
    no result received in given number of seconds, the value None can
    be used when no timeout is needed
    """
    ssh_client = get_ssh_client()

    if ssh_config.proxycommand is not None:
        proxy = paramiko.ProxyCommand(ssh_config.proxycommand)
    else:
        proxy = None

    try:
        ssh_client.connect(ssh_config.hostname, ssh_config.port,
                           testbed.username, testbed.password,
                           look_for_keys=True, timeout=time_out,
                           sock=proxy)
        o = ""
        for command in commands:
            logger.debug("%s@%s:%s >> %s" % (testbed.username,
                         ssh_config.hostname,
                         ssh_config.port,
                         command))
            envars = '. /etc/profile;'
            command = envars + ' ' + command
            stdin, stdout, stderr = ssh_client.exec_command(command)
            o = _print_stream(stdout)
            _print_stream(stderr)
        ssh_client.close()
        return o

    except Exception as e:
        logger.error(str(e))
        return


def execute_command(testbed, ssh_config, command, time_out=3):
    """
    Remote execution of a list of shell command on hostname. By
    default this function will exit (timeout) after 3 seconds.

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param command: *nix shell command
    @param time_out: time_out value in seconds, error will be generated if
    no result received in given number of seconds, the value None can
    be used when no timeout is needed

    @return: stdout resulting from the command
    """
    o = execute_commands(testbed, ssh_config, [command], time_out)
    if o is not None:
        return o


def copy_file_to_testbed(testbed, ssh_config, text, file_name):
    """
    Write a string to a given remote file.
    Overwrite the complete file if it already exists!

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param text: string to be written in file
    @param file_name: file name (including full path) on the host
    """
    ssh_client = get_ssh_client()

    if ssh_config.proxycommand is not None:
        proxy = paramiko.ProxyCommand(ssh_config.proxycommand)
    else:
        proxy = None

    try:
        ssh_client.connect(ssh_config.hostname, ssh_config.port,
                           testbed.username,
                           testbed.password,
                           look_for_keys=True,
                           sock=proxy)

        cmd = "touch " + file_name + \
              "; chmod a+rwx " + file_name

        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        del stdin, stdout
        err = str(stderr.read()).strip('b\'\"\\n')
        if err != "":
            logger.error(err)

        sftp_client = ssh_client.open_sftp()
        remote_file = sftp_client.open(file_name, 'w')

        remote_file.write(text)
        remote_file.close()

    except Exception as e:
        logger.error(str(e))


def copy_paths_to_testbed(testbed, ssh_config, paths, destination):
    """
    Write a string to a given remote file.
    Overwrite the complete file if it already exists!

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param paths: source paths (local) as an iterable
    @param destination: destination folder name (remote)
    """
    ssh_client = get_ssh_client()

    if ssh_config.proxycommand is not None:
        proxy = paramiko.ProxyCommand(ssh_config.proxycommand)
    else:
        proxy = None

    if destination is not '' and not destination.endswith('/'):
        destination = destination + '/'

    try:
        ssh_client.connect(ssh_config.hostname, ssh_config.port,
                           testbed.username,
                           testbed.password,
                           look_for_keys=True,
                           sock=proxy)

        sftp_client = ssh_client.open_sftp()

        for path in paths:
            file_name = os.path.basename(path)
            dest_file = destination + file_name
            logger.debug("Copying %s to %s@%s:%s path %s" % (
                path,
                testbed.username,
                ssh_config.hostname,
                ssh_config.port,
                dest_file))
            sftp_client.put(path, dest_file)

    except Exception as e:
        logger.error(str(e))


def copy_path_to_testbed(testbed, ssh_config, path, destination):
    """
    Write a string to a given remote file.
    Overwrite the complete file if it already exists!

    @param testbed: testbed info
    @param ssh_config: ssh config of the node
    @param path: source path (local)
    @param destination: destination folder name (remote)
    """
    copy_paths_to_testbed(testbed, ssh_config, [path], destination)


def setup_vlan(testbed, node, vlan_id, int_name):
    """
    Gets the interface (ethx) to link mapping

    @param testbed: testbed info
    @param node: the node to create the VLAN on
    @param vlan_id: the VLAN id
    @param int_name: the name of the interface
    """
    if testbed.username == 'root':
        def sudo(s):
            return s
    else:
        def sudo(s):
            return 'sudo ' + s

    logger.debug("Setting up VLAN on node %s, if %s.", node.name, int_name)

    args = {'ifname': str(int_name), 'vlan': str(vlan_id)}

    cmds = [sudo("ip link add link %(ifname)s name "
                 "%(ifname)s.%(vlan)s type vlan id %(vlan)s"
                 % args),
            sudo("ifconfig %(ifname)s.%(vlan)s up"
                 % args)]
    # TODO: is ethtool needed? Should install or check if it is present.
    # cmds += [sudo("ethtool -K %(ifname)s rxvlan off"
    #               % args),
    #          sudo("ethtool -K %(ifname)s txvlan off"
    #               % args)]
    execute_commands(testbed, node.ssh_config, cmds)
