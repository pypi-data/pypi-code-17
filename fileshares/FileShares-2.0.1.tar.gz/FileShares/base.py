import os
import sys
from time import sleep
from hashlib import md5
import logging
from termcolor import cprint, colored
from .config import ENV, PATH_DEL, loger

class FileNotFoundErr(Exception):
    pass


class IO:
    items = set()
    i_map = dict()
    i_hash_map = dict()
    i_hash_name = dict()

    def __call__(self, file):

        if hasattr(file, 'hash'):
            ha = file.hash
            if ha in IO.i_hash_map:
                old_f = IO.i_hash_map.pop(ha)
                del old_f

            IO.i_hash_map[ha] = file
            IO.items.add(file.path)
            IO.i_map[file.path] = file
            IO.i_hash_name[ha] = file.path
        else:
            IO.items.add(file.path)
            IO.i_map[file.path] = file

    def __getitem__(self, file):
        if file in IO.items:
            return IO.i_map[file]

        if file in IO.i_hash_name:
            return IO.i_hash_name[file]

    def exists(self, f):
        return f in IO.items

    def d(self, f):
        if f in IO.items:
            # print(f)
            IO.items.remove(f)
            if f in IO.i_map:
                IO.i_map.pop(f)
            if hasattr(f, 'hash'):
                del IO.i_hash_map[f.hash]
                del IO.i_hash_name[f.hash]

            


class File:

    def __init__(self, file, io, name=None):
        if hasattr(file, 'readable'):
            self.content = file.read()
            self.length = len(self.content)
            if not name:
                raise Exception("no file's name!!")
            self.name = name

        elif isinstance(file, bytes):
            self.content = file
            if not name:
                raise Exception("no file's name!!")
            self.name = name
            self.length = len(self.content)

        elif isinstance(file, str):
            if os.path.exists(file) and os.path.isfile(file):
                self.path = os.path.abspath(file)
                self.name = os.path.basename(self.path)
                self.dir = os.path.dirname(self.path)
                with open(file, 'rb') as fp:
                    self.length = fp.seek(0, 2)
            else:
                raise FileNotFoundErr("file not found: " + self.path)
        else:
            raise TypeError("not file .")
        # add to register
        io(self)
        self.io = io

    @property
    def hash(self):
        if hasattr(self, 'md5'):
            return self.md5

        try:
            with open(self.path, 'rb') as fp:
                self.md5 = md5(fp.read()).hexdigest()
            return self.md5
        except Exception as e:
            raise e
            

    def __del__(self):
        if hasattr(self, 'fp'):
            self.fp.close()

        self.io.d(self.path)

    def __repr__(self):
        return self.name


class Dir(IO):

    def __init__(self, dir_p, io):
        if os.path.exists(dir_p) and os.path.isdir(dir_p):
            self.path = os.path.abspath(dir_p)
            self.files = []
            self.dirs = []
            self.name = os.path.basename(self.path)

            for f in os.listdir(self.path):
                # loger.debug(f)
                if f.startswith("."):
                    continue
                f_p = os.path.join(self.path, f)

                if os.path.isfile(f_p):
                    # if not io.exists(f_p):
                    self.files.append(File(f_p, io))
                    # else :
                        # self.files.append(io[f_p])

                elif os.path.isdir(f_p):
                    self.dirs.append(Dir(f_p, io))

        else:
            raise FileNotFoundErr("not such dir: " + self.path)

        # loger.debug("dir ok")
        io(self)
        self.io = io

    def tree(self, count=0, prefix='  |'):
        for f in self.dirs + self.files:

            if hasattr(f, 'dirs'):
                cprint(' ' + prefix.replace("|", "-")
                       * count + f.name + " :", 'red')
                f.tree(count=count+1, prefix=prefix)
            else:
                print('|' + prefix * count + f.name)

    def all(self):
        for f in self.dirs + self.files:
            if hasattr(f, 'dirs'):
                yield from f.all()
            else:
                # loger.debug(colored(f.hash,"yellow"))
                yield f.hash

    def __repr__(self):
        return self.path

    def __del__(self):
        self.io.d(self.path)


class Encry:

    @staticmethod
    def stream(data, key):
        k_l = len(key)
        for i, v in enumerate(data):
            k_serial = key[i % k_l] ^ ((i << ((2 * i - 1) % 256)) % 256)
            yield v ^ k_serial
