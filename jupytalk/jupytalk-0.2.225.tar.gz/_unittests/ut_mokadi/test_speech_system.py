#-*- coding: utf-8 -*-
"""
@brief      test log(time=10s)
"""

import sys
import os
import unittest
import warnings


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
from pyquickhelper.pycode import is_travis_or_appveyor, add_missing_development_version


class TestSpeechSystem(unittest.TestCase):

    def setUp(self):
        add_missing_development_version(["jyquickhelper", "ensae_teaching_cs", "pymmails"],
                                        __file__, hide=True)

    def test_speech_system(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor():
            # no keys
            return

        # bugged
        warnings.warn(
            "vocal_recognition_system does not return for a wav file.")
        return

        wav = os.path.join(os.path.abspath(
            os.path.dirname(__file__)), "data", "output.wav")
        with open(wav, "rb") as f:
            content = f.read()

        from ensae_teaching_cs.pythonnet import vocal_recognition_system
        fLOG("start recognition")
        res = vocal_recognition_system(content)
        fLOG("end recognition")
        fLOG(res)
        self.assertTrue(isinstance(res, tuple))


if __name__ == "__main__":
    unittest.main()
