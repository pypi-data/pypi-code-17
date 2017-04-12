# -*- coding: utf-8 -*-
import os
import json

FILE = './data.txt'


def write_file(todos, file_path=FILE):
    with open(file_path, 'w') as fp:
        for todo in todos:
            fp.write('{}\n'.format(json.dumps(todo)))


def read_file(file_path=FILE):
    todos = []
    if not os.path.exists(file_path):
        return todos
    with open(file_path, 'r') as fp:
        line = fp.readline()
        while line:
            todos.append(json.loads(line))
            line = fp.readline()
    return todos
