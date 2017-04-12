import sys
import shlex
import subprocess


def syscall(command):
    """Makes a syscall based on the specified command, returns stdout result of the command call"""
    if sys.platform == 'win32':
        process = subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE,
            shell=True
        )
    else:
        process = subprocess.Popen(
            ["set -o pipefail && " + command],
            stdout=subprocess.PIPE,
            shell=True,
            executable='/bin/bash'
        )
    stdout_text = ""
    with process.stdout as stdo:
        stdout_text = stdo.read().decode('utf-8')
    process.wait()
    if process.returncode == 124:
        return "ERRTIMEOUT"
    if process.returncode == 1:
        return "UNKNOWNFAIL: {}".format(stdout_text)
    return stdout_text
