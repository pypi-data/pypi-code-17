from PyQt4.QtGui import QApplication
from raipy.GUI import GUIWindow
import sys

def exe():
    app = QApplication(sys.argv)
    ex=GUIWindow()
    sys.exit(app.exec_())