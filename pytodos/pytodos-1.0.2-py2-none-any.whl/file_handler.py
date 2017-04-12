# -*- coding: utf-8 -*-
import os
import json

FILE = './data.txt'


def write_file(todos):
    with open(FILE, 'w') as fp:
        for todo in todos:
            fp.write('{}\n'.format(json.dumps(todo)))


def read_file():
    todos = []
    if not os.path.exists(FILE):
        return todos
    with open(FILE, 'r+') as fp:
        line = fp.readline()
        while line:
            todos.append(json.loads(line))
            line = fp.readline()
    return todos
