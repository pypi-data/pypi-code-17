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


class TestGrammarMokadi(unittest.TestCase):

    def test_mokadi_grammar(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        from src.jupytalk.mokadi.mokadi_parser import get_tree_string, parse_mokadi
        from src.jupytalk.mokadi.grammars import MokadiGrammar_frParser, MokadiGrammar_frLexer, MokadiGrammar_frListener

        codes = ["MOKADI a", "MOKADI lire mail"]
        expec = [[('MOKADI', ':MOKADI:'), ('a', ':word:'), ('<EOF>', ':P:')],
                 [('MOKADI', ':MOKADI:'), ('lire', ':verb_voir:'),
                  ('mail', ':mails:'), ('<EOF>', ':P:')]
                 ]

        for i, code in enumerate(codes):
            fLOG("{0}/{1}: {2}".format(i + 1, len(codes), code))
            parser = parse_mokadi(
                code, MokadiGrammar_frParser, MokadiGrammar_frLexer)
            tree = parser.parse()
            res, simple = get_tree_string(
                MokadiGrammar_frListener, tree, parser, code)
            if "error" in res:
                raise Exception("unable to parse '{0}'".format(code))
            fLOG("SIMPLE", simple)
            fLOG("OUTPUT")

            def display(li, level=0):
                if isinstance(li, list):
                    for el in li:
                        display(el, level + 1)
                else:
                    fLOG("  " * level, li)

            display(res)

            self.assertEqual(simple, expec[i])

    def test_mokadi_interpret(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        from src.jupytalk.mokadi import interpret
        from src.jupytalk.mokadi.grammars import MokadiGrammar_frParser, MokadiGrammar_frLexer, MokadiGrammar_frListener

        codes = ["MOKADI a", "MOKADI lire mail"]
        expec = [[('MOKADI', ':MOKADI:'), ('a', ':word:'), ('<EOF>', ':P:')],
                 [('MOKADI', ':MOKADI:'), ('lire', ':verb_voir:'),
                  ('mail', ':mails:'), ('<EOF>', ':P:')]
                 ]

        for i, code in enumerate(codes):
            fLOG("{0}/{1}: {2}".format(i + 1, len(codes), code))
            simple = interpret(code, MokadiGrammar_frParser,
                               MokadiGrammar_frLexer, MokadiGrammar_frListener)
            self.assertEqual(simple, expec[i])

    def test_mokadi_interpret_exception(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        from src.jupytalk.mokadi import interpret
        from src.jupytalk.mokadi.grammars import MokadiGrammar_frParser, MokadiGrammar_frLexer, MokadiGrammar_frListener

        try:
            interpret("ROOCADI", MokadiGrammar_frParser,
                      MokadiGrammar_frLexer, MokadiGrammar_frListener)
            self.assertTrue(False)
        except SyntaxError as e:
            fLOG(e)
            self.assertTrue("missing" in str(e))


if __name__ == "__main__":
    unittest.main()
