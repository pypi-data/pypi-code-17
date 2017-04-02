# -*- coding: utf-8 -*-

#
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogModulation(object):
    def setupUi(self, DialogModulation):
        DialogModulation.setObjectName("DialogModulation")
        DialogModulation.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(DialogModulation)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.comboBoxCustomModulations = QtWidgets.QComboBox(DialogModulation)
        self.comboBoxCustomModulations.setEditable(True)
        self.comboBoxCustomModulations.setInsertPolicy(QtWidgets.QComboBox.InsertAtCurrent)
        self.comboBoxCustomModulations.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.comboBoxCustomModulations.setObjectName("comboBoxCustomModulations")
        self.comboBoxCustomModulations.addItem("")
        self.gridLayout_5.addWidget(self.comboBoxCustomModulations, 0, 0, 1, 1)
        self.btnAddModulation = QtWidgets.QToolButton(DialogModulation)
        icon = QtGui.QIcon.fromTheme("list-add")
        self.btnAddModulation.setIcon(icon)
        self.btnAddModulation.setObjectName("btnAddModulation")
        self.gridLayout_5.addWidget(self.btnAddModulation, 0, 1, 1, 1)
        self.btnRemoveModulation = QtWidgets.QToolButton(DialogModulation)
        icon = QtGui.QIcon.fromTheme("list-remove")
        self.btnRemoveModulation.setIcon(icon)
        self.btnRemoveModulation.setObjectName("btnRemoveModulation")
        self.gridLayout_5.addWidget(self.btnRemoveModulation, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_5)
        self.scrollArea = QtWidgets.QScrollArea(DialogModulation)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 769, 862))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.lPlus = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lPlus.sizePolicy().hasHeightForWidth())
        self.lPlus.setSizePolicy(sizePolicy)
        self.lPlus.setMaximumSize(QtCore.QSize(30, 30))
        self.lPlus.setText("")
        self.lPlus.setPixmap(QtGui.QPixmap(":/icons/data/icons/plus.png"))
        self.lPlus.setScaledContents(True)
        self.lPlus.setAlignment(QtCore.Qt.AlignCenter)
        self.lPlus.setObjectName("lPlus")
        self.gridLayout_7.addWidget(self.lPlus, 2, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_7.addWidget(self.label_7, 7, 0, 1, 1)
        self.gVOriginalSignal = ZoomAndDropableGraphicView(self.scrollAreaWidgetContents_2)
        self.gVOriginalSignal.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gVOriginalSignal.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.gVOriginalSignal.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing)
        self.gVOriginalSignal.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.gVOriginalSignal.setObjectName("gVOriginalSignal")
        self.gridLayout_7.addWidget(self.gVOriginalSignal, 8, 1, 1, 1)
        self.gVData = ZoomableGraphicView(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gVData.sizePolicy().hasHeightForWidth())
        self.gVData.setSizePolicy(sizePolicy)
        self.gVData.setAcceptDrops(False)
        self.gVData.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gVData.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.gVData.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing)
        self.gVData.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.gVData.setObjectName("gVData")
        self.gridLayout_7.addWidget(self.gVData, 3, 1, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.treeViewSignals = ModulatorTreeView(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeViewSignals.sizePolicy().hasHeightForWidth())
        self.treeViewSignals.setSizePolicy(sizePolicy)
        self.treeViewSignals.setProperty("showDropIndicator", True)
        self.treeViewSignals.setDragEnabled(True)
        self.treeViewSignals.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.treeViewSignals.setHeaderHidden(True)
        self.treeViewSignals.setObjectName("treeViewSignals")
        self.gridLayout_6.addWidget(self.treeViewSignals, 0, 0, 1, 2)
        self.cbShowDataBitsOnly = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbShowDataBitsOnly.sizePolicy().hasHeightForWidth())
        self.cbShowDataBitsOnly.setSizePolicy(sizePolicy)
        self.cbShowDataBitsOnly.setMinimumSize(QtCore.QSize(0, 0))
        self.cbShowDataBitsOnly.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.cbShowDataBitsOnly.setObjectName("cbShowDataBitsOnly")
        self.gridLayout_6.addWidget(self.cbShowDataBitsOnly, 1, 0, 1, 2)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.btnSearchPrev = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSearchPrev.sizePolicy().hasHeightForWidth())
        self.btnSearchPrev.setSizePolicy(sizePolicy)
        self.btnSearchPrev.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btnSearchPrev.setText("")
        icon = QtGui.QIcon.fromTheme("go-previous")
        self.btnSearchPrev.setIcon(icon)
        self.btnSearchPrev.setObjectName("btnSearchPrev")
        self.gridLayout_4.addWidget(self.btnSearchPrev, 0, 0, 1, 1)
        self.lCurrentSearchResult = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lCurrentSearchResult.sizePolicy().hasHeightForWidth())
        self.lCurrentSearchResult.setSizePolicy(sizePolicy)
        self.lCurrentSearchResult.setMinimumSize(QtCore.QSize(0, 0))
        self.lCurrentSearchResult.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lCurrentSearchResult.setAlignment(QtCore.Qt.AlignCenter)
        self.lCurrentSearchResult.setObjectName("lCurrentSearchResult")
        self.gridLayout_4.addWidget(self.lCurrentSearchResult, 0, 1, 1, 1)
        self.lSlash = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lSlash.sizePolicy().hasHeightForWidth())
        self.lSlash.setSizePolicy(sizePolicy)
        self.lSlash.setMaximumSize(QtCore.QSize(7, 16777215))
        self.lSlash.setObjectName("lSlash")
        self.gridLayout_4.addWidget(self.lSlash, 0, 2, 1, 1)
        self.lTotalSearchresults = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lTotalSearchresults.sizePolicy().hasHeightForWidth())
        self.lTotalSearchresults.setSizePolicy(sizePolicy)
        self.lTotalSearchresults.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lTotalSearchresults.setAlignment(QtCore.Qt.AlignCenter)
        self.lTotalSearchresults.setObjectName("lTotalSearchresults")
        self.gridLayout_4.addWidget(self.lTotalSearchresults, 0, 3, 1, 1)
        self.btnSearchNext = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSearchNext.sizePolicy().hasHeightForWidth())
        self.btnSearchNext.setSizePolicy(sizePolicy)
        self.btnSearchNext.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btnSearchNext.setText("")
        icon = QtGui.QIcon.fromTheme("go-next")
        self.btnSearchNext.setIcon(icon)
        self.btnSearchNext.setObjectName("btnSearchNext")
        self.gridLayout_4.addWidget(self.btnSearchNext, 0, 4, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_4, 2, 0, 1, 2)
        self.lSamplesInViewOrigSignalText = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lSamplesInViewOrigSignalText.sizePolicy().hasHeightForWidth())
        self.lSamplesInViewOrigSignalText.setSizePolicy(sizePolicy)
        self.lSamplesInViewOrigSignalText.setObjectName("lSamplesInViewOrigSignalText")
        self.gridLayout_6.addWidget(self.lSamplesInViewOrigSignalText, 3, 0, 1, 1)
        self.lSamplesInViewOrigSignal = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lSamplesInViewOrigSignal.sizePolicy().hasHeightForWidth())
        self.lSamplesInViewOrigSignal.setSizePolicy(sizePolicy)
        self.lSamplesInViewOrigSignal.setObjectName("lSamplesInViewOrigSignal")
        self.gridLayout_6.addWidget(self.lSamplesInViewOrigSignal, 3, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_6.addWidget(self.label_10, 4, 0, 1, 1)
        self.lOriginalSignalSamplesSelected = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.lOriginalSignalSamplesSelected.setObjectName("lOriginalSignalSamplesSelected")
        self.gridLayout_6.addWidget(self.lOriginalSignalSamplesSelected, 4, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_6, 8, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.linEdDataBits = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linEdDataBits.sizePolicy().hasHeightForWidth())
        self.linEdDataBits.setSizePolicy(sizePolicy)
        self.linEdDataBits.setObjectName("linEdDataBits")
        self.gridLayout_2.addWidget(self.linEdDataBits, 0, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.spinBoxBitLength = QtWidgets.QSpinBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxBitLength.sizePolicy().hasHeightForWidth())
        self.spinBoxBitLength.setSizePolicy(sizePolicy)
        self.spinBoxBitLength.setMinimum(1)
        self.spinBoxBitLength.setMaximum(999999)
        self.spinBoxBitLength.setObjectName("spinBoxBitLength")
        self.gridLayout_2.addWidget(self.spinBoxBitLength, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)
        self.spinBoxSampleRate = KillerDoubleSpinBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxSampleRate.sizePolicy().hasHeightForWidth())
        self.spinBoxSampleRate.setSizePolicy(sizePolicy)
        self.spinBoxSampleRate.setDecimals(3)
        self.spinBoxSampleRate.setMinimum(0.001)
        self.spinBoxSampleRate.setMaximum(999999999.0)
        self.spinBoxSampleRate.setObjectName("spinBoxSampleRate")
        self.gridLayout_2.addWidget(self.spinBoxSampleRate, 4, 1, 1, 1)
        self.btnRestoreBits = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRestoreBits.sizePolicy().hasHeightForWidth())
        self.btnRestoreBits.setSizePolicy(sizePolicy)
        self.btnRestoreBits.setObjectName("btnRestoreBits")
        self.gridLayout_2.addWidget(self.btnRestoreBits, 2, 0, 1, 2)
        self.label_8 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_8.setStyleSheet("color:orange")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 2)
        self.gridLayout_7.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        self.gVModulated = ZoomableGraphicView(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gVModulated.sizePolicy().hasHeightForWidth())
        self.gVModulated.setSizePolicy(sizePolicy)
        self.gVModulated.setAcceptDrops(False)
        self.gVModulated.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gVModulated.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.gVModulated.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing)
        self.gVModulated.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.gVModulated.setObjectName("gVModulated")
        self.gridLayout_7.addWidget(self.gVModulated, 5, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_7.addWidget(self.label_6, 4, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lCarrierFreq = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lCarrierFreq.sizePolicy().hasHeightForWidth())
        self.lCarrierFreq.setSizePolicy(sizePolicy)
        self.lCarrierFreq.setObjectName("lCarrierFreq")
        self.gridLayout.addWidget(self.lCarrierFreq, 0, 0, 1, 1)
        self.doubleSpinBoxCarrierFreq = KillerDoubleSpinBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxCarrierFreq.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxCarrierFreq.setSizePolicy(sizePolicy)
        self.doubleSpinBoxCarrierFreq.setSuffix("")
        self.doubleSpinBoxCarrierFreq.setDecimals(3)
        self.doubleSpinBoxCarrierFreq.setMinimum(0.0)
        self.doubleSpinBoxCarrierFreq.setMaximum(99999999999.0)
        self.doubleSpinBoxCarrierFreq.setObjectName("doubleSpinBoxCarrierFreq")
        self.gridLayout.addWidget(self.doubleSpinBoxCarrierFreq, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.doubleSpinBoxCarrierPhase = QtWidgets.QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxCarrierPhase.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxCarrierPhase.setSizePolicy(sizePolicy)
        self.doubleSpinBoxCarrierPhase.setDecimals(3)
        self.doubleSpinBoxCarrierPhase.setMaximum(360.0)
        self.doubleSpinBoxCarrierPhase.setObjectName("doubleSpinBoxCarrierPhase")
        self.gridLayout.addWidget(self.doubleSpinBoxCarrierPhase, 1, 1, 1, 1)
        self.btnAutoDetect = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.btnAutoDetect.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnAutoDetect.sizePolicy().hasHeightForWidth())
        self.btnAutoDetect.setSizePolicy(sizePolicy)
        self.btnAutoDetect.setObjectName("btnAutoDetect")
        self.gridLayout.addWidget(self.btnAutoDetect, 2, 0, 1, 2)
        self.gridLayout_7.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.spinBoxGaussBT = QtWidgets.QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        self.spinBoxGaussBT.setMinimum(0.01)
        self.spinBoxGaussBT.setMaximum(0.99)
        self.spinBoxGaussBT.setSingleStep(0.01)
        self.spinBoxGaussBT.setObjectName("spinBoxGaussBT")
        self.gridLayout_3.addWidget(self.spinBoxGaussBT, 3, 1, 1, 2)
        self.spinBoxParameter1 = KillerDoubleSpinBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxParameter1.sizePolicy().hasHeightForWidth())
        self.spinBoxParameter1.setSizePolicy(sizePolicy)
        self.spinBoxParameter1.setDecimals(3)
        self.spinBoxParameter1.setMinimum(0.001)
        self.spinBoxParameter1.setMaximum(999999999.99)
        self.spinBoxParameter1.setObjectName("spinBoxParameter1")
        self.gridLayout_3.addWidget(self.spinBoxParameter1, 2, 1, 1, 2)
        self.lParameterfor1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lParameterfor1.sizePolicy().hasHeightForWidth())
        self.lParameterfor1.setSizePolicy(sizePolicy)
        self.lParameterfor1.setObjectName("lParameterfor1")
        self.gridLayout_3.addWidget(self.lParameterfor1, 2, 0, 1, 1)
        self.lParameterfor0 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lParameterfor0.sizePolicy().hasHeightForWidth())
        self.lParameterfor0.setSizePolicy(sizePolicy)
        self.lParameterfor0.setObjectName("lParameterfor0")
        self.gridLayout_3.addWidget(self.lParameterfor0, 1, 0, 1, 1)
        self.chkBoxLockSIV = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chkBoxLockSIV.sizePolicy().hasHeightForWidth())
        self.chkBoxLockSIV.setSizePolicy(sizePolicy)
        self.chkBoxLockSIV.setObjectName("chkBoxLockSIV")
        self.gridLayout_3.addWidget(self.chkBoxLockSIV, 9, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 10, 1, 1, 1)
        self.comboBoxModulationType = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxModulationType.sizePolicy().hasHeightForWidth())
        self.comboBoxModulationType.setSizePolicy(sizePolicy)
        self.comboBoxModulationType.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.comboBoxModulationType.setObjectName("comboBoxModulationType")
        self.comboBoxModulationType.addItem("")
        self.comboBoxModulationType.addItem("")
        self.comboBoxModulationType.addItem("")
        self.comboBoxModulationType.addItem("")
        self.gridLayout_3.addWidget(self.comboBoxModulationType, 0, 0, 1, 3)
        self.spinBoxParameter0 = KillerDoubleSpinBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxParameter0.sizePolicy().hasHeightForWidth())
        self.spinBoxParameter0.setSizePolicy(sizePolicy)
        self.spinBoxParameter0.setDecimals(3)
        self.spinBoxParameter0.setMinimum(0.001)
        self.spinBoxParameter0.setMaximum(999999999.99)
        self.spinBoxParameter0.setObjectName("spinBoxParameter0")
        self.gridLayout_3.addWidget(self.spinBoxParameter0, 1, 1, 1, 2)
        self.lSamplesInViewModulatedText = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lSamplesInViewModulatedText.sizePolicy().hasHeightForWidth())
        self.lSamplesInViewModulatedText.setSizePolicy(sizePolicy)
        self.lSamplesInViewModulatedText.setObjectName("lSamplesInViewModulatedText")
        self.gridLayout_3.addWidget(self.lSamplesInViewModulatedText, 5, 0, 1, 1)
        self.lSamplesInViewModulated = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lSamplesInViewModulated.sizePolicy().hasHeightForWidth())
        self.lSamplesInViewModulated.setSizePolicy(sizePolicy)
        self.lSamplesInViewModulated.setObjectName("lSamplesInViewModulated")
        self.gridLayout_3.addWidget(self.lSamplesInViewModulated, 5, 1, 1, 2)
        self.label_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 8, 0, 1, 1)
        self.lModulatedSelectedSamples = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.lModulatedSelectedSamples.setObjectName("lModulatedSelectedSamples")
        self.gridLayout_3.addWidget(self.lModulatedSelectedSamples, 8, 1, 1, 2)
        self.lGaussBT = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.lGaussBT.setObjectName("lGaussBT")
        self.gridLayout_3.addWidget(self.lGaussBT, 3, 0, 1, 1)
        self.lGaussWidth = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.lGaussWidth.setObjectName("lGaussWidth")
        self.gridLayout_3.addWidget(self.lGaussWidth, 4, 0, 1, 1)
        self.spinBoxGaussFilterWidth = QtWidgets.QDoubleSpinBox(self.scrollAreaWidgetContents_2)
        self.spinBoxGaussFilterWidth.setMinimum(0.01)
        self.spinBoxGaussFilterWidth.setMaximum(100.0)
        self.spinBoxGaussFilterWidth.setSingleStep(0.01)
        self.spinBoxGaussFilterWidth.setProperty("value", 1.0)
        self.spinBoxGaussFilterWidth.setObjectName("spinBoxGaussFilterWidth")
        self.gridLayout_3.addWidget(self.spinBoxGaussFilterWidth, 4, 1, 1, 2)
        self.gridLayout_7.addLayout(self.gridLayout_3, 5, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_7.addWidget(self.label_4, 0, 0, 1, 1)
        self.gVCarrier = ZoomableGraphicView(self.scrollAreaWidgetContents_2)
        self.gVCarrier.setAcceptDrops(False)
        self.gVCarrier.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gVCarrier.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.gVCarrier.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.HighQualityAntialiasing)
        self.gVCarrier.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.gVCarrier.setObjectName("gVCarrier")
        self.gridLayout_7.addWidget(self.gVCarrier, 0, 1, 2, 1)
        self.label_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_7.addWidget(self.label_5, 2, 0, 1, 1)
        self.lEqual = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lEqual.sizePolicy().hasHeightForWidth())
        self.lEqual.setSizePolicy(sizePolicy)
        self.lEqual.setMaximumSize(QtCore.QSize(30, 30))
        self.lEqual.setText("")
        self.lEqual.setPixmap(QtGui.QPixmap(":/icons/data/icons/equals_generator.png"))
        self.lEqual.setScaledContents(True)
        self.lEqual.setAlignment(QtCore.Qt.AlignCenter)
        self.lEqual.setObjectName("lEqual")
        self.gridLayout_7.addWidget(self.lEqual, 4, 1, 1, 1)
        self.btnSaveAndClose = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.btnSaveAndClose.setObjectName("btnSaveAndClose")
        self.gridLayout_7.addWidget(self.btnSaveAndClose, 9, 0, 1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(DialogModulation)
        QtCore.QMetaObject.connectSlotsByName(DialogModulation)

    def retranslateUi(self, DialogModulation):
        _translate = QtCore.QCoreApplication.translate
        DialogModulation.setWindowTitle(_translate("DialogModulation", "Modulation"))
        self.comboBoxCustomModulations.setItemText(0, _translate("DialogModulation", "My Modulation"))
        self.btnAddModulation.setText(_translate("DialogModulation", "..."))
        self.btnRemoveModulation.setText(_translate("DialogModulation", "..."))
        self.label_7.setText(_translate("DialogModulation", "Original Signal (drag&drop)"))
        self.cbShowDataBitsOnly.setText(_translate("DialogModulation", "Show Only Data Sequence\n"
"(10)"))
        self.lCurrentSearchResult.setText(_translate("DialogModulation", "-"))
        self.lSlash.setText(_translate("DialogModulation", "/"))
        self.lTotalSearchresults.setText(_translate("DialogModulation", "-"))
        self.lSamplesInViewOrigSignalText.setText(_translate("DialogModulation", "Samples in View:"))
        self.lSamplesInViewOrigSignal.setToolTip(_translate("DialogModulation", "<html><head/><body><p>Shown Samples in View:</p><p><span style=\" font-weight:600; color:#ff0000;\">Red</span> - if samples in view differ from original signal</p><p><span style=\" font-weight:600;\">Normal</span> - if samples in view are equal to the original signal</p></body></html>"))
        self.lSamplesInViewOrigSignal.setText(_translate("DialogModulation", "0"))
        self.label_10.setText(_translate("DialogModulation", "Samples selected:"))
        self.lOriginalSignalSamplesSelected.setText(_translate("DialogModulation", "0"))
        self.linEdDataBits.setPlaceholderText(_translate("DialogModulation", "Enter Data Bits here"))
        self.label.setText(_translate("DialogModulation", "Bit Length:"))
        self.label_3.setText(_translate("DialogModulation", "Sample Rate (Sps):"))
        self.btnRestoreBits.setText(_translate("DialogModulation", "Restore Bits"))
        self.label_8.setText(_translate("DialogModulation", "You compare raw bits."))
        self.label_6.setText(_translate("DialogModulation", "Modulation"))
        self.lCarrierFreq.setText(_translate("DialogModulation", "Frequency:"))
        self.label_2.setText(_translate("DialogModulation", "Phase:"))
        self.doubleSpinBoxCarrierPhase.setSuffix(_translate("DialogModulation", "°"))
        self.btnAutoDetect.setToolTip(_translate("DialogModulation", "<html><head/><body><p>Auto detect the frequency based on the original signal. You have to select a signal (<span style=\" font-weight:600;\">bottom of this window</span>) to use this feature.</p><p><br/></p><p>Select a signal by dragging it from the tree and dropping it on the graphics pane to the right.</p></body></html>"))
        self.btnAutoDetect.setText(_translate("DialogModulation", "Auto detect from original signal"))
        self.lParameterfor1.setText(_translate("DialogModulation", "Amplitude for 1:"))
        self.lParameterfor0.setText(_translate("DialogModulation", "Amplitude for 0:"))
        self.chkBoxLockSIV.setText(_translate("DialogModulation", "Lock SIV to original signal"))
        self.comboBoxModulationType.setItemText(0, _translate("DialogModulation", "Amplitude Shift Keying (ASK)"))
        self.comboBoxModulationType.setItemText(1, _translate("DialogModulation", "Frequency Shift Keying (FSK)"))
        self.comboBoxModulationType.setItemText(2, _translate("DialogModulation", "Gaussian Frequency Shift Keying (GFSK)"))
        self.comboBoxModulationType.setItemText(3, _translate("DialogModulation", "Phase Shift Keying (PSK)"))
        self.lSamplesInViewModulatedText.setText(_translate("DialogModulation", "Samples in View:"))
        self.lSamplesInViewModulated.setToolTip(_translate("DialogModulation", "<html><head/><body><p>Shown Samples in View:</p><p><span style=\" font-weight:600; color:#ff0000;\">Red</span> - if samples in view differ from original signal</p><p><span style=\" font-weight:600;\">Normal</span> - if samples in view are equal to the original signal</p></body></html>"))
        self.lSamplesInViewModulated.setText(_translate("DialogModulation", "101010121"))
        self.label_9.setText(_translate("DialogModulation", "Samples selected:"))
        self.lModulatedSelectedSamples.setText(_translate("DialogModulation", "0"))
        self.lGaussBT.setText(_translate("DialogModulation", "Gauss BT:"))
        self.lGaussWidth.setText(_translate("DialogModulation", "Gauss filter width:"))
        self.label_4.setText(_translate("DialogModulation", "Carrier"))
        self.label_5.setText(_translate("DialogModulation", "Data"))
        self.btnSaveAndClose.setText(_translate("DialogModulation", "Save and Close"))

from urh.ui.KillerDoubleSpinBox import KillerDoubleSpinBox
from urh.ui.views.ModulatorTreeView import ModulatorTreeView
from urh.ui.views.ZoomAndDropableGraphicView import ZoomAndDropableGraphicView
from urh.ui.views.ZoomableGraphicView import ZoomableGraphicView
from . import urh_rc
