import docker

from typing import List


class PortMapping:
    def __init__(self, private_port, public_port):
        self.private_port = private_port
        self.public_port = public_port

    def __repr__(self):
        return '%d:%d' % (self.public_port, self.private_port)


class Container:
    def __init__(self, name: str, status: str, networks: List[str], image: str, ports: List[PortMapping]):
        self.name = name
        self.status = status
        self.networks = networks
        self.image = image
        self.ports = ports

    def is_running(self):
        return self.status == 'running'

    def __repr__(self) -> str:
        return '%s - %s - %s %s' % (self.name, self.status, self.networks, self.ports)


class Configuration:
    def __init__(self, containers: List[Container]):
        self.containers = containers

    def __repr__(self):
        return str([repr(c) for c in self.containers])


class ConfigParser:
    def __init__(self):
        self._client = docker.from_env(assert_hostname=False)

    def get_configuration(self) -> Configuration:
        containers = []

        for cinfo in self._client.containers(all=True):
            name = cinfo['Names'][0]

            if name[0] == '/':
                name = name[1:]

            status = cinfo['State']
            image = cinfo['Image']
            networks = [n for n in cinfo['NetworkSettings']['Networks'].keys()]
            networks.sort()
            ports = [PortMapping(p['PrivatePort'], p['PublicPort']) for p in cinfo['Ports'] if 'PublicPort' in p.keys()]
            containers.append(Container(name, status, networks, image, ports))

        return Configuration(containers)
