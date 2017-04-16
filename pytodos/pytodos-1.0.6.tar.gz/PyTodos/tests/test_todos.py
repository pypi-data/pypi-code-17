# -*- coding: utf-8 -*-
import os
import time

from PyTodos.file_handler import read_file, write_file

directory = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = '{directory}/test_data.txt'.format(directory=directory)


def test_file_handler():
    now = int(time.time())
    write_todos = [
        {
            'id': 1,
            'task_detail': '1st_todo_detail',
            'timestamp': now
        },
        {
            'id': 2,
            'task_detail': '2nd_todo_detail',
            'timestamp': now
        }
    ]
    write_file(write_todos, file_path=TEST_FILE)
    read_todos = read_file(TEST_FILE)
    assert read_todos == write_todos
