import os
import io
import pttlib.paths
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

class HelpAbout(QDialog):
   def __init__(self, parent):
      super().__init__(parent)
      loadUi(io.BytesIO(pttlib.paths.getData("help_about.ui")),self)
      self.help_text.document().setHtml(self.help_text.document().toHtml().replace("$VERSION",pttlib.paths.getData("VERSION").decode("utf-8")))
