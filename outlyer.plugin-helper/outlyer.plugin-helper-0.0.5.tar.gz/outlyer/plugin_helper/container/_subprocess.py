import subprocess
import docker
from outlyer.plugin_helper.container import is_container, get_container_id


def check_output(cmd):
    if is_container():
        cid = get_container_id()
        client = docker.from_env()
        target = client.containers.get(cid)
        return target.exec_run(cmd)

    elif is_patched():
        return getattr(subprocess, '_check_output')(cmd)

    else:
        return subprocess.check_output(cmd)


def patch():
    if not is_patched():
        subprocess._check_output = subprocess.check_output
        subprocess.check_output = check_output


def unpatch():
    if is_patched():
        subprocess.check_output = getattr(subprocess, '_check_output')
        delattr(subprocess, '_check_output')


def is_patched():
    return hasattr(subprocess, '_check_output')
