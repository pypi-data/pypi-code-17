from PyQt5.QtWidgets import QLineEdit

class NewSubfolderEdit(QLineEdit):
  def __init__(self, parent):
     super().__init__(parent)
     self.initialized = False

  def focusInEvent(self,event):
    if not self.initialized:
      self.setText("")
      self.initialized = True
    super().focusInEvent(event)
