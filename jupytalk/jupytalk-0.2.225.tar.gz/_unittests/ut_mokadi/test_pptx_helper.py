#-*- coding: utf-8 -*-
"""
@brief      test log(time=5s)
"""

import sys
import os
import unittest


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

try:
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pyquickhelper as skip_

from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import get_temp_folder
from src.jupytalk.mokadi.pptx_helper import pptx_enumerate_text, pptx_apply_transform


class TestPptxHelper(unittest.TestCase):

    def test_pptx_helper(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        import pptx
        temp = get_temp_folder(__file__, "temp_pptx_helper")
        data = os.path.join(temp, "..", "data")
        name = os.path.join(data, "simple.pptx")
        ptx = pptx.Presentation(name)
        zones = list(pptx_enumerate_text(ptx))
        exp = [(0, 0, 0, 'Exemple de présentation'),
               (0, 1, 0, 'Xavier Dupré'), (1, 0, 0, 'Première diapositive'),
               (1, 1, 0, 'Cela sera très vite terminé.'),
               (1, 1, 1, 'Ceci est une petite présentation en exemple. ')]
        self.assertEqual(zones, exp)

        def trans(islide, ishape, ip, text):
            return "*" + text + "*"

        exp2 = [(a, b, c, "*" + d + "*") for a, b, c, d in exp]
        zones = list(pptx_enumerate_text(pptx_apply_transform(ptx, trans)))
        self.assertEqual(zones, exp2)


if __name__ == "__main__":
    unittest.main()
