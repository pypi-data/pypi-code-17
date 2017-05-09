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
from pyquickhelper.pycode import is_travis_or_appveyor, get_temp_folder
from src.jupytalk.mokadi import record_speech, play_speech


class TestRestApiSpeech(unittest.TestCase):

    def test_record(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor():
            # no keys
            return

        fLOG("record")
        temp = get_temp_folder(__file__, "temp_record")
        output = os.path.join(temp, "output.wav")
        try:
            record = record_speech(3, fLOG=fLOG, WAVE_OUTPUT_FILENAME=output)
        except Exception as e:
            if os.environ["USERNAME"] == "ensaestudent" or \
               os.environ["USERNAME"] == "vsxavierdupre" or \
               os.environ["USERNAME"] == "vsxavierdupre" or \
               "DOUZE2016" in os.environ["COMPUTERNAME"] or \
               os.environ["USERNAME"] == "appveyor" or \
               "paris" in os.environ["COMPUTERNAME"].lower() or \
               os.environ["USERNAME"].endswith("$"):
                return
        fLOG("play", len(record))
        play_speech(record)
        fLOG("end")


if __name__ == "__main__":
    unittest.main()
