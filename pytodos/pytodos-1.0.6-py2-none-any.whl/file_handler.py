# -*- coding: utf-8 -*-
import os
import json

directory = os.path.dirname(os.path.abspath(__file__))
FILE = '{directory}/data.txt'.format(directory=directory)


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
            try:
                todos.append(json.loads(line))
                line = fp.readline()
            except ValueError:
                write_file(todos, file_path)
                return todos
    return todos
