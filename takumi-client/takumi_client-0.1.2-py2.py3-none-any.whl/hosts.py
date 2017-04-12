# -*- coding: utf-8 -*-


class ListHosts(object):
    def __init__(self, conf, target):
        self.hosts = conf['hosts']
        self.target = target

    def update(self):
        for host in set(self.target).difference(self.hosts):
            self.target.pop(host)
        for host in self.hosts:
            self.target.setdefault(host, 0)
