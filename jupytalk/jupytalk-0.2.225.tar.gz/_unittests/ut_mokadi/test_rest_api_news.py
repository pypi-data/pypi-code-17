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
from pyquickhelper.pycode import is_travis_or_appveyor
from src.jupytalk.mokadi.cognitive_services_helper import call_api_news


class TestRestApiNews(unittest.TestCase):

    def test_api_news(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor():
            # no keys
            return

        import keyring
        subkey = keyring.get_password(
            "cogser", os.environ["COMPUTERNAME"] + "news")
        res = call_api_news(subkey, "tennis")
        self.assertTrue(isinstance(res, dict))
        self.assertTrue(len(res) > 0)
        for k, v in res.items():
            fLOG("k={0}".format(k))
            if isinstance(v, list):
                for _ in v:
                    fLOG(_)
                    self.assertTrue(isinstance(_, dict))
                    self.assertTrue("name" in _)


if __name__ == "__main__":
    unittest.main()
