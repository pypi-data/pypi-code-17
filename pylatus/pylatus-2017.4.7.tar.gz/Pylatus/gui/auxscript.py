#!/usr/bin/python
# -*- coding: utf-8 -*-

from keyword import kwlist
from collections import namedtuple
from PyQt5 import QtGui, QtCore, QtWidgets


class QPyCompletionTextEdit(QtWidgets.QTextEdit):
    eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="  # end of word

    def setCompleter(self, keywords):
        self.completer = QtWidgets.QCompleter(keywords + kwlist, self)
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        # noinspection PyUnresolvedReferences
        self.completer.activated.connect(self.insertCompletion)

    @QtCore.pyqtSlot(str)
    def insertCompletion(self, completion):
        tc = self.textCursor()
        tc.movePosition(QtGui.QTextCursor.StartOfWord)
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        tc.insertText(completion)
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        self.completer.setWidget(self)
        QtWidgets.QTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        popup = self.completer.popup()
        key = event.key()
        if popup.isVisible() and key in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return, QtCore.Qt.Key_Escape,
                                         QtCore.Qt.Key_Tab, QtCore.Qt.Key_Backtab):
            event.ignore()
            return

        if key == QtCore.Qt.Key_Tab:
            self.textCursor().insertText('  ')
            return

        QtWidgets.QTextEdit.keyPressEvent(self, event)
        text = event.text()
        completionPrefix = self.textUnderCursor()

        if not text or len(completionPrefix) < 2 or text[-1] in self.eow:
            popup.hide()
            return

        if completionPrefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completionPrefix)
            popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(popup.sizeHintForColumn(0) + popup.verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)  # popup it up!


class QPyHighlighter(QtGui.QSyntaxHighlighter):
    HighlightingRule = namedtuple('HighlightingRule', ['pattern', 'format'])

    def __init__(self, specialWordsList, parent):
        super().__init__(parent)
        self.highlightingRules = []

        # keywords
        keyword = QtGui.QTextCharFormat()
        brush = QtGui.QBrush(QtCore.Qt.darkBlue, QtCore.Qt.SolidPattern)
        keyword.setForeground(brush)
        keyword.setFontWeight(QtGui.QFont.Bold)
        for word in kwlist:
            pattern = QtCore.QRegExp("\\b" + word + "\\b")
            rule = self.HighlightingRule(pattern, keyword)
            self.highlightingRules.append(rule)

        # specialWords
        specialWords = QtGui.QTextCharFormat()
        brush = QtGui.QBrush(QtCore.Qt.magenta, QtCore.Qt.SolidPattern)
        specialWords.setForeground(brush)
        specialWords.setFontWeight(QtGui.QFont.Bold)
        for word in specialWordsList:
            pattern = QtCore.QRegExp("\\b" + word + "\\b")
            rule = self.HighlightingRule(pattern, specialWords)
            self.highlightingRules.append(rule)

        # assignmentOperator
        assignmentOperator = QtGui.QTextCharFormat()
        brush = QtGui.QBrush(QtCore.Qt.darkBlue, QtCore.Qt.SolidPattern)
        pattern = QtCore.QRegExp("(<){1,2}-")
        assignmentOperator.setForeground(brush)
        assignmentOperator.setFontWeight(QtGui.QFont.Bold)
        rule = self.HighlightingRule(pattern, assignmentOperator)
        self.highlightingRules.append(rule)

        # delimiter
        delimiter = QtGui.QTextCharFormat()
        pattern = QtCore.QRegExp("[\)\(]+|[\{\}]+|[][]+")
        delimiter.setForeground(brush)
        delimiter.setFontWeight(QtGui.QFont.Bold)
        rule = self.HighlightingRule(pattern, delimiter)
        self.highlightingRules.append(rule)

        # boolean
        boolean = QtGui.QTextCharFormat()
        boolean.setForeground(brush)
        keywords = ["True", "False"]
        for word in keywords:
            pattern = QtCore.QRegExp("\\b" + word + "\\b")
            rule = self.HighlightingRule(pattern, boolean)
            self.highlightingRules.append(rule)

        # number
        number = QtGui.QTextCharFormat()
        pattern = QtCore.QRegExp("[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
        pattern.setMinimal(True)
        number.setForeground(brush)
        rule = self.HighlightingRule(pattern, number)
        self.highlightingRules.append(rule)

        # comment
        comment = QtGui.QTextCharFormat()
        brush = QtGui.QBrush(QtCore.Qt.gray, QtCore.Qt.SolidPattern)
        pattern = QtCore.QRegExp("#[^\n]*")
        comment.setForeground(brush)
        comment.setFontItalic(True)
        rule = self.HighlightingRule(pattern, comment)
        self.highlightingRules.append(rule)

        # string
        string = QtGui.QTextCharFormat()
        brush = QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern)
        pattern = QtCore.QRegExp("\".*\"")
        pattern.setMinimal(True)
        string.setForeground(brush)
        rule = self.HighlightingRule(pattern, string)
        self.highlightingRules.append(rule)

        # singleQuotedString
        singleQuotedString = QtGui.QTextCharFormat()
        pattern = QtCore.QRegExp("\'.*\'")
        pattern.setMinimal(True)
        singleQuotedString.setForeground(brush)
        rule = self.HighlightingRule(pattern, singleQuotedString)
        self.highlightingRules.append(rule)

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QtCore.QRegExp(rule.pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
