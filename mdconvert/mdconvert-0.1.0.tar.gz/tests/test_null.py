from os.path import abspath, dirname
from pathlib import Path
import unittest

from mdconvert.mdconvertapp import MDConvertApp

HERE = Path(abspath(dirname(__file__)))


class NullTestCase(unittest.TestCase):
    def test_null_output(self):
        self.app = MDConvertApp(files=HERE / "fixtures" / "no-metadata.ipynb")
        self.app.start()
