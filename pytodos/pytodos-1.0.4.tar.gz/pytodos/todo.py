# -*- coding: utf-8 -*-

import click

from file_handler import read_file, write_file


def show(todos):
    for index, todo in enumerate([todo for todo in todos if todo['status'] == 0]):
        print '{}. {}'.format(index+1, todo['task_detail'].encode('utf-8'))


@click.command()
@click.argument('task_detail')
def add(task_detail):
    todos = read_file()
    todos.append(
        {
            'task_detail': task_detail,
            'status': 0
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
