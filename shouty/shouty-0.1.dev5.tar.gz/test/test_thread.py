#!/usr/bin/env python3
from sys import argv
from time import sleep
from threading import Thread
import shouty


class TestThread(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.params = {
            'user': 'source',
            'password': 'hackme',
            'format': shouty.Format.MP3,
            'mount': '/shouty'
        }

    def run(self):
        print('Running')
        with shouty.connect(**self.params) as connection:
            for file_name in argv[1:]:
                connection.send_file(file_name)


class OtherThread(Thread):
    def run(self):
        while True:
            sleep(1)


try:
    other_thread = OtherThread()
    other_thread.start()
    test_thread = TestThread()
    test_thread.start()
except KeyboardInterrupt:
    print()
