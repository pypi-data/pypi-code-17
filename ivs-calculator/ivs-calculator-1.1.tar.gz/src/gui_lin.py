# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'linearSystem.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
try:
    from src.mathlib import Solver
except ImportError:
    from mathlib import Solver


class Ui_Form_LinearSystem(QtWidgets.QWidget):

    def __init__(self, parent):
        super().__init__()
        self.clearExpression = False
        self.parentUi = parent
        self.setupUi()

    def setupUi(self):
        self.setObjectName("self")
        self.resize(594, 424)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.clicked.connect(
            self.calculateLinSystem
            )

        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(
            self.pushButton.sizePolicy().hasHeightForWidth()
            )
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.pushButton.setFont(font)
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 0, 1, 10)
        self.lineEdit_7 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_7.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout.addWidget(self.lineEdit_7, 2, 4, 1, 1)
        self.lineEdit_5 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_5.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout.addWidget(self.lineEdit_5, 2, 0, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_6.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout.addWidget(self.lineEdit_6, 2, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_8.sizePolicy().hasHeightForWidth()
            )
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 6, 1, 1)
        self.label = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.label.sizePolicy().hasHeightForWidth()
            )
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 10)
        self.label_2 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 7, 1, 1)
        self.label_9 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_9.sizePolicy().hasHeightForWidth()
            )
        self.label_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 2, 7, 1, 1)
        self.label_7 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_7.sizePolicy().hasHeightForWidth()
            )
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 3, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_4.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 1, 9, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_2.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 2, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_8.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout.addWidget(self.lineEdit_8, 2, 9, 1, 1)
        self.label_6 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_6.sizePolicy().hasHeightForWidth()
            )
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 6, 1, 1)
        self.label_4 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit.setFont(font)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_3.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 1, 4, 1, 1)
        self.lineEdit_9 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_9.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_9.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.gridLayout.addWidget(self.lineEdit_9, 3, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_10.sizePolicy().hasHeightForWidth()
            )
        self.label_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 3, 1, 1, 1)
        self.lineEdit_10 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_10.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_10.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.gridLayout.addWidget(self.lineEdit_10, 3, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_11.sizePolicy().hasHeightForWidth()
            )
        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 3, 3, 1, 1)
        self.lineEdit_11 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_11.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.gridLayout.addWidget(self.lineEdit_11, 3, 4, 1, 1)
        self.label_12 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_12.sizePolicy().hasHeightForWidth()
            )
        self.label_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 3, 6, 1, 1)
        self.label_13 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_13.sizePolicy().hasHeightForWidth()
            )
        self.label_13.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 3, 7, 1, 1)
        self.lineEdit_12 = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.lineEdit_12.sizePolicy().hasHeightForWidth()
            )
        self.lineEdit_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setItalic(True)
        self.lineEdit_12.setFont(font)
        self.lineEdit_12.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.gridLayout.addWidget(self.lineEdit_12, 3, 9, 1, 1)
        self.label_14 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Preferred
            )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.label_14.sizePolicy().hasHeightForWidth()
            )
        self.label_14.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setItalic(True)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 5, 0, 1, 10)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "Linear system - IVS"))
        self.pushButton.setText(_translate("self", "Calculate"))
        self.lineEdit_7.setText(_translate("self", ""))    # OK
        self.lineEdit_5.setText(_translate("self", ""))    # OK
        self.lineEdit_6.setText(_translate("self", ""))    # OK
        self.label_8.setText(_translate("self", "z"))
        self.label.setText(_translate("self", "Linear system"))
        self.label_2.setText(_translate("self", "="))
        self.label_9.setText(_translate("self", "="))
        self.label_7.setText(_translate("self", "y"))
        self.lineEdit_4.setText(_translate("self", ""))    # OK
        self.lineEdit_2.setText(_translate("self", ""))    # OK
        self.lineEdit_8.setText(_translate("self", ""))    # OK
        self.label_6.setText(_translate("self", "x"))
        self.label_5.setText(_translate("self", "z"))
        self.label_4.setText(_translate("self", "y"))
        self.label_3.setText(_translate("self", "x"))
        self.lineEdit.setText(_translate("self", ""))    # OK
        self.lineEdit_3.setText(_translate("self", ""))    # OK
        self.lineEdit_9.setText(_translate("self", ""))    # OK
        self.label_10.setText(_translate("self", "x"))
        self.lineEdit_10.setText(_translate("self", ""))    # OK
        self.label_11.setText(_translate("self", "y"))
        self.lineEdit_11.setText(_translate("self", ""))    # OK
        self.label_12.setText(_translate("self", "z"))
        self.label_13.setText(_translate("self", "="))
        self.lineEdit_12.setText(_translate("self", ""))
        self.label_14.setText(_translate(
            "self",
            ""
            ))

    def calculateLinSystem(self):
        _translate = QtCore.QCoreApplication.translate

        try:
            firstLin = [
                int(self.lineEdit.text()) if (self.lineEdit.text())
                else 0,
                int(self.lineEdit_2.text()) if (self.lineEdit_2.text())
                else 0,
                int(self.lineEdit_3.text()) if (self.lineEdit_3.text())
                else 0
                ]
            secondLin = [
                int(self.lineEdit_5.text()) if (self.lineEdit_5.text())
                else 0,
                int(self.lineEdit_6.text()) if (self.lineEdit_6.text())
                else 0,
                int(self.lineEdit_7.text()) if (self.lineEdit_7.text())
                else 0
            ]
            thirdLin = [
                int(self.lineEdit_9.text()) if (self.lineEdit_9.text())
                else 0,
                int(self.lineEdit_10.text()) if (self.lineEdit_10.text())
                else 0,
                int(self.lineEdit_11.text()) if (self.lineEdit_11.text())
                else 0
            ]
            rightLin = [
                int(self.lineEdit_4.text()) if (self.lineEdit_4.text())
                else 0,
                int(self.lineEdit_8.text()) if (self.lineEdit_8.text())
                else 0,
                int(self.lineEdit_12.text()) if (self.lineEdit_12.text())
                else 0
            ]

            resultLin = self.parentUi.mathSolver.linear_solve(firstLin,
                                                              secondLin,
                                                              thirdLin,
                                                              rightLin)

            if (not resultLin):
                self.label_14.setText(_translate(
                    "self",
                    "Invalid input"
                    ))
            else:
                self.label_14.setText(_translate(
                    "self",
                    "x=" + str(resultLin[0]) + "    " +
                    "y=" + str(resultLin[1]) + "    " +
                    "z=" + str(resultLin[2])
                    ))
        except:
            self.label_14.setText(_translate(
                "self",
                "Invalid input"
                ))
            return

    def closeEvent(self, event):
        self.hide()
        self.parentUi.show()
        self.setEnabled(False)
        self.parentUi.setEnabled(True)
        event.accept()

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Escape):
            self.hide()
            self.parentUi.show()
            self.setEnabled(False)
            self.parentUi.setEnabled(True)
