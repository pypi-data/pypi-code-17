from PyQt5.QtWidgets import QApplication
import sys
from raipy.GUI import GUIWindow

def exe():
    app = QApplication(sys.argv)
    ex=GUIWindow()
    sys.exit(app.exec_())