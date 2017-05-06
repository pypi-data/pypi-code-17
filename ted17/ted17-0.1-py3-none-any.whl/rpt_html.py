# -*- coding: utf-8 -*-
'''
Created on 5 Μαρ 2013
Updated on 26 Mar 2017
@author: tedlaz
'''
import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtPrintSupport as Qp


class Window(Qw.QWidget):
    def __init__(self, template, value_array, pdf_name):
        Qw.QWidget.__init__(self)
        self.pdf_name = pdf_name
        self.setWindowTitle(self.tr('Document Printer'))
        self.editor = Qw.QTextEdit(self)
        self.editor.setFont(Qg.QFont('Times New Roman', 10))
        self.editor.textChanged.connect(self.handleTextChanged)
        self.buttonOpen = Qw.QPushButton('Open', self)
        self.buttonOpen.clicked.connect(self.handleOpen)
        self.buttonPrint = Qw.QPushButton('Print', self)
        self.buttonPrint.clicked.connect(self.tstPrintPdf)
        self.buttonPreview = Qw.QPushButton('Preview', self)
        self.buttonPreview.clicked.connect(self.handlePreview)

        layout = Qw.QGridLayout(self)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        layout.addWidget(self.buttonOpen, 1, 0)
        layout.addWidget(self.buttonPrint, 1, 1)
        layout.addWidget(self.buttonPreview, 1, 2)
        self.handleTextChanged()
        final_text = u''
        pages = len(value_array)
        for i, row_dict in enumerate(value_array):
            final_text += template.format(**row_dict)
            newpage = "<p style='page-break-after:always;'>"
            final_line = (newpage if i+1 < pages else "<p>")
            final_text += final_line
        self.editor.setHtml(final_text)

    def handleOpen(self):
        path = Qw.QFileDialog.getOpenFileName(
            self, self.tr('Open file'), '',
            self.tr('HTML files (*.html);;Text files (*.txt)'))
        if not path[0]:
            stream = Qc.QFile(path)
            if stream.open(Qc.QIODevice.ReadOnly):
                info = Qc.QFileInfo(path)
                text = stream.readAll()
                codec = Qc.QTextCodec.codecForHtml(text)
                unistr = codec.toUnicode(text)
                if info.completeSuffix() == 'html':
                    self.editor.setHtml(unistr)
                else:
                    self.editor.setPlainText(unistr)
            stream.close()

    def handlePrint(self):
        dialog = Qp.QPrintDialog()
        if dialog.exec_() == Qg.QDialog.Accepted:
            self.editor.document().print_(dialog.printer())

    def tstPrintPdf(self):
        fname = Qw.QFileDialog.getSaveFileName(self, u"%Αποθήκευση ως",
                                               self.pdf_name,
                                               u"Αρχείο (*.pdf)")
        print(fname)
        printer = Qp.QPrinter()
        printer.setOutputFormat(Qp.QPrinter.PdfFormat)
        printer.setOutputFileName(fname[0])
        self.editor.document().print_(printer)

    def saveAsOdt(self):
        doc = Qg.QTextDocument()
        cursor = Qg.QTextCursor(doc)
        cursor.insertHtml(self.editor.toHtml())
        writer = Qg.QTextDocumentWriter()
        odf_format = writer.supportedDocumentFormats()[1]
        writer.setFormat(odf_format)
        writer.setFileName('symbaseis.odt')
        writer.write(doc)

    def handlePreview(self):
        dialog = Qp.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()

    def handleTextChanged(self):
        enable = not self.editor.document().isEmpty()
        self.buttonPrint.setEnabled(enable)
        self.buttonPreview.setEnabled(enable)


