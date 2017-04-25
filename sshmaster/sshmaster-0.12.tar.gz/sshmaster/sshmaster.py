#!/usr/bin/env python
import os
import paramiko
import sys
import optparse
from types import *
import vmtools
import time
from gmailer.gmailer import senderror_simple
from scp import SCPClient

vm_root_path = vmtools.vm_root_grabber()
sys.path.append(vm_root_path)
from local_settings import *

def scp_cmd(current_host, mode, username, keyfile, local_file, remote_file, recursive=False, preserve_times=False, port=22):
    """sends or gets a file via scp
    :type current_host: string
    :param current_host: the remote host to copy to or from
    :type mode: string
    :param mode: put or get
    :type local_file: string
    :param local_file: the absolute path to the local file
    :type remote_file: string
    :param remote_file: the absolute path to the remote file
    :type recursive: boolean
    :param recursive: boolean option False if a single file True if a directory
    :type preserve_times: boolean
    :param preserve_times: boolean option False if no True if yes
    :type username: string
    :param username: the username to use when connecting
    :type keyfile: string
    :param keyfile: the absolute path to the private ssh key
    :type port: intr
    :param port: the port to connect on
    :type print_stdout: boolean
    :param print_stdout: Wether to print the stdout to terminal
    """

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(current_host, username=username, key_filename=keyfile, port=port )
    scp = SCPClient(ssh.get_transport())
    if mode == 'put':
        scp.put(files=local_file, remote_path=remote_file, recursive=recursive, preserve_times=preserve_times)
    if mode == 'get':
        scp.get(remote_path=remote_file, local_path=local_file, recursive=recursive, preserve_times=preserve_times)

# function for running a shell command on a host
def ssh_cmd(current_host, command, username, keyfile, port=22, print_stdout=True):
    """runs a commad via ssh on the host: current_host and returns a dictionary of the results
    :type current_host: string
    :param current_host: the host you want to run your command on
    :type command: string
    :param command: the command you wish to run
    :type username: string
    :param username: the username to use when connecting
    :type keyfile: string
    :param keyfile: the absolute path to the private ssh key
    :type port: intr
    :param port: the port to connect on
    :type print_stdout: boolean
    :param print_stdout: Wether to print the stdout to terminal
    """
    # make sure command ends in a new line
    if not command.endswith('\n'):
        command = command+'\n'
    # establish our dict for returning
    ssh_cmd_dict = {}
    # fill in the stuff we know
    #ssh_cmd_dict['server'] = current_host
    ssh_cmd_dict['current_host'] = current_host
    ssh_cmd_dict['command'] = command
    # make the ssh object
    ssh = paramiko.SSHClient()
    # add new servers to known_hosts automatically
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # try to establish the connection to server
    try:
        ssh.connect(current_host, username=username, key_filename=keyfile, port=port )
    except:
        # record connection failure
        ssh_cmd_dict['connection_successful'] = False
        # if it doesn't work tell 'em
        print('unable to connect to: '+current_host)
        return ssh_cmd_dict
    else:
        # record connection success
        ssh_cmd_dict['connection_successful'] = True
        # execute the command storing stdout, stdin, and stderr
        stdin, stdout, stderr = ssh.exec_command(command)
        # wait for the end of line from stdout so we know the command has finished
        while not stdout.channel.eof_received:
            time.sleep(3)
        # wait for exit status (that means command finished)
        exit_status = stdout.channel.recv_exit_status()
        # flush commands and cut off more writes
        stdin.flush()
        stdin.channel.shutdown_write()

        # close the connection
        ssh.close()

        # store the stdout
        ssh_cmd_dict['stdout_raw'] = stdout.readlines()

        # create an entry that is pretty to read
        if type(ssh_cmd_dict['stdout_raw']) is ListType:
            ssh_cmd_dict['stdout_print'] = "".join(ssh_cmd_dict['stdout_raw'])
        ssh_cmd_dict['stdout'] = ssh_cmd_dict['stdout_raw']

        # store stdin
        ssh_cmd_dict['stdin'] = command

        # store the stderr
        ssh_cmd_dict['stderr_raw'] = stderr.readlines()
        # create an entry for stderr that is pretty to read
        if type(ssh_cmd_dict['stderr_raw']) is ListType:
            ssh_cmd_dict['stderr_print'] = "".join(ssh_cmd_dict['stderr_raw'])
        ssh_cmd_dict['stderr'] = ssh_cmd_dict['stderr_raw']

        # store exit status
        ssh_cmd_dict['exitstatus'] = exit_status

        if exit_status > 0:
            if ssh_cmd_dict['stderr'] is not None:
                print('Unfortunately the command: '+command+' executed on server: '+current_host+' had a non-zero exit status. Below is the stderr:')
                print(ssh_cmd_dict['stderr'])
        else:
            if print_stdout:
                if ssh_cmd_dict['stdout_print'] is not None:
                    print(ssh_cmd_dict['stdout_print'])
        return ssh_cmd_dict


def ssh_cmd_auto_check(current_host, command, username, keyfile, port=22, print_stdout=True):
    """runs a commad via ssh on the host: current_host and returns a dictionary of the results, if the connection is not successful or the exitstatus is non-zero send an email to error recipients and exit with an error
    :type current_host: string
    :param current_host: the host you want to run your command on
    :type command: string
    :param command: the command you wish to run
    :type username: string
    :param username: the username to use when connecting
    :type keyfile: string
    :param keyfile: the absolute path to the private ssh key
    :type port: intr
    :param port: the port to connect on
    :type print_stdout: boolean
    :param print_stdout: Wether to print the stdout to terminal
    """
    ssh_cmd_output = ssh_cmd(current_host, command, username=username, keyfile=keyfile, port=port, print_stdout=True)
    if not ssh_cmd_output['connection_successful'] or ssh_cmd_output['exitstatus'] != 0:
        subject_text="command executed on %s failed " % current_host
        body_text = "Executed on: %s\nCommand: %s\nConnection_successful: %s\nStdout: %s\nStderr: %s\nExit Status: %s\n" %( current_host, ssh_cmd_output['command'], ssh_cmd_output['connection_successful'], ssh_cmd_output['stdout_print'], ssh_cmd_output['stderr_print'], ssh_cmd_output['exitstatus'])
        senderror_simple(subject_text, body_text)
        print(body_text)
        sys.exit(1)
    return ssh_cmd_output

