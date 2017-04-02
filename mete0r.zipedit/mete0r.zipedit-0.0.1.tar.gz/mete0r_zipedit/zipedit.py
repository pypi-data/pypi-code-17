# -*- coding: utf-8 -*-
#
#   mete0r.zipedit: ZipFile editing
#   Copyright (C) 2015-2017 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from io import BytesIO
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import logging


logger = logging.getLogger(__name__)


class ZipEdit(object):
    '''
    Make modified copies of a :py:class:`zipfile.ZipFile`.

    For example::

        with ZipEdit.open('foo.zip') as zipedit:
            foo = zipedit.get('foo.txt')                    # bytes
            bar = zipedit.get('bar.json', formatter=json)   # dict
            qux = zipedit.get('qux.json', loader=json.load) # dict

            # Make a modified copy
            bar['dog'] = 'bark'
            qux['cat'] = 'meow'
            with io.open('foo-modified.zip', 'wb') as fp:
                zipedit.dump(fp)

            # Make a further modified copy
            zipedit.put('foo.txt', b'FOO')
            zipedit.put('qux.json', [1, 2, 3], dump=json.dump)
            with io.open('foo-modified-further.zip', 'wb') as fp:
                zipedit.dump(fp)


    :param sourceZipFile:
        source zip file.
    :type sourceZipFile:
        :py:class:`zipfile.ZipFile`
    '''

    def __init__(self, sourceZipFile):
        self.sourceZipFile = sourceZipFile
        self.editingStreams = {
        }

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    @classmethod
    def open(cls, path):
        '''
        Open a zip file.

        :param path:
            Path to a zip file to open.
        :returns:
            :py:class:`.ZipEdit` instance.
        '''
        zipfile = ZipFile(path)
        return cls(zipfile)

    @classmethod
    def load(cls, fp):
        '''
        Load from file-like objects.

        :param fp:
            a zip file
        :type fp:
            file-like object
        :returns:
            loaded ZipEdit instance.
        :rtype: :py:class:`.ZipEdit`
        '''
        sourceZipFile = ZipFile(fp)
        return cls(sourceZipFile)

    @classmethod
    def loads(cls, sourceBytes):
        '''
        Load a zip file from :py:class:`bytes`.

        :param sourceBytes:
            a zip file content bytes.
        :type sourceBytes:
            :py:class:`bytes`
        :returns:
            loaded ZipEdit instance.
        :rtype: :py:class:`.ZipEdit`
        '''
        f = BytesIO(sourceBytes)
        return cls.load(f)

    def close(self):
        ''' Close underlying :py:class:`zipfile.ZipFile`. '''
        self.sourceZipFile.close()

    def list(self):
        '''
        List internal paths of streams in the source zip file.

        :returns: an iterator of paths
        '''
        seen = set()
        for zipinfo in self.sourceZipFile.infolist():
            filename = zipinfo.filename
            if filename not in seen:
                yield filename
            seen.add(filename)
        for path in self.editingStreams:
            if path not in seen:
                yield path
            seen.add(path)

    def get(self, path, formatter=None, load=None, dump=None):
        '''
        Get an object from an internal stream specified by given path.

        If either of `formatter` or `load` is specified, that will be used to
        deserialize the stream into the returning object. If both are
        specified, `load` takes precedence. If none of them are specified,
        entire stream data will be read and returned as :py:class:`bytes`.

        If either of `formatter` or `dump` is specified, the returning object
        will be cached to be :py:meth:`.dump`-ed to output later. So you can do
        like this::

            manifest = zipedit.get('manifest.json', formatter=json)
            manifest['foo'] = 'bar'
            zipedit.dump(fp)  # modified manifest will be serialized with json
                              # formatter.

        If both of `formatter` and `dump` are specified, `dump` takes
        precedence.

        :param path:
            a path to internal stream.
        :param formatter:
            stream formatter.
        :param load:
            object deserializer
        :param dump:
            object serializer
        :return:
            deserialized object.
        '''

        if load is None:
            if formatter is not None:
                load = formatter.load
            else:
                def load(f):
                    return f.read()
        if dump is None:
            if formatter is not None:
                dump = formatter.dump

        sourceZipFile = self.sourceZipFile
        if path not in self.editingStreams:
            try:
                zipinfo = sourceZipFile.getinfo(path)
            except KeyError:
                raise KeyError(path)
            with sourceZipFile.open(zipinfo) as f:
                obj = load(f)
            if dump is None:
                return obj
            editingStream = EditingStream(obj, dump, zipinfo)
            self.editingStreams[path] = editingStream
        return self.editingStreams[path].obj

    def put(self, path, obj, formatter=None, dump=None):
        '''
        Put an object serialized at the specified path.

        If either `formatter` or `dump` is specified, `obj` will be serialized
        with it before being written to the underlying zipfile. If both are
        specified, `dump` takes precedence.

        If none of them are specified, `obj` should be a :py:class:`bytes`.

        '''
        if dump is None:
            if formatter is not None:
                dump = formatter.dump
            else:
                def dump(obj, f):
                    f.write(obj)

        sourceZipFile = self.sourceZipFile
        try:
            # try extract zipinfo from source zipfile
            zipinfo = sourceZipFile.getinfo(path)
        except KeyError:
            # try extract zipinfo from existing editingStream
            try:
                editingStream = self.editingStreams[path]
            except KeyError:
                zipinfo = path
            else:
                zipinfo = editingStream.zipinfo_or_arcname
        editingStream = EditingStream(obj, dump, zipinfo)
        self.editingStreams[path] = editingStream

    def dump(self, fp, compression=ZIP_DEFLATED):
        '''
        Dump contents of the underlying :py:class:`zipfile.ZipFile` with
        modifications to file-like object.

        :param fp:
            output file
        :type fp:
            file-like object
        :param compression:
            compression parameter. Either of
            :py:const:`zipfile.ZIP_DEFLATED` or
            :py:const:`zipfile.ZIP_STORED`. Default to
            :py:const:`zipfile.ZIP_DEFLATED`.
        '''
        sourceZipFile = self.sourceZipFile
        with ZipFile(fp, 'w', compression=compression) as targetZipFile:
            pending = set(self.editingStreams)

            for zipinfo in sourceZipFile.infolist():
                path = zipinfo.filename
                if path in pending:
                    logger.debug('%s: modified', path)
                    streamEdit = self.editingStreams[path]
                    streamEdit.save(targetZipFile)
                    pending.remove(path)
                else:
                    logger.debug('%s: not modified', path)
                    bytes = sourceZipFile.read(path)
                    targetZipFile.writestr(zipinfo, bytes)

            for path in pending:
                logger.debug('%s: new')
                streamEdit = self.editingStreams[path]
                streamEdit.save(targetZipFile)

    def dumps(self, compression=ZIP_DEFLATED):
        '''
        Dump contents of the underlying :py:class:`zipfile.ZipFile` with
        modifications to bytes.

        :param compression:
            compression parameter. Either of
            :py:data:`zipfile.ZIP_DEFLATED` or
            :py:data:`zipfile.ZIP_STORED`. Default to
            :py:data:`zipfile.ZIP_DEFLATED`.
        :returns:
            a .zip file contents
        :rtype:
            :py:class:`bytes`
        '''
        f = BytesIO()
        self.dump(f, compression=compression)
        f.flush()
        return f.getvalue()

    def revert(self, path):
        '''
        Revert a modified stream to original state.

        :param path:
            path to a modified stream.
        '''
        if path in self.editingStreams:
            del self.editingStreams[path]

    def reset(self):
        '''
        Revert any modified streams to their original states.
        '''
        self.editingStreams.clear()


class EditingStream(object):

    def __init__(self, obj, dump, zipinfo_or_arcname):
        self.obj = obj
        self.dump = dump
        self.zipinfo_or_arcname = zipinfo_or_arcname

    def save(self, targetZipFile):
        targetStream = BytesIO()
        self.dump(self.obj, targetStream)
        bytes = targetStream.getvalue()
        targetZipFile.writestr(self.zipinfo_or_arcname, bytes)
