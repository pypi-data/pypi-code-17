#-*- coding: utf-8 -*-
"""
@brief      test log(time=10s)
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
from pyquickhelper.pycode import is_travis_or_appveyor
from src.jupytalk.mokadi import take_picture


class TestPicture(unittest.TestCase):

    def test_take_picture(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor():
            # no keys
            return

        temp = get_temp_folder(__file__, "temp_take_picture")

        try:
            for module in ["pygame", "cv2"]:
                fLOG(module)
                img = os.path.join(temp, "im_{0}.png".format(module))
                take_picture(img, module=module)
        except Exception as e:
            if os.environ["USERNAME"] == "ensaestudent" or \
               os.environ["USERNAME"] == "vsxavierdupre" or \
               os.environ["USERNAME"] == "vsxavierdupre" or \
               "DOUZE2016" in os.environ.get("COMPUTERNAME", "") or \
               os.environ["USERNAME"] == "appveyor" or \
               "paris" in os.environ.get("COMPUTERNAME", "").lower() or \
               os.environ["USERNAME"].endswith("$"):
                return


if __name__ == "__main__":
    unittest.main()
