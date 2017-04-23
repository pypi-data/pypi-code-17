# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'calculator.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
try:
    from src.mathlib import Solver
    from src.gui_lin import *
except ImportError:
    from mathlib import Solver
    from gui_lin import *


class Ui_Form(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.clearExpression = False
        self.mathSolver = Solver()
        self.linearSystem = Ui_Form_LinearSystem(self)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("self")
        self.setWindowModality(QtCore.Qt.NonModal)
        self.setEnabled(True)
        self.resize(903, 583)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(False)
        self.setFont(font)
        self.gridLayout_6 = QtWidgets.QGridLayout(self)
        self.gridLayout_6.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(25)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSpacing(10)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.pushButton_22 = QtWidgets.QPushButton(self)
        self.pushButton_22.clicked.connect(
            lambda: self.addTextToExpression("4")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_22.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_22.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_22.setFont(font)
        self.pushButton_22.setObjectName("pushButton_22")
        self.gridLayout_3.addWidget(self.pushButton_22, 1, 0, 1, 1)

        self.pushButton_14 = QtWidgets.QPushButton(self)
        self.pushButton_14.clicked.connect(
            lambda: self.addTextToExpression("8")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_14.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_14.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_14.setFont(font)
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout_3.addWidget(self.pushButton_14, 0, 1, 1, 1)

        self.pushButton_15 = QtWidgets.QPushButton(self)
        self.pushButton_15.clicked.connect(
            lambda: self.addTextToExpression("9")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_15.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_15.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_15.setFont(font)
        self.pushButton_15.setObjectName("pushButton_15")
        self.gridLayout_3.addWidget(self.pushButton_15, 0, 2, 1, 1)

        self.pushButton_17 = QtWidgets.QPushButton(self)
        self.pushButton_17.clicked.connect(
            lambda: self.addTextToExpression("5")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_17.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_17.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_17.setFont(font)
        self.pushButton_17.setObjectName("pushButton_17")
        self.gridLayout_3.addWidget(self.pushButton_17, 1, 1, 1, 1)

        self.pushButton_13 = QtWidgets.QPushButton(self)
        self.pushButton_13.clicked.connect(
            lambda: self.addTextToExpression("7")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_13.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_13.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_13.setFont(font)
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout_3.addWidget(self.pushButton_13, 0, 0, 1, 1)

        self.pushButton_25 = QtWidgets.QPushButton(self)
        self.pushButton_25.clicked.connect(
            lambda: self.addTextToExpression("1")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_25.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_25.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_25.setFont(font)
        self.pushButton_25.setObjectName("pushButton_25")
        self.gridLayout_3.addWidget(self.pushButton_25, 2, 0, 1, 1)

        self.pushButton_23 = QtWidgets.QPushButton(self)
        self.pushButton_23.clicked.connect(
            lambda: self.addTextToExpression("2")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_23.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_23.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_23.setFont(font)
        self.pushButton_23.setObjectName("pushButton_23")
        self.gridLayout_3.addWidget(self.pushButton_23, 2, 1, 1, 1)

        self.pushButton_29 = QtWidgets.QPushButton(self)
        self.pushButton_29.clicked.connect(
            lambda: self.addTextToExpression(".")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_29.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_29.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_29.setFont(font)
        self.pushButton_29.setObjectName("pushButton_29")
        self.gridLayout_3.addWidget(self.pushButton_29, 3, 2, 1, 1)

        self.pushButton_28 = QtWidgets.QPushButton(self)
        self.pushButton_28.clicked.connect(
            lambda: self.addTextToExpression("3")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_28.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_28.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_28.setFont(font)
        self.pushButton_28.setObjectName("pushButton_28")
        self.gridLayout_3.addWidget(self.pushButton_28, 2, 2, 1, 1)

        self.pushButton_27 = QtWidgets.QPushButton(self)
        self.pushButton_27.clicked.connect(
            lambda: self.addTextToExpression("6")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_27.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_27.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_27.setFont(font)
        self.pushButton_27.setObjectName("pushButton_27")
        self.gridLayout_3.addWidget(self.pushButton_27, 1, 2, 1, 1)

        self.pushButton_26 = QtWidgets.QPushButton(self)
        self.pushButton_26.clicked.connect(
            lambda: self.addTextToExpression("0")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_26.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_26.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_26.setFont(font)
        self.pushButton_26.setObjectName("pushButton_26")
        self.gridLayout_3.addWidget(self.pushButton_26, 3, 0, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_3, 1, 2, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setSpacing(10)
        self.gridLayout_4.setObjectName("gridLayout_4")

        self.pushButton_20 = QtWidgets.QPushButton(self)
        self.pushButton_20.clicked.connect(
            lambda: self.addTextToExpression("*")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_20.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_20.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_20.setFont(font)
        self.pushButton_20.setObjectName("pushButton_20")
        self.gridLayout_4.addWidget(self.pushButton_20, 2, 0, 1, 1)

        self.pushButton_18 = QtWidgets.QPushButton(self)
        self.pushButton_18.clicked.connect(
            lambda: self.addTextToExpression("+")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_18.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_18.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_18.setFont(font)
        self.pushButton_18.setObjectName("pushButton_18")
        self.gridLayout_4.addWidget(self.pushButton_18, 0, 0, 1, 1)

        self.pushButton_19 = QtWidgets.QPushButton(self)
        self.pushButton_19.clicked.connect(
            lambda: self.addTextToExpression("-")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_19.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_19.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_19.setFont(font)
        self.pushButton_19.setObjectName("pushButton_19")
        self.gridLayout_4.addWidget(self.pushButton_19, 1, 0, 1, 1)

        self.pushButton_21 = QtWidgets.QPushButton(self)
        self.pushButton_21.clicked.connect(
            lambda: self.addTextToExpression("/")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_21.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_21.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_21.setFont(font)
        self.pushButton_21.setObjectName("pushButton_21")
        self.gridLayout_4.addWidget(self.pushButton_21, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_4, 1, 3, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.clicked.connect(
            lambda: self.addTextToExpression(")")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_3.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 0, 4, 1, 1)

        self.pushButton_6 = QtWidgets.QPushButton(self)
        self.pushButton_6.clicked.connect(
            lambda: self.addTextToExpression("x√(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_6.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_2.addWidget(self.pushButton_6, 2, 4, 1, 1)

        self.pushButton_5 = QtWidgets.QPushButton(self)
        self.pushButton_5.clicked.connect(
            lambda: self.addTextToExpression("√(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_5.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_2.addWidget(self.pushButton_5, 2, 3, 1, 1)

        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.clicked.connect(
            lambda: self.addTextToExpression("(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_2.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 3, 1, 1)

        self.pushButton_7 = QtWidgets.QPushButton(self)
        self.pushButton_7.clicked.connect(self.openLinearSystemWindow)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_7.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_2.addWidget(self.pushButton_7, 3, 3, 1, 2)

        self.pushButton_8 = QtWidgets.QPushButton(self)
        self.pushButton_8.clicked.connect(
            self.clearExpressionLable
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_8.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_8.setSizePolicy(sizePolicy)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_2.addWidget(self.pushButton_8, 0, 0, 1, 1)

        self.pushButton_10 = QtWidgets.QPushButton(self)
        self.pushButton_10.clicked.connect(
            self.removeOneCharacter
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_10.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_10.setSizePolicy(sizePolicy)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_2.addWidget(self.pushButton_10, 1, 0, 1, 1)

        self.pushButton_11 = QtWidgets.QPushButton(self)
        self.pushButton_11.clicked.connect(
            lambda: self.addTextToExpression("ans")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_11.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_11.setSizePolicy(sizePolicy)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout_2.addWidget(self.pushButton_11, 2, 0, 1, 1)

        self.pushButton_12 = QtWidgets.QPushButton(self)
        self.pushButton_12.clicked.connect(
            lambda: self.addTextToExpression("abs(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_12.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_12.setSizePolicy(sizePolicy)
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout_2.addWidget(self.pushButton_12, 3, 0, 1, 1)

        self.pushButton_32 = QtWidgets.QPushButton(self)
        self.pushButton_32.clicked.connect(
            lambda: self.addTextToExpression("sin(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_32.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_32.setSizePolicy(sizePolicy)
        self.pushButton_32.setObjectName("pushButton_32")
        self.gridLayout_2.addWidget(self.pushButton_32, 0, 1, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.clicked.connect(
            lambda: self.addTextToExpression("asin(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton.sizePolicy().hasHeightForWidth()
            )
        self.pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 2, 1, 1)

        self.pushButton_34 = QtWidgets.QPushButton(self)
        self.pushButton_34.clicked.connect(
            lambda: self.addTextToExpression("cos(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_34.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_34.setSizePolicy(sizePolicy)
        self.pushButton_34.setObjectName("pushButton_34")
        self.gridLayout_2.addWidget(self.pushButton_34, 1, 1, 1, 1)

        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.clicked.connect(
            lambda: self.addTextToExpression("acos(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_4.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 1, 2, 1, 1)

        self.pushButton_35 = QtWidgets.QPushButton(self)
        self.pushButton_35.clicked.connect(
            lambda: self.addTextToExpression("tang(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_35.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_35.setSizePolicy(sizePolicy)
        self.pushButton_35.setObjectName("pushButton_35")
        self.gridLayout_2.addWidget(self.pushButton_35, 2, 1, 1, 1)

        self.pushButton_9 = QtWidgets.QPushButton(self)
        self.pushButton_9.clicked.connect(
            lambda: self.addTextToExpression("atang(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_9.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(False)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_2.addWidget(self.pushButton_9, 2, 2, 1, 1)

        self.pushButton_30 = QtWidgets.QPushButton(self)
        self.pushButton_30.clicked.connect(
            lambda: self.addTextToExpression("fact(")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_30.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_30.setSizePolicy(sizePolicy)
        self.pushButton_30.setObjectName("pushButton_30")
        self.gridLayout_2.addWidget(self.pushButton_30, 1, 3, 1, 1)

        self.pushButton_24 = QtWidgets.QPushButton(self)
        self.pushButton_24.clicked.connect(
            lambda: self.addTextToExpression("^")
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_24.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_24.setSizePolicy(sizePolicy)
        self.pushButton_24.setObjectName("pushButton_24")
        self.gridLayout_2.addWidget(self.pushButton_24, 1, 4, 1, 1)

        self.pushButton_31 = QtWidgets.QPushButton(self)
        self.pushButton_31.clicked.connect(
            self.switchRadDeg
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_31.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_31.setSizePolicy(sizePolicy)
        self.pushButton_31.setObjectName("pushButton_31")
        self.gridLayout_2.addWidget(self.pushButton_31, 3, 1, 1, 2)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 2)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint
            )
        self.gridLayout_5.setContentsMargins(10, 10, 10, 10)
        self.gridLayout_5.setHorizontalSpacing(20)
        self.gridLayout_5.setVerticalSpacing(15)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_5.addWidget(self.line_2, 2, 0, 1, 2)

        self.pushButton_16 = QtWidgets.QPushButton(self)
        self.pushButton_16.clicked.connect(self.solveExpression)

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButton_16.sizePolicy().hasHeightForWidth()
            )
        self.pushButton_16.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton_16.setFont(font)
        self.pushButton_16.setObjectName("pushButton_16")
        self.gridLayout_5.addWidget(self.pushButton_16, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_2.sizePolicy().hasHeightForWidth()
            )
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_2.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft |
            QtCore.Qt.AlignVCenter
            )
        self.label_2.setWordWrap(False)
        self.label_2.setIndent(20)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Preferred
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth()
            )
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setMouseTracking(True)
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setLineWidth(1)
        self.label.setMidLineWidth(0)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing |
            QtCore.Qt.AlignVCenter
            )
        self.label.setIndent(20)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 2)
        self.gridLayout_5.setColumnStretch(0, 5)
        self.gridLayout_5.setRowStretch(0, 5)
        self.gridLayout.addLayout(self.gridLayout_5, 0, 0, 1, 4)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.setRowStretch(1, 3)
        self.gridLayout_6.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Calculator - IVS"))
        self.pushButton_22.setText(_translate("self", "4"))
        self.pushButton_14.setText(_translate("self", "8"))
        self.pushButton_15.setText(_translate("self", "9"))
        self.pushButton_17.setText(_translate("self", "5"))
        self.pushButton_13.setText(_translate("self", "7"))
        self.pushButton_25.setText(_translate("self", "1"))
        self.pushButton_23.setText(_translate("self", "2"))
        self.pushButton_29.setText(_translate("self", "."))
        self.pushButton_28.setText(_translate("self", "3"))
        self.pushButton_27.setText(_translate("self", "6"))
        self.pushButton_26.setText(_translate("self", "0"))
        self.pushButton_20.setText(_translate("self", "*"))
        self.pushButton_18.setText(_translate("self", "+"))
        self.pushButton_19.setText(_translate("self", "-"))
        self.pushButton_21.setText(_translate("self", "/"))
        self.pushButton_3.setText(_translate("self", ")"))
        self.pushButton_6.setText(_translate("self", "x√"))
        self.pushButton_5.setText(_translate("self", "2√"))
        self.pushButton_2.setText(_translate("self", "("))
        self.pushButton_7.setText(_translate("self", "Linear system"))
        self.pushButton_8.setText(_translate("self", "CE"))
        self.pushButton_10.setText(_translate("self", "C"))
        self.pushButton_11.setText(_translate("self", "ANS"))
        self.pushButton_12.setText(_translate("self", "abs"))
        self.pushButton_32.setText(_translate("self", "sin"))
        self.pushButton.setText(_translate("self", "asin"))
        self.pushButton_34.setText(_translate("self", "cos"))
        self.pushButton_4.setText(_translate("self", "acos"))
        self.pushButton_35.setText(_translate("self", "tang"))
        self.pushButton_9.setText(_translate("self", "atang"))
        self.pushButton_30.setText(_translate("self", "!"))
        self.pushButton_24.setText(_translate("self", "x^y"))
        self.pushButton_31.setText(_translate("self", "Swith to degree"))
        self.pushButton_16.setText(_translate("self", "="))
        self.label_2.setText(_translate("self", ""))
        self.label.setText(_translate("self", ""))

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Backspace):
            self.clearExpression = False
            self.removeOneCharacter()

        if (e.key() == Qt.Key_0):
            self.addTextToExpression("0")

        elif (e.key() == Qt.Key_1):
            self.addTextToExpression("1")

        elif (e.key() == Qt.Key_2):
            self.addTextToExpression("2")

        elif (e.key() == Qt.Key_3):
            self.addTextToExpression("3")

        elif (e.key() == Qt.Key_4):
            self.addTextToExpression("4")

        elif (e.key() == Qt.Key_5):
            self.addTextToExpression("5")

        elif (e.key() == Qt.Key_6):
            self.addTextToExpression("6")

        elif (e.key() == Qt.Key_7):
            self.addTextToExpression("7")

        elif (e.key() == Qt.Key_8):
            self.addTextToExpression("8")

        elif (e.key() == Qt.Key_9):
            self.addTextToExpression("9")

        elif (e.key() == Qt.Key_S):
            self.addTextToExpression("s")

        elif (e.key() == Qt.Key_I):
            self.addTextToExpression("i")

        elif (e.key() == Qt.Key_N):
            self.addTextToExpression("n")

        elif (e.key() == Qt.Key_A):
            self.addTextToExpression("a")

        elif (e.key() == Qt.Key_F):
            self.addTextToExpression("f")

        elif (e.key() == Qt.Key_C):
            self.addTextToExpression("c")

        elif (e.key() == Qt.Key_T):
            self.addTextToExpression("t")

        elif (e.key() == Qt.Key_B):
            self.addTextToExpression("b")

        elif (e.key() == Qt.Key_O):
            self.addTextToExpression("o")

        elif (e.key() == Qt.Key_G):
            self.addTextToExpression("g")

        elif (e.key() == Qt.Key_Q):
            self.addTextToExpression("q")

        elif (e.key() == Qt.Key_R):
            self.addTextToExpression("r")

        elif (e.key() == Qt.Key_E):
            self.addTextToExpression("e")

        elif (e.key() == Qt.Key_P):
            self.addTextToExpression("p")

        elif (e.key() == Qt.Key_Plus):
            self.addTextToExpression("+")

        elif (e.key() == Qt.Key_Minus):
            self.addTextToExpression("-")

        elif (e.key() == Qt.Key_Asterisk):
            self.addTextToExpression("*")

        elif (e.key() == Qt.Key_Slash):
            self.addTextToExpression("/")

        elif (e.key() == Qt.Key_Period):
            self.addTextToExpression(".")

        elif (e.key() == Qt.Key_Comma):
            self.addTextToExpression(",")

        elif (e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return):
            self.solveExpression()

        elif (e.key() == Qt.Key_Exclam):
            self.addTextToExpression("fact(")

        elif (e.key() == Qt.Key_ParenLeft):
            self.addTextToExpression("(")

        elif (e.key() == Qt.Key_ParenRight):
            self.addTextToExpression(")")

        elif (e.key() == Qt.Key_Escape):
            self.close()

    def switchRadDeg(self):
        self.mathSolver.switch_rad_deg()
        if (self.mathSolver.is_degree):
            self.pushButton_31.setText("Swith to radian")
        else:
            self.pushButton_31.setText("Swith to degree")

    def openLinearSystemWindow(self):
        self.linearSystem.show()
        self.setEnabled(False)
        self.linearSystem.setEnabled(True)

    def loadAns(self):
        _translate = QtCore.QCoreApplication.translate

        self.addTextToExpression("")
        ans = self.mathSolver.ans

        self.label_2.setText(_translate(
            "self",
            self.label_2.text() + str(ans)
            ))

    def clearExpressionLable(self):
        self.clearExpression = True
        self.addTextToExpression("")

    def removeOneCharacter(self):
        _translate = QtCore.QCoreApplication.translate

        if (len(self.label_2.text()) != 0):
            self.label_2.setText(_translate(
                "self",
                self.label_2.text()[:-1]
                ))

    def addTextToExpression(self, text):
        _translate = QtCore.QCoreApplication.translate

        if (self.clearExpression):
            self.label_2.setText(_translate("self", ""))
            self.clearExpression = False

        self.label_2.setText(_translate(
            "self",
            self.label_2.text() + text
            ))

    def solveExpression(self):
        _translate = QtCore.QCoreApplication.translate
        try:
            self.clearExpression = True
            expression = self.label_2.text()
            expression = expression.replace("^", "**")
            expression = expression.replace("x√", "root")
            expression = expression.replace("√", "sqrt")

            self.label.setText(_translate(
                "self",
                str(self.mathSolver.solve(expression))
                ))

        except Exception as err:
            self.label.setText(_translate("self", str(err)))


def Win_run(ar):
    app = QtWidgets.QApplication(ar)
    ui = Ui_Form()
    ui.show()
    sys.exit(app.exec_())
