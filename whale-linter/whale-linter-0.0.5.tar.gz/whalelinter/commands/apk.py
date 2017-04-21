#!/usr/bin/env python3
from whalelinter.app              import App
from whalelinter.dispatcher       import Dispatcher
from whalelinter.commands.command import PackageManager


@Dispatcher.register(token='run', command='apk')
class Apk(PackageManager):

    _callbacks      = {}

    def __init__(self, **kwargs):
        PackageManager.__init__(self, kwargs.get('token'), kwargs.get('command'), kwargs.get('args'), kwargs.get('lineno'))

        Apk.register(self)(type(self).add)

        for method in self.methods:
            if self.subcommand == method:
                self.react(method)

    def add(self):
        print(self.full_command)
