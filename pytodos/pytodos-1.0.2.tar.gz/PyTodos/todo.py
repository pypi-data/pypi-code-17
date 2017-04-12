# -*- coding: utf-8 -*-

import click
import pprint

from file_handler import read_file, write_file

pp = pprint.PrettyPrinter(indent=4)


def show(todos):
    for index, todo in enumerate([todo for todo in todos if todo['status'] == 0]):
        print '{}. {}'.format(index+1, todo['task_detail'])


@click.group(context_settings={'help_option_names': ('-h', '--help')})
def cli():
    pass


@cli.command()
@click.option('--task_detail', default='Hello', help='Details of your task')
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


@cli.command()
def l():
    todos = read_file()
    show(todos)


@cli.command()
@click.option('--task_id', default=1, help='finished this task already')
def kill(task_id):
    todos = [todo for todo in read_file() if todo['status'] == 0]
    todos[task_id-1]['status'] = 1
    write_file(todos)
    print 'cool!'
