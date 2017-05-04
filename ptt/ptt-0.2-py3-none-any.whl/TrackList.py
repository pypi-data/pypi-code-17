import os
from PyQt5.QtWidgets import QListWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

class TrackList(QListWidget):
   def __init__(self, parent):
      super().__init__(parent)

   def keyPressEvent(self, key_event):
     if key_event.key() == Qt.Key_Space:
       self.parent().keyPressEvent(key_event)
     elif key_event.key() == Qt.Key_Return or key_event.key() == Qt.Key_Enter:
       self.window().play_track(self.currentItem())
     elif key_event.key() == Qt.Key_Delete or key_event.key() == Qt.Key_D:
       if self.currentRow() == 0:
         return
       cur = self.currentItem()
       file = cur.data(Qt.UserRole)["filename"]
       if os.path.exists(file):
         os.remove(file)
       self.takeItem(self.currentRow())
       if not self.currentRow() == self.count() - 1:
         self.setCurrentRow(self.currentRow() - 1)
       self.window().save_playlist()
     elif (key_event.key() == Qt.Key_J or key_event.key() == Qt.Key_Down) and key_event.modifiers() & Qt.ControlModifier:
       row = self.currentRow()
       if row == 0:
         return
       row += 1
       item = self.takeItem(self.currentRow())
       self.insertItem(row,item)
       self.setCurrentRow(row)
       self.window().save_playlist()
     elif (key_event.key() == Qt.Key_K or key_event.key() == Qt.Key_Up) and key_event.modifiers() & Qt.ControlModifier:
       row = self.currentRow()
       if row < 2:
         return
       row -= 1
       item = self.takeItem(self.currentRow())
       self.insertItem(row,item)
       self.setCurrentRow(row)
       self.window().save_playlist()
     elif key_event.key() == Qt.Key_J:
       newRow = self.currentRow() + 1
       if newRow >= self.count():
         return
       self.setCurrentRow(newRow)
     elif key_event.key() == Qt.Key_K:
       self.setCurrentRow(self.currentRow() - 1)
     elif key_event.key() == Qt.Key_Escape:
       self.window().stop_playing()
     else:
       super().keyPressEvent(key_event)
