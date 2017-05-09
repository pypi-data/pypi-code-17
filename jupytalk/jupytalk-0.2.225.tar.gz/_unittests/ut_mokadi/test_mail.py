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
from pyquickhelper.pycode import is_travis_or_appveyor
from src.jupytalk.mokadi import enumerate_last_mails


class TestMail(unittest.TestCase):

    def test_mail(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor():
            # no keys
            return

        import keyring
        user = keyring.get_password(
            "gmail", os.environ["COMPUTERNAME"] + "user")
        pwd = keyring.get_password("gmail", os.environ["COMPUTERNAME"] + "pwd")
        server = "imap.gmail.com"
        try:
            mails = enumerate_last_mails(user, pwd, server, fLOG=fLOG)

            i = 0
            for mail in mails:
                fLOG(mail.get_name(), "**", mail.get_nb_attachements(),
                     "**", mail.get_date_str())
                fLOG(mail.get_field("subject").split("\n")[0])
                i += 1

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
