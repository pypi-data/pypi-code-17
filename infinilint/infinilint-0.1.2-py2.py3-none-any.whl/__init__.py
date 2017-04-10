#!/usr/bin/env python

import argparse
import os
import pprint
import sys
import time

import docker
import hiyapyco
import requests
from six import string_types
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def get_command_line_args():
    parser = argparse.ArgumentParser(description='Run a bunch of linters.')
    parser.add_argument('linters', metavar='linter', nargs='*',
                        default=None, help='linters to run')
    parser.add_argument('--list', required=False, action='store_true',
                        help='list available linters')
    parser.add_argument('--watch', required=False, action='store_true',
                        help='rerun linters on any change')
    return parser.parse_args()


def read_configs():
    script_path = os.path.dirname(os.path.realpath(__file__))
    base_config_file = os.path.join(script_path, 'base.yml')
    return hiyapyco.load(base_config_file, '.infinilint.yml',
                         method=hiyapyco.METHOD_MERGE,
                         failonmissingfiles=False)


def select_linters(config, selected=None):
    if selected:
        if isinstance(selected, string_types):
            selected = [selected]
        linters = {l: config['linters'][l]
                   for l in selected}
    else:
        linters = {l: config['linters'][l]
                   for l in config['linters']
                   if config['linters'][l]['enabled']}
    return linters


def list_linters(linters, selected):
    for l in linters:
        if l in selected:
            print("%s [enabled]" % l)
        else:
            print(l)


def get_image(config, key):
    # use a proxy if set
    try:
        image = "%s/%s" % (config['proxy'], config['linters'][key]['image'])
    except KeyError:
        image = config['linters'][key]['image']

    # default to latest image if no tag is specified
    if ':' not in image:
        image = "%s:latest" % image

    return image


def get_entrypoint(entry):
    # if a pattern has been given, use xargs to run the command
    try:
        if not isinstance(entry['command'], string_types):
            command = ' '.join(entry['command'])
        else:
            command = entry['command']
        entrypoint = [
            'sh', '-c',
            'find . -name "%s" -print0'
            ' | xargs -0 -r %s' % (entry['find'], command)
        ]
    except KeyError:
        entrypoint = entry['command']
    return entrypoint


def run_linters():
    args = get_command_line_args()

    config = read_configs()

    linters = select_linters(config, selected=args.linters)

    if args.list:
        list_linters(config['linters'], linters)
        exit(0)

    client = docker.DockerClient(version="auto")

    container = {}

    for linter in linters:
        image = get_image(config, linter)

        entrypoint = get_entrypoint(linters[linter])

        # Mount current folder at /code read-only
        code_mount = {os.getcwd(): {'bind': '/code', 'mode': 'ro'}}

        print("Starting %s (%s)" % (linter, image))
        container[linter] = client.containers.run(
            image,
            entrypoint=entrypoint,
            volumes=code_mount,
            working_dir='/code',
            detach=True
        )

    final_exit_code = 0
    start = time.time()
    while container:
        for linter in list(container):
            try:
                exit_code = container[linter].wait(timeout=5)
            except requests.exceptions.ReadTimeout:
                if int(time.time() - start) < config['timeout']:
                    continue
                else:
                    raise
            print("Output of %s" % linter)
            print(container[linter].logs().decode("UTF-8"))
            container[linter].remove()
            del container[linter]
            print("%s exit code: %i\n" % (linter, exit_code))
            if exit_code:
                final_exit_code += 1

    print("Final exit code: %i" % final_exit_code)
    return final_exit_code


def run_watcher():
        class LinterHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                pprint.pprint(event)
                if not event.is_directory:
                    run_linters()
        observer = Observer()
        observer.schedule(LinterHandler(), os.getcwd(), recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


def main():
    if '--watch' in sys.argv:
        run_watcher()
    else:
        exit(run_linters())


if __name__ == '__main__':
    main()
