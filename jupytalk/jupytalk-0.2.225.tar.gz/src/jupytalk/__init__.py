# -*- coding: utf-8 -*-
"""
@file
@brief Main file.
"""

__version__ = "0.2"
__author__ = "Xavier Dupré"
__github__ = "https://github.com/sdpython/jupytalk"
__url__ = "http://www.xavierdupre.fr/app/jupytalk/helpsphinx/index.html"
__downloadUrl__ = "https://github.com/sdpython/jupytalk"
__license__ = "MIT License"
__blog__ = """
<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
    <head>
        <title>blog</title>
    </head>
    <body>
        <outline text="jupytalk"
            title="jupytalk"
            type="rss"
            xmlUrl="http://www.xavierdupre.fr/app/jupytalk/helpsphinx/_downloads/rss.xml"
            htmlUrl="http://www.xavierdupre.fr/app/jupytalk/helpsphinx/blog/main_0000.html" />
    </body>
</opml>
"""


def check(log=False):
    """
    Checks the library is working.
    It raises an exception.
    If you want to disable the logs:

    @param      log     if True, display information, otherwise
    @return             0 or exception
    """
    return True


def _setup_hook(use_print=False):
    """
    if this function is added to the module,
    the help automation and unit tests call it first before
    anything goes on as an initialization step.
    """
    # we can check many things, needed module
    # any others things before unit tests are started
    if use_print:
        print("Success: _setup_hook")


def launch_gui_mokadi(fLOG=None):
    """
    Launches tkinter with Mokadi BOT.
    """
    try:
        import pyquickhelper
    except ImportError:
        import os
        this = os.path.abspath(os.path.dirname(__file__))
        import sys
        for mod in ["pyquickhelper", "pyensae", "ensae_teaching_cs", "pymmails", "jyquickhelper"]:
            np = os.path.join(this, "..", "..", "..", mod, "src")
            sys.path.append(np)
        import pyquickhelper
    import ensae_teaching_cs

    if fLOG is None:
        import pyquickhelper.loghelper
        fLOG = pyquickhelper.loghelper.fLOG
        fLOG(OutputPrint=True)

    from .mokadi.gui_mokadi import gui_mokadi
    gui_mokadi()
