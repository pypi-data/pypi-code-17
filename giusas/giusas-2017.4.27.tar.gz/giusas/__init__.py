#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from giusas.controller import Controller


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setOrganizationName('Dubble')
    app.setOrganizationDomain('esrf.eu')
    app.setApplicationName('GiuSAS')
    ctrl = Controller()
    ctrl.start()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
