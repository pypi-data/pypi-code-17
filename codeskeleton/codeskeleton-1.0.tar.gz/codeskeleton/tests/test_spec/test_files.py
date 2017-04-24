import unittest
from collections import OrderedDict

from codeskeleton import spec


class TestFiles(unittest.TestCase):
    def test_deserialize(self):
        files = spec.Files()
        files.deserialize(data=OrderedDict([
            ('a', {'content': 'test1'}),
            ('b', {'content': 'test2'}),
        ]))
        self.assertEqual(len(files._files), 2)
        self.assertEqual(files._files[0].content, 'test1')
        self.assertEqual(files._files[1].content, 'test2')

    def test_iter(self):
        files = spec.Files()
        file1 = spec.File(path='a')
        file2 = spec.File(path='a')
        files._files = [file1, file2]
        self.assertEqual(list(files), [file1, file2])

    def test_len(self):
        files = spec.Files()
        files._files = [spec.File(path='a'), spec.File(path='b')]
        self.assertEqual(len(files), 2)
