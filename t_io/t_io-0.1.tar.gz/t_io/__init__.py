#!/usr/bin/env python

import errno
import os

def read_file(path, split_lines = False):
    '''Reads the specified file and returns its contents as one block'''
    with open(path, 'r') as file_handle:
        if split_lines:
            contents = file_handle.readlines()
        else:
            contents = file_handle.read()
    return contents

def write_file(contents, path, makedirs = False):
    # TODO: check if contents is an array and simply branch and use writelines
    if makedirs:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as file_handle:
        file_handle.write(contents)

# Python 2 Implementation
#def write_file_x(path, contents):
#    '''Writes the specified contents to the specified file, iff the file does not exist'''
#    file_handle_flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
#    file_handle = None
#    try:
#        file_handle = os.open(path, file_handle_flags)
#        writable_file_handle = os.fdopen(file_handle, 'w')
#        writable_file_handle.write(contents)
#    finally:
#        if file_handle:
#            os.close(file_handle)

# Python 3 Implementation
def write_file_x(path, contents):
    '''Writes the specified contents to the specified file, iff the file does not exist'''
    with open(path, 'x') as file_handle:
        file_handle.write(contents)
