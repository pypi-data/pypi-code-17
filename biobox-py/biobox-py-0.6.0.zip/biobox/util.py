import docker
import docker.utils

from biobox.exception import UnsupportedDockerVersionException

def clean_docker_version_string(s):
    return s.split('-')[0]


def is_supported_docker_version(client_version):
    from packaging import version
    minimum_supported_version = version.parse("1.10.0")
    client_version = version.parse(clean_docker_version_string(client_version))
    return not (client_version < minimum_supported_version)


def client(timeout = 60):
    args = docker.utils.kwargs_from_env(assert_hostname = False)
    args['version'] = '1.20'
    args['timeout'] = timeout
    client  = docker.Client(**args)
    version = client.version()['Version']
    if is_supported_docker_version(version):
        return client
    else:
        msg = "Docker version {} is not supported by bioboxes."
        raise UnsupportedDockerVersionException(msg.format(version))
