import glob
import json
import os
from collections.abc import MutableMapping
from os import path

not_imported = []
try:
    import numpy
    npy_properties = [numpy.ndarray, numpy.save, numpy.load]
except ImportError:
    npy_properties = []
    not_imported.append('npy')

try:
    import pandas
    # noinspection PyUnresolvedReferences
    pd_properties = [pandas.core.generic.NDFrame, pandas.to_msgpack, pandas.read_msgpack]
except ImportError:
    pd_properties = []
    not_imported.append('msg')


class File(MutableMapping):
    formats = {'npy': npy_properties, 'msg': pd_properties}

    def __init__(self, file_name: str, mode: str = 'r'):
        if mode in {'r+', 'wr', 'rw'}:
            mode = 'w+'
        is_folder = path.isdir(file_name)
        if mode in {'r', 'w+'}:
            if not is_folder:
                raise IOError('file not exist!', file_name)
        elif mode == 'w':
            if is_folder:
                empty_dir(file_name)
            else:
                os.makedirs(file_name)
        elif mode == 'w-':
            if is_folder:
                raise IOError('file already exist!', file_name)
            else:
                os.makedirs(file_name)
        else:
            raise ValueError('mode not supported!', mode)
        self.file_name = file_name
        self.mode = mode
        self.type_dict = {self.formats[ext][0]: ext for ext in self.formats}
        self.attrs = Attributes(file_name)
        for file_type in not_imported:
            del self.formats[file_type]

    def __contains__(self, item):
        full_name = path.join(self.file_name, item) + '.*'
        return bool(glob.glob(full_name))

    def __getitem__(self, item):
        full_name = path.join(self.file_name, item) + '.*'
        file_list = glob.glob(full_name)
        if len(file_list) < 1:
            raise IOError('item does not exist!', path.join(self.file_name, item))
        if len(file_list) > 1:
            raise IOError('different items in file!', path.join(self.file_name, item))
        ext = path.splitext(file_list[0])[1][1:]
        return self.formats[ext][2](file_list[0])

    def __setitem__(self, key, value):
        if self.mode == 'r':
            raise IOError('cannot write under read mode')
        if self.__contains__(key):
            self.__delitem__(key)
        for file_type, ext in self.type_dict.items():
            if isinstance(value, file_type):
                full_name = path.join(self.file_name, key) + '.' + ext
                self.formats[ext][1](full_name, value)
                break

    def __iter__(self):
        file_list = os.listdir(self.file_name)
        for file in file_list:
            base_name, ext = path.splitext(file)
            if ext[1:] in self.formats:
                yield path.split(base_name)[1]

    def __delitem__(self, key):
        if not self.__contains__(key):
            raise IOError('value not in file', key)
        else:
            full_name = path.join(self.file_name, key) + '.*'
            file_list = glob.glob(full_name)
            for file in file_list:
                os.remove(file)

    def __len__(self):
        file_list = os.listdir(self.file_name)
        return len([file for file in file_list if path.splitext(file)[1] in self.formats])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del exc_type, exc_val, exc_tb
        del self.attrs


class Attributes(MutableMapping):
    def __init__(self, file_name):
        self.file_name = path.join(file_name, 'attributes.json')
        if path.isfile(self.file_name):
            self.dict = json.load(open(self.file_name, 'r'))
        else:
            self.dict = dict()
        self.changed = False

    def __iter__(self):
        return self.dict.__iter__()

    def __len__(self):
        return self.dict.__len__()

    def __setitem__(self, key, value):
        self.changed = True
        self.dict[key] = value

    def __delitem__(self, key):
        self.changed = True
        del self.dict[key]

    def __contains__(self, key):
        return key in self.dict

    def __getitem__(self, key):
        return self.dict[key]

    def __del__(self):
        if self.changed:
            json.dump(self.dict, open(self.file_name, 'w'))


def empty_dir(top: str) -> None:
    """recursively delete all files inside folder 'top'"""
    if top == '/' or top == "\\":
        return
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            folder_path = os.path.join(root, name)
            empty_dir(folder_path)
            os.rmdir(folder_path)
