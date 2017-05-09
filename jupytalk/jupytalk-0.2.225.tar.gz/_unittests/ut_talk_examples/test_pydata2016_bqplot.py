"""
@brief      test log(time=2s)
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
from pyquickhelper.filehelper import get_url_content_timeout
from pyquickhelper.pycode import get_temp_folder
from bqplot import topo_load


class TestPyData2016bqplot(unittest.TestCase):

    def test_bqplot_topo_load(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        temp = get_temp_folder(__file__, "temp_bqplot_topo_load")
        f = 'WorldMap.json'
        full = os.path.join(temp, f)
        url = "https://raw.githubusercontent.com/bloomberg/bqplot/master/bqplot/map_data/"
        get_url_content_timeout(url + f, output=full)
        r = topo_load(full)
        assert r
        if not isinstance(r, dict):
            raise TypeError(type(r))


if __name__ == "__main__":
    unittest.main()
