#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from PyQt5 import QtWidgets


def main():
    if sys.platform.startswith('linux'):
        subprocess.call(f'kill -9 `pgrep -f pylatus|grep -v {os.getpid()}`', shell=True)
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('SNBL')
    app.setOrganizationDomain('snbl.eu')
    app.setApplicationName('pylatus')
    from .controller.ctrl import Controller
    controller = Controller()
    controller.start()
    sys.exit(app.exec_())
