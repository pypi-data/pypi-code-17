"""
@brief      test log(time=35s)
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
from pyquickhelper.pycode import get_temp_folder, fix_tkinter_issues_virtualenv
from src.jupytalk.talk_examples.pydata2016 import example_pydy


class TestPyData2016pydy(unittest.TestCase):

    def test_example_pydy(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        temp = get_temp_folder(__file__, "temp_example_pydy")
        fix_tkinter_issues_virtualenv()
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 8))
        example_pydy(ax=ax)
        assert ax is not None
        img = os.path.join(temp, "img.png")
        fig.savefig(img)
        assert os.path.exists(img)
        if __name__ == "__main__":
            fig.show()
        plt.close('all')
        fLOG("end")


if __name__ == "__main__":
    unittest.main()
