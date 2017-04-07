#!/usr/bin/env python3
import shouty


params = {
    'user': 'source',
    'password': 'hackme',
    'mount': '/shouty',
}

with shouty.connect(**params) as connection:
    connection.send_file('test.ogg')
    connection.send_file('test.ogg')
