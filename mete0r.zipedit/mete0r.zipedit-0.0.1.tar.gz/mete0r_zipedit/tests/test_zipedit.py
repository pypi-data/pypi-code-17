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
from unittest import TestCase
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
import logging
import io
import shutil

from ..json_formatter import JSON


logger = logging.getLogger(__name__)


class ZipEditTest(TestCase):

    @property
    def logger(self):
        name = self.id()
        return logging.getLogger(name)

    def makeSourceZip(self, sourceStream=None):
        sourceStream = sourceStream or BytesIO()
        with ZipFile(sourceStream, 'w', ZIP_DEFLATED) as sourceZip:
            sourceZip.writestr('foo.txt', 'Foo')
            sourceZip.writestr('bar.txt', 'Bar')
        sourceStream.seek(0)
        return ZipFile(sourceStream)

    def makeSourceZipWithJsonStreams(self, sourceStream=None):
        sourceStream = sourceStream or BytesIO()
        with ZipFile(sourceStream, 'w', ZIP_DEFLATED) as sourceZip:
            sourceZip.writestr('foo.json', '"Foo"')
            sourceZip.writestr('bar.json', '{"bar": "Bar"}')
        sourceStream.seek(0)
        return ZipFile(sourceStream)

    def makeSourceZipWithUTF8Names(self, sourceStream=None):
        sourceStream = sourceStream or BytesIO()
        with ZipFile(sourceStream, 'w', ZIP_DEFLATED) as sourceZip:
            sourceZip.writestr('갑.txt', '甲'.encode('utf-8'))
            sourceZip.writestr('을.txt', '乙'.encode('utf-8'))
            sourceZip.writestr('병.txt', '丙'.encode('utf-8'))
        sourceStream.seek(0)
        return ZipFile(sourceStream)

    def test_open(self):
        source = BytesIO()
        self.makeSourceZip(source)
        source.seek(0)
        with io.open('foo.zip', 'wb') as fp:
            shutil.copyfileobj(source, fp)
        from ..zipedit import ZipEdit
        with ZipEdit.open('foo.zip') as zipedit:
            zipedit.close()

    def test_load(self):
        from ..zipedit import ZipEdit
        sourceStream = BytesIO()
        self.makeSourceZip(sourceStream)
        sourceStream.seek(0)

        zipedit = ZipEdit.load(sourceStream)
        self.assertTrue(isinstance(zipedit.sourceZipFile, ZipFile))

    def test_loads(self):
        from ..zipedit import ZipEdit
        sourceStream = BytesIO()
        self.makeSourceZip(sourceStream)
        sourceStream.seek(0)
        sourceBytes = sourceStream.getvalue()

        zipedit = ZipEdit.loads(sourceBytes)
        self.assertTrue(isinstance(zipedit.sourceZipFile, ZipFile))

    def test_close(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZip()
        zipedit = ZipEdit(source)
        zipedit.close()

    def test_as_context(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZip()
        with ZipEdit(source) as zipedit:
            self.assertEquals(b'Foo', zipedit.get('foo.txt'))

    def test_get_raises_keyerror_on_missing(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZip()
        with ZipEdit(source) as zipedit:
            with self.assertRaises(KeyError):
                zipedit.get('qux.txt')

    def test_get_with_unicode_path(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZipWithUTF8Names()
        with ZipEdit(source) as zipedit:
            zipedit.get('갑.txt')

    def test_basic_editing_session(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZip()

        zipedit = ZipEdit(source)

        foo = zipedit.get('foo.txt')
        self.assertEquals(b'Foo', foo)
        self.assertEquals({}, zipedit.editingStreams)

        bar = zipedit.get('bar.txt')
        self.assertEquals(b'Bar', bar)
        self.assertEquals({}, zipedit.editingStreams)
        zipedit.put('bar.txt', b'Bar modified')

        with self.assertRaises(KeyError):
            zipedit.get('qux.txt')

        # put new qux.txt
        zipedit.put('qux.txt', b'Qux')

        targetBytes = zipedit.dumps()
        target = ZipFile(BytesIO(targetBytes))
        dump_zipinfo_list(target, self.logger)
        self.assertEquals(
            b'Foo',
            target.read('foo.txt'),
        )
        self.assertEquals(
            b'Bar modified',
            target.read('bar.txt'),
        )
        self.assertEquals(
            b'Qux',
            target.read('qux.txt'),
        )

        # modify qux
        zipedit.put('qux.txt', 'Qux modified', dump=JSON.dump)

        targetBytes = zipedit.dumps()
        target = ZipFile(BytesIO(targetBytes))
        dump_zipinfo_list(target, self.logger)
        self.assertEquals(
            b'Foo',
            target.read('foo.txt'),
        )
        self.assertEquals(
            b'Bar modified',
            target.read('bar.txt'),
        )
        self.assertEquals(
            b'"Qux modified"',
            target.read('qux.txt'),
        )

    def test_with_formatter(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZipWithJsonStreams()

        zipedit = ZipEdit(source)

        foo = zipedit.get('foo.json', formatter=JSON)
        self.assertEquals('Foo', foo)
        zipedit.put('foo.json', 'Foo modified', formatter=JSON)

        # modify bar.json
        bar = zipedit.get('bar.json', formatter=JSON)
        bar['bar'] = 'Bar modified'

        # put new qux.json
        qux = ['Qux']
        zipedit.put('qux.json', qux, formatter=JSON)

        targetBytes = zipedit.dumps()
        target = ZipFile(BytesIO(targetBytes))
        dump_zipinfo_list(target, self.logger)
        self.assertEquals(
            b'"Foo modified"',
            target.read('foo.json'),
        )
        self.assertEquals(
            {'bar': 'Bar modified'},
            JSON.loads(target.read('bar.json')),
        )
        self.assertEquals(
            ['Qux'],
            JSON.loads(target.read('qux.json')),
        )

        # further modify qux
        qux[0] = 'Qux modified'

        targetBytes = zipedit.dumps()
        target = ZipFile(BytesIO(targetBytes))
        dump_zipinfo_list(target, self.logger)
        self.assertEquals(
            b'"Foo modified"',
            target.read('foo.json'),
        )
        self.assertEquals(
            {'bar': 'Bar modified'},
            JSON.loads(target.read('bar.json')),
        )
        self.assertEquals(
            ['Qux modified'],
            JSON.loads(target.read('qux.json')),
        )

    def test_with_formatter_and_stream_dumper(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZipWithJsonStreams()

        zipedit = ZipEdit(source)

        def pretty_dump(o, f):
            return JSON.dump(o, f, indent=2, sort_keys=True)

        foo = zipedit.get('foo.json', formatter=JSON, dump=pretty_dump)
        self.assertEquals('Foo', foo)
        zipedit.put('foo.json', 'Foo modified',
                    formatter=JSON,
                    dump=pretty_dump)

        # modify bar.json
        bar = zipedit.get('bar.json', formatter=JSON, dump=pretty_dump)
        bar['bar'] = 'Bar modified'

        # put new qux.json
        qux = ['Qux']
        zipedit.put('qux.json', qux, formatter=JSON, dump=pretty_dump)

        targetBytes = zipedit.dumps()
        target = ZipFile(BytesIO(targetBytes))
        dump_zipinfo_list(target, self.logger)
        self.assertEquals(
            b'"Foo modified"',
            target.read('foo.json'),
        )
        self.assertEquals(
            b'{\n  "bar": "Bar modified"\n}',
            target.read('bar.json'),
        )
        self.assertEquals(
            b'[\n  "Qux"\n]',
            target.read('qux.json'),
        )

        # further modify qux
        qux[0] = 'Qux modified'

        # and dump it
        targetBytes = zipedit.dumps()
        target = ZipFile(BytesIO(targetBytes))
        dump_zipinfo_list(target, self.logger)
        self.assertEquals(
            b'"Foo modified"',
            target.read('foo.json'),
        )
        self.assertEquals(
            b'{\n  "bar": "Bar modified"\n}',
            target.read('bar.json'),
        )
        self.assertEquals(
            b'[\n  "Qux modified"\n]',
            target.read('qux.json'),
        )

    def test_with_stream_loader_and_dumper(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZipWithJsonStreams()

        zipedit = ZipEdit(source)

        foo = zipedit.get('foo.json', load=JSON.load, dump=JSON.dump)
        self.assertEquals('Foo', foo)
        zipedit.put('foo.json', 'Foo modified', dump=JSON.dump)

        # modify bar.json
        bar = zipedit.get('bar.json', load=JSON.load, dump=JSON.dump)
        bar['bar'] = 'Bar modified'

        # put new qux.json
        qux = ['Qux']
        zipedit.put('qux.json', qux, dump=JSON.dump)

        targetBytes = zipedit.dumps()
        target = ZipFile(BytesIO(targetBytes))
        dump_zipinfo_list(target, self.logger)
        self.assertEquals(
            b'"Foo modified"',
            target.read('foo.json'),
        )
        self.assertEquals(
            {'bar': 'Bar modified'},
            JSON.loads(target.read('bar.json')),
        )
        self.assertEquals(
            ['Qux'],
            JSON.loads(target.read('qux.json')),
        )

        # further modify qux
        qux[0] = 'Qux modified'

        targetBytes = zipedit.dumps()
        target = ZipFile(BytesIO(targetBytes))
        dump_zipinfo_list(target, self.logger)
        self.assertEquals(
            b'"Foo modified"',
            target.read('foo.json'),
        )
        self.assertEquals(
            {'bar': 'Bar modified'},
            JSON.loads(target.read('bar.json')),
        )
        self.assertEquals(
            ['Qux modified'],
            JSON.loads(target.read('qux.json')),
        )

    def test_revert(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZip()

        zipedit = ZipEdit(source)

        foo = zipedit.get('foo.txt')
        self.assertEquals(b'Foo', foo)
        self.assertEquals({}, zipedit.editingStreams)

        bar = zipedit.get('bar.txt')
        self.assertEquals(b'Bar', bar)
        self.assertEquals({}, zipedit.editingStreams)
        zipedit.put('bar.txt', b'Bar modified')
        self.assertTrue('bar.txt' in zipedit.editingStreams)

        zipedit.revert('bar.txt')
        self.assertEquals({}, zipedit.editingStreams)

    def test_reset(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZip()

        zipedit = ZipEdit(source)

        zipedit.put('foo.txt', b'Foo modified')
        zipedit.put('bar.txt', b'Bar modified')
        self.assertTrue('foo.txt' in zipedit.editingStreams)
        self.assertTrue('bar.txt' in zipedit.editingStreams)

        zipedit.reset()
        self.assertEquals({}, zipedit.editingStreams)

    def test_list(self):
        from ..zipedit import ZipEdit
        source = self.makeSourceZip()

        zipedit = ZipEdit(source)
        filenames = sorted(zipedit.list())
        self.assertEquals(sorted([
            'foo.txt',
            'bar.txt',
        ]), filenames)

        zipedit.put('bar.txt', b'Bar modified')
        zipedit.put('qux.txt', b'Qux')
        filenames = sorted(zipedit.list())
        self.assertEquals(sorted([
            'foo.txt',
            'bar.txt',
            'qux.txt',
        ]), filenames)


def dump_zipinfo_list(zipfile, logger):
    for zipinfo in zipfile.infolist():
        logger.info(
            '[%1s][%2d/%2d][%08o] %s',
            zipinfo.compress_type,
            zipinfo.compress_size,
            zipinfo.file_size,
            zipinfo.external_attr,
            zipinfo.filename,
        )
