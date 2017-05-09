#-*- coding: utf-8 -*-
"""
@brief      test log(time=40s)
"""

import sys
import os
import unittest
import wikipedia


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

try:
    import pymmails as skip__
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pymmails",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import pymmails as skip__


from pyquickhelper.loghelper import fLOG
from src.jupytalk.mokadi import definition_wikipedia, suggestions_wikipedia, synonyms_wiktionary


class TestWikipedia(unittest.TestCase):

    def test_wikipedia_summary(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        res = definition_wikipedia("microsoft")
        self.assertTrue("Gates" in res)
        res = definition_wikipedia("intelligence")
        self.assertTrue("L'intelligence" in res)
        try:
            definition_wikipedia("intelligence iafhaepzfuichaefhanozfnhaoi")
            self.assertTrue(False)
        except wikipedia.exceptions.PageError:
            pass

    def test_wikipedia_definition(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        res = definition_wikipedia("intelligence", summary=False)
        enc = res.encode("utf-8")
        dec = enc.decode("cp1252", errors="ignore")
        self.assertTrue(dec)

    def test_suggestion(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        res = suggestions_wikipedia("pari")
        self.assertTrue(isinstance(res, list))
        self.assertTrue(len(res) > 0)

    def test_dictionary_synonym(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        res = synonyms_wiktionary("ville")
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 1)

    def test_dictionary_synonym_travail(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        res = synonyms_wiktionary("travail")
        self.assertTrue(isinstance(res, list))
        self.assertEqual(len(res), 10)
        self.assertEqual(res, ['boulot', 'chagrin', 'emploi', 'gagne-pain',
                               'job', 'métier', 'profession', 'job', 'taf', 'turbin'])


if __name__ == "__main__":
    unittest.main()
