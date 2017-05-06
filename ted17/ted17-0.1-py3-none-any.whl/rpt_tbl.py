# -*- coding: utf-8 -*-
'''
Created on 23 Mar 2017

@author: tedlaz

version 1.0
'''

import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtPrintSupport as Qp
# from PyQt4 import QtGui, QtCore, Qt
from tedutil import dec

import decimal


# Utility Functions
def gr(number):
    'Returns Greek Decimal(2) number or empty space'
    number = dec.dec(number)
    if abs(number) <= 0.004:
        return ''
    s = '%.2f' % number
    a, d = s.split('.')
    groups = []
    while a and a[-1].isdigit():
        groups.append(a[-3:])
        a = a[:-3]
    return a + '.'.join(reversed(groups)) + ',' + d


def gr0(number):
    'Returns Greek Decimal(2) number or 0,00'
    number = dec(number)
    if abs(number) <= 0.004:
        return '0,00'
    s = '%.2f' % number
    a, d = s.split('.')
    groups = []
    while a and a[-1].isdigit():
        groups.append(a[-3:])
        a = a[:-3]
    return a + '.'.join(reversed(groups)) + ',' + d


def grint(number):
    'Returns Greek Decimal(1) number'
    number = dec(number)
    if abs(number) <= 0.004:
        return ''
    s = '%.1f' % number
    a, d = s.split('.')
    groups = []
    while a and a[-1].isdigit():
        groups.append(a[-3:])
        a = a[:-3]
    return a + '.'.join(reversed(groups)) + ',' + d


def grd(imnia):
    'Returns Greek Date'
    y, m, d = imnia.split('-')
    return '%s/%s/%s' % (d, m, y)


