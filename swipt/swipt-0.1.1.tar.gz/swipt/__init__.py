#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkgutil
import random
import os
import logo
import importlib
import time
import sys


class StoneWorkIsPedroTen(object):
    def __init__(self, *args, **kwargs):
        self.generate_people()
        os.system('clear')
        while True:
            try:
                self.show_menu()
            except (KeyboardInterrupt, EOFError):
                exit(0)

    def generate_people(self):
        people = [name for _, name, _ in pkgutil.iter_modules(['swipt/people'])]
        self.people = sorted(people, key=lambda *args: random.random())

    def load_person(self, person_name):
        self.show_progress('Loading {0}\'s program..'.format(person_name))
        os.system('clear')
        importlib.import_module('swipt.people.{person_name}'.format(person_name=person_name))
        raw_input()
        self.unload_person(person_name)

    def show_menu(self):
        self.show_progress('Loading main menu..')
        os.system('clear')
        self.show_logo()
        self.show_people()
        self.show_selection()

    def show_logo(self):
        print(logo.logo)

    def show_people(self):
        print('Please! Select your friend & colleague :)')
        for i, person in enumerate(self.people):
            print('[{0}] {1}'.format(i, person))
        print('[Q] Quit!')

    def show_selection(self):
        data_ok = False
        while not data_ok:
                try:
                    data = raw_input('Selection: ')
                    data = int(data)
                    data_ok = True
                except ValueError:
                    if data in ('Q', 'q'):
                        exit(0)
                    data_ok = False

        self.load_person(self.people[data])

    def unload_person(self, person_name):
        del sys.modules['swipt.people.{0}'.format(person_name)]

    def show_progress(self, msg):
        i = 0
        sys.stdout.write(msg)
        sys.stdout.flush()
        while i < random.randint(0, 10):
            time.sleep(random.random())
            sys.stdout.write('.')
            sys.stdout.flush()
            i += 1


swipt = StoneWorkIsPedroTen()
