# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as Qw


class Text(Qw.QTextEdit):

    """
    Text field
    """

    def __init__(self, val='', parent=None):
        super().__init__(parent)

        self.set(val)

    def set(self, txt):
        """Set value

        :param txt: value to set
        """
        if txt:
            ttxt = '%s' % txt
            self.setText(ttxt.strip())
        else:
            self.setText('')

    def get(self):
        """Get value

        :return: Text value of control
        """
        tmpval = '%s' % self.toPlainText().replace("'", "''")
        return tmpval.strip()