def align(opt=0):
    if opt == 0:
        option = Qg.QTextOption(Qc.Qt.AlignLeft | Qc.Qt.AlignVCenter)
    elif opt == 1:
        option = Qg.QTextOption(Qc.Qt.AlignCenter | Qc.Qt.AlignVCenter)
    else:
        option = Qg.QTextOption(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
    option.setWrapMode(Qg.QTextOption.WordWrap)
    return option


def frmt(val, typos):
    if typos == 0:  # String
        frmtVal = '%s' % val
    elif typos == 1:  # Integer
        frmtVal = '%s' % val
    elif typos == 2:  # Decimal
        frmtVal = gr(val)
    elif typos == 3:  # Date
        frmtVal = grd(val)
    elif typos == 4:  # Decimal with one decimal digit
        frmtVal = grint(val)
    else:
        frmtVal = '%s' % val
    return frmtVal


class qtTableReport():
    def __init__(self, f={}):
        self.f = f
        self.printer = Qp.QPrinter()
        # Set portrait or landscape
        if self.f['orientation'] == 0:
            self.printer.setOrientation(Qp.QPrinter.Portrait)
        else:
            self.printer.setOrientation(Qp.QPrinter.Landscape)
        fontSize = 9
        widthOffset = 3
        # Set Fonts
        self.__RHead1Font = Qg.QFont(self.f['fontFamily'], 20)
        self.__RHead1Font.setBold(True)

        self.__RHead2Font = Qg.QFont(self.f['fontFamily'], 12)
        self.__RHead2Font.setBold(True)
        self.__RHead2Font.setItalic(True)

        self.__RHead3Font = Qg.QFont(self.f['fontFamily'], 10)
        self.__RHead3Font.setItalic(True)

        self.__TableHeadFont = Qg.QFont(self.f['fontFamily'], fontSize)
        self.__TableHeadFont.setBold(True)

        self.__TableLineFont = Qg.QFont(self.f['fontFamily'], fontSize)

        self.__FooterFont = Qg.QFont(self.f['fontFamily'], fontSize)
        # self.__FooterFont.setItalic(True)

        self.tableMetrics = Qg.QFontMetrics(self.__TableLineFont)
        self.tableHeaderHeight = int(self.tableMetrics.height() * 3)
        self.tableColumnHeight = int(self.tableMetrics.height() * 1.7)
        # Το πλάτος των στηλών
        self.colWidths = [self.tableMetrics.width('w' * i) + widthOffset for i in self.f['columnSizes']]
        self.totalColWidths = sum(self.colWidths)

        # Ο αριθμός των στηλών
        self.__colNo = len(self.colWidths)

    def __drawCol(self):
        pass

    def __drawCenteredText(self, text, painter, font, spaceAfter=25):
        if text == '':
            return
        painter.setFont(font)
        painter.drawText(Qc.QRectF(self.x,
                                   self.y,
                                   self.pageRect.width()- 2 * self.xLeftMargin,
                                   31),
                         text,
                         align(1))
        self.y += spaceAfter

    def __drawReportHeader(self, painter, hspaceAfter=20):
        self.__drawCenteredText(self.f['ReportHeader1'],
                                painter,
                                self.__RHead1Font,
                                spaceAfter=25)
        self.__drawCenteredText(self.f['ReportHeader2'],
                                painter,
                                self.__RHead2Font,
                                spaceAfter=20)
        self.__drawCenteredText(self.f['ReportHeader3'],
                                painter,
                                self.__RHead3Font,
                                spaceAfter=20)
        self.y += hspaceAfter

    def __fixPainterBug(self, painter):
        'This is a workaround for painter to paint lines properly'
        painter.setPen(Qc.Qt.NoPen)
        painter.setPen(Qc.Qt.black)

    def __drawPageHeader(self, painter):
        pass

    def __drawRectWithText(self, x, y, width, height, value, option):
        pass

    def __drawTableHeader(self, painter):
        painter.save()
        painter.setFont(self.__TableHeadFont)
        pen = Qg.QPen()
        pen.setColor(Qc.Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        self.x = self.xLeftMargin
        for i in range(len(self.f['headerLabels'])):
            # painter.drawRect(self.x,self.y,self.colWidths[i],self.tableHeaderHeight)
            painter.drawLine(self.x,
                             self.y + self.tableHeaderHeight,
                             self.x + self.colWidths[i],
                             self.y + self.tableHeaderHeight)
            painter.drawText(Qc.QRectF(self.x + 3,
                                       self.y + 3,
                                       self.colWidths[i] - 6,
                                       self.tableHeaderHeight - 6),
                             self.f['headerLabels'][i],
                             align(1))
            self.x += self.colWidths[i]
        self.y += self.tableHeaderHeight
        self.x = self.xLeftMargin
        painter.restore()

    def __drawTableLines(self, painter):
        painter.save()
        self.x = self.xLeftMargin
        j = 0
        dlen = len(self.f['data'])
        for el in self.f['data']:
            if self.y > self.pageRect.height() - 95:
                painter.save()
                self.__drawNewPage(painter)
                painter.restore()
            painter.setFont(self.__TableLineFont)
            painter.setPen(Qc.Qt.black | Qc.Qt.DashLine)
            j += 1
            for i in range(self.__colNo):
                if j == dlen:
                    painter.save()
                    pen = Qg.QPen()
                    pen.setColor(Qc.Qt.black)
                    pen.setWidth(2)
                    painter.setPen(pen)
                    painter.drawLine(self.x,
                                     self.y + self.tableColumnHeight,
                                     self.x + self.colWidths[i],
                                     self.y + self.tableColumnHeight)
                    painter.restore()
                painter.drawLine(self.x,
                                 self.y + self.tableColumnHeight,
                                 self.x + self.colWidths[i],
                                 self.y + self.tableColumnHeight)
                painter.drawText(Qc.QRectF(self.x + 3,
                                           self.y + 3,
                                           self.colWidths[i] - 6,
                                           self.tableColumnHeight - 6),
                                 frmt(el[i], self.f['columnTypes'][i]),
                                 align(self.f['columnAlign'][i]))
                self.x += self.colWidths[i]
            self.x = self.xLeftMargin
            self.y += self.tableColumnHeight
        painter.restore()

    def __drawTableFooter(self, painter):
        painter.save()
        if not self.f['columnToSum']:
            return False
        sumArr = []
        for el in self.f['columnToSum']:
            if el == 0:
                sumArr.append('')
            else:
                sumArr.append(0)

        for el in self.f['data']:
            for i in range(self.__colNo):
                if self.f['columnToSum'][i] != 0:
                    sumArr[i] += el[i]
        self.y += 10
        painter.setFont(self.__TableHeadFont)
        self.x = self.xLeftMargin
        for i in range(self.__colNo):
            if self.f['columnToSum'][i]:
                painter.drawText(QtCore.QRectF(self.x + 3,
                                               self.y + 3,
                                               self.colWidths[i] - 6,
                                               self.tableColumnHeight - 6),
                                 frmt(sumArr[i], self.f['columnTypes'][i]),
                                 align(self.f['columnAlign'][i]))
            self.x += self.colWidths[i]
        # painter.drawRect(self.xLeftMargin,self.y,sum(self.colWidths),self.tableColumnHeight)
        self.y += self.tableColumnHeight
        self.x = self.xLeftMargin
        painter.restore()

    def __drawPageFooter(self, painter):
        painter.save()
        pen = Qg.QPen()
        pen.setColor(Qc.Qt.black)
        painter.setPen(pen)
        self.x = self.xLeftMargin
        old_y = self.y
        self.y = self.yFooter
        if self.f['footerLine']:
            painter.drawLine(self.x, self.y,
                             self.pageRect.width() - 30, self.y)
            # painter.drawLine(self.x,self.y,self.totalColWidths+self.xLeftMargin,self.y)
        self.y += 2
        painter.setFont(self.__FooterFont)
        if self.f['footerPageNumberText'] == '':
            finalText = self.f['footerText']
        else:
            finalText = '%s' % self.f['footerText']
            selText = '%s %s' % (self.f['footerPageNumberText'], self.pageNo)
        painter.drawText(Qc.QRectF(self.x,
                                   self.y,
                                   self.pageRect.width() - 2 * self.xLeftMargin,
                                   31),
                         finalText,
                         align(1))
        painter.drawText(Qc.QRectF(self.x,
                                   self.y,
                                   self.pageRect.width() - 2 * self.xLeftMargin,
                                   31),
                         selText, align(2))
        self.y = old_y
        self.x = self.xLeftMargin
        painter.restore()

    def __drawNewPage(self, painter):
        painter.save()
        self.printer.newPage()
        self.pageNo += 1
        self.x = self.xLeftMargin
        self.y = self.yTopMargin
        self.__drawPageFooter(painter)
        self.__drawTableHeader(painter)
        painter.restore()

    def __tstPoly(self, painter, siz=15, num=10):
        x, y = self.xLeftMargin, self.y+90

        def poly(pts):
            return QtGui.QPolygonF(map(lambda p: QtCore.QPointF(*p), pts))
        xsiz = siz
        ysiz = int(siz/2)
        for i in range(num):
            pts = [[x, y], [x, y + ysiz], [x + xsiz, y + ysiz], [x + xsiz, y]]
            pts = pts[:]
            painter.drawPolyline(poly(pts))
            x += xsiz
        x = self.xLeftMargin
        painter.drawLine(QtCore.QPoint(x, y-3),
                         QtCore.QPoint(x + (num * xsiz), y - 3))
        print('height : {0}, width : {1}'.format(self.pageRect.height(),
                                                 self.pageRect.width()))
        painter.drawRect(self.xLeftMargin,
                         self.yTopMargin,
                         self.pageRect.width() - self.xLeftMargin - 36,
                         self.pageRect.height() - 2 * self.yTopMargin)

    def __drawReport(self):
        '''Here we assemble the pieces to make the final report'''
        painter = Qg.QPainter(self.printer)
        painter.save()
        self.pageRect = self.printer.pageRect()
        # initialize print Cursor
        self.xLeftMargin = self.x = 52
        self.yTopMargin = self.y = 30
        self.yFooter = self.pageRect.height() - 54
        self.pageNo = 1
        self.__drawReportHeader(painter)
        # self.__drawPageHeader()
        self.__fixPainterBug(painter)
        self.__drawPageFooter(painter)
        self.__drawTableHeader(painter)
        self.__drawTableLines(painter)
        # self.__tstPoly(painter)
        self.__drawTableFooter(painter)
        painter.restore()

    def printPreview(self):
        if self.f['pdfName']:
            self.printer.setOutputFormat(Qp.QPrinter.PdfFormat)
            self.printer.setOutputFileName(self.f['pdfName'])
        self.printer.setPaperSize(Qp.QPrinter.A4)
        self.printer.setFullPage(True)
        pp = Qp.QPrintPreviewDialog(self.printer)
        pp.paintRequested.connect(self.__drawReport)
        pp.exec_()

    def printPdf(self):
        if self.f['pdfName']:
            self.printer.setOutputFormat(Qp.QPrinter.PdfFormat)
            self.printer.setOutputFileName(self.f['pdfName'])
            self.printer.setPaperSize(Qp.QPrinter.A4)
            self.printer.setFullPage(True)
            self.__drawReport()
