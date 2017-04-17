# -*- coding: utf-8 -*-

import click
import time
import datetime

from file_handler import read_file, write_file


MSG = '{color}{content}{nc}'

RED   = "\033[1;31m"
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD  = "\033[;1m"

REVERSE = "\033[;7m"
NC = '\033[0m'  # No Color

alert = lambda content, color=RED: MSG.format(color=color, content=content, nc=NC)

now = lambda : time.time()


def show(todos):
    print alert('\n=========================== TODO ================================', BLUE)
    for index, todo in enumerate([todo for todo in todos if todo['status'] == 0]):
        msg = '{}. {}'.format(index+1, todo['task_detail'].encode('utf-8'))
        print alert(msg, RED)

    print '\n'
    print alert('=========================== DONE ================================', BLUE)
    for index, todo in enumerate([todo for todo in todos if todo['status'] == 1]):
        msg = '{}. {}'.format(index+1, todo['task_detail'].encode('utf-8'))
        print alert(msg, GREEN)
    print '\n'


@click.command()
@click.argument('task_detail')
def add(task_detail):
    todos = read_file()
    todos.append(
        {
            'task_detail': task_detail,
            'status': 0,
            'timestamp': now()
        }
    )
    write_file(todos)
    print 'got it.'


@click.command()
def list():
    todos = read_file()
    if not todos:
        print 'Cool! You have no extra tasks!'
        return
    show(todos)


@click.command()
@click.argument('task_id')
def kill(task_id):
    todos = [todo for todo in read_file() if todo['status'] == 0]
    todos[int(task_id)-1]['status'] = 1
    write_file(todos)
    print 'cool!\nTasks left:'
    show(todos)
