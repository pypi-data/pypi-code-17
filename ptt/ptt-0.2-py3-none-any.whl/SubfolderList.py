import os
import shutil
from PyQt5.QtWidgets import QListWidget, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

class SubfolderList(QListWidget):
  def __init__(self, parent):
     super().__init__(parent)

  def keyPressEvent(self, key_event):
    if key_event.key() == Qt.Key_Return or key_event.key() == Qt.Key_Enter:
      self.window().traverse_subfolder(self.currentItem())
    if key_event.key() == Qt.Key_Delete:
      self.delete_selected_folder()
    else:
      super().keyPressEvent(key_event)

  def delete_selected_folder(self):
    folder = self.currentItem().text()
    reply = QMessageBox.question(self,"Delete folder","Are you shure you want to delete '"+folder+"'?")
    if reply == QMessageBox.Yes:
      try:
        if os.path.islink(folder):
          os.remove(folder)
        else:
          shutil.rmtree(folder)
      except OSError as e:
        QMessageBox.warning(self,"Deletion failed.","Failed to delete "+folder+".\n"+str(e))
        return
      self.takeItem(self.currentRow())
