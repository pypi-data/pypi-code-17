# -*- coding: utf-8 -*-
'''
Created on 3 Mar 2013

@author: tedlaz
'''
import sys
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import rpt_tbl as tr


class testprn1(Qw.QDialog):
    def __init__(self):
        Qw.QDialog.__init__(self)
        self.setAttribute(Qc.Qt.WA_DeleteOnClose)
        dt = [[u'       ΈΣΟΔΑ', 0, 0, 0, 0, 0, 0],
              [u'Πωλ.Πρ/ντ.Χονδρικές', 955, 181.45, 4050, 769.5, 5005, 950.95],
              [u'Σύνολα εσόδων κεντρικού', 955, 181.45, 4050, 769.5, 5005,
               950.95],
              [u'Γενικό Σύνολο εσόδων', 955, 181.45, 4050, 769.5, 5005,
               950.95],
              [u'', 0, 0, 0, 0, 0, 0],
              [u'       ΈΞΟΔΑ', 0, 0, 0, 0, 0, 0],
              [u'Αγορές Α Υλών', 1573.73, 0, 19743.77, 0, 21317.5, 0],
              [u'Αγορές παγίων', 366.94, 69.71, 121.9, 23.16, 488.84, 92.87],
              [u'Γεν.Εξοδα ΧΔΕΦ', 129.6, 0, 4, 0, 133.6, 0],
              [u'Γεν.Εξ.ΜΔΕΦ', 1055.33, 200.55, 4170.93, 785.71, 5226.26,
               986.26],
              [u'Ενοίκια', 3470.4, 0, 500, 0, 3970.4, 0],
              [u'Σύνολο εξόδων κεντρικού', 955, 181.45, 4050, 769.5, 5005,
               950.95],
              [u'Γενικό σύνολα εξόδων', 955, 181.45, 4050, 769.5, 5005,
               950.95],
              ]
        f = {'orientation': 0,
             'pdfName': 'test.pdf',
             'fontFamily': 'Helvetica',
             'ReportHeader1': u'Μηνιαία κατάσταση εσόδων-εξόδων',
             'ReportHeader2': u'Περίοδος : Μάρτιος 2012',
             'ReportHeader3': u'',
             'headerLabels': [u'Τύπος', u'Από μεταφορά', u'ΦΠΑ', u'Περίοδος',
                              u'ΦΠΑ', u'Σε μεταφορά', u'ΦΠΑ'],
             'columnSizes': [25, 8, 8, 8, 8, 8, 8],
             'columnToSum': [0, 0, 0, 0, 0, 0, 0],
             'columnTypes': [0, 2, 2, 2, 2, 2, 2],
             'columnAlign': [0, 2, 2, 2, 2, 2, 2],
             'footerLine': True,
             'footerText': u'This is a footer text for testing',
             'footerPageNumberText': u'Σελίδα',
             'data': dt * 5
             }
        self.rep = tr.qtTableReport(f)
        tstButton = Qw.QPushButton('test')
        tstButton.clicked.connect(self.onClick)
        layout = Qw.QHBoxLayout()
        layout.addWidget(tstButton)
        self.setLayout(layout)
        # self.onClick()

    def onClick(self):
        self.rep.printPreview()
        # self.accept()

if __name__ == '__main__':
    app = Qw.QApplication(sys.argv)
    window = testprn1()
    window.show()
    sys.exit(app.exec_())