if __name__ == '__main__':
    txt_html = u'''
<p><center><span style=" font-size:14pt; text-decoration: underline;">
 <b>ΕΚΚΑΘΑΡΙΣΗ ΑΠΟΔΟΧΩΝ & ΑΠΟΔΕΙΞΗ ΠΛΗΡΩΜΗΣ</b></span></center><p>
Περίοδος : {period}<br>
Τύπος : {typos}<br>
<p><span style=" font-size:12pt;"><b>Στοιχεία Επιχείρησης</b></span><br>
Επωνυμία : <i>{co_epon}</i><br>
ΑΦΜ : {co_afm}<br>
Δραστηριότητα : {co_dra}<br>
Διεύθυνση : {co_addr}<br>
</p>
<p><span style=" font-size:12pt;"><b>Στοιχεία Εργαζομένου</b></span><br>
Ονοματεπώνυμο : {erg_onomatep}<br>
Όνομα Πατρός : {erg_pateras}<br>
ΑΦΜ : {erg_afm}<br>
Ειδικότητα εργασίας : {erg_eid}
</p><br>
<table width="100%" border="1" cellpadding="4" cellspacing="0">
  <tbody>
      <tr>
      <td colspan=2><center><b>ΑΝΑΛΥΣΗ ΑΠΟΔΟΧΩΝ</b></center></td>
      <td colspan=2><center><b>ΚΡΑΤΗΣΕΙΣ<b></center></td>
    </tr>
    <tr>
      <td>Ημερομίσθιο/ Μισθός</td>
      <td align="right">{misthos}</td>
      <td>1. ΙΚΑ</td>
      <td align="right">{ika}</td>
    </tr>
    <tr>
      <td>Μέρες εργασίας</td>
      <td align="right">{meres}</td>
      <td>2. Φόρος Μισθωτών Υπηρεσιών</center></td>
      <td align="right">{foros}</td>
    </tr>
    <tr>
      <td>Ακαθάριστες αποδοχές</td>
      <td align="right">{apod}</td>
      <td>3. Επίδομα Αλληλεγγύης</td>
      <td align="right">{epid}</td>
    </tr>
    <tr>
      <td>Λοιπές αποδοχές</td>
      <td align="right">{loipa}</td>
    </tr>
    <tr>
      <td><center>(Α) Σύνολο αποδοχών</center></td>
      <td align="right"><b>{apod_total}</b></td>
    </tr>
     <tr>
      <td><center>Μείον: (Β) Σύνολο κρατήσεων</center></td>
      <td align="right"><b>{kratiseis}</b></td>
    </tr>
     <tr>
      <td><center>Υπόλοιπο Πληρωτέο (Α - Β)</center></td>
      <td align="right"><b>{ypoloipo}</b></td>
      <td><center>(Β) Σύνολο κρατήσεων</center></td>
      <td align="right"><b>{kratiseis}</b></td>
    </tr>
    </tbody>
</table>
<p>Ο/Η υπογράφων/υπογράφουσα {erg_onomatep},  δηλώνω ότι η παρούσα αποτελεί
πλήρη εξώφληση των αποδοχών μου και καμία άλλη απαίτηση έχω από την παραπάνω
επιχείρηση για οποιαδήποτε άλλη αιτία μέχρι σήμερα.</p>
<br>
<table width="100%" border="0" cellpadding="2" cellspacing="2">
  <tbody>
      <tr>
      <td><center>    </center></td>
      <td><center>{imnia}</center></td>
    </tr>
    <tr>
      <td><center>    </center></td>
      <td><center>(Υπογραφή εργαζομένου)</center></td>
    </tr>
  </tbody>
</table>
'''
    f1 = {'period': u'Ιανουάριος 2015', 'typos': u'Μισθοδοσία Περιόδου',
          'co_epon': u'Μαλακόπουλος ΕΠΕ', 'co_afm': '044444565',
          'co_dra': u'Υπηρεσίες εστίασης',
          'co_addr': u'Αργεντινής 38 14434, Αθήνα',
          'erg_onomatep': u'Θεόδωρος Μαρκόπουλος', 'erg_pateras': u'Γεράσιμος',
          'erg_afm': '044564112', 'erg_eid': u'Μάγειρας',
          'misthos': '50,00', 'meres': '10',
          'apod': '1.000,35', 'loipa': '0,00',
          'apod_total': '100,35', 'kratiseis': '20,00',
          'ypoloipo': '0,00', 'ika': '112,41',
          'foros': '0,00', 'epid': '0,00',
          'kratiseis': '12,41', 'imnia': u'Αθήνα 15/3/2015',
          }
    import sys
    app = Qw.QApplication(sys.argv)
    window = Window(txt_html, [f1, f1, f1, f1], 'file1.pdf')
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
    # print num2descr(4949901945689)
