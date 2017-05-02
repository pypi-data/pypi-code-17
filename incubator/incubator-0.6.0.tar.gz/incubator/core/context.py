"""
Class for manipulating with build context.
"""
import os
import tarfile

import six

from .fileutils import (get_filtered_files, is_top_file, normalise_patterns,
                        remove_top_parent)


class BuildContext:
    def __init__(self, context, limit):
        self._context = context
        self._struct = None
        self._context.seek(0)
        self.limit = limit

    @property
    def structure(self):
        if not self._struct:
            self._context.seek(0)
            with tarfile.open(mode="r", fileobj=self._context) as tar_file:
                self._struct = tar_file.getnames()
            self._context.seek(0)
        return self._struct

    def get_file(self, name):
        try:
            with tarfile.open(mode="r", fileobj=self._context) as tar:
                f = tar.extractfile(tar.getmember(name))
            if not f:
                return None
            file = six.BytesIO()
            file.writelines(f.readlines())
            file.seek(0)
            return file
        except:
            return None
        finally:
            self._context.seek(0)

    def get_archive(self, patterns, single_file=None):

        normpatterns = normalise_patterns(patterns)

        with tarfile.open(mode="r", fileobj=self._context) as tar_file:

            put_all = os.curdir in normpatterns

            files_to_put = self.structure if put_all else get_filtered_files(self.structure, normpatterns, tar_file)

            if len(files_to_put) == 0:
                return None
            elif single_file and len(files_to_put) > 1:
                raise ValueError("expecting single file in patterns: {}".format(normpatterns))

            tar_in_memory = six.BytesIO()
            with tarfile.open(mode="w", fileobj=tar_in_memory) as filtered_tar:
                for file in files_to_put:
                    file_info = tar_file.getmember(file)
                    file_object = tar_file.extractfile(file_info)
                    if single_file:
                        file_info.name = single_file
                    elif not put_all and is_top_file(file):
                        file_info.name = remove_top_parent(file)
                    filtered_tar.addfile(tarinfo=file_info,
                                         fileobj=file_object)

            tar_in_memory.seek(0)
            self._context.seek(0)
            return tar_in_memory
