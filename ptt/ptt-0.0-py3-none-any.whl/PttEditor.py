#!/usr/bin/python3
import sys
import os
import subprocess
import pkg_resources
import time
import pttlib.paths
from pttlib import HelpAbout
from pttlib import Share
import io
from PyQt5.QtWidgets import QMainWindow, QListWidget, QListWidgetItem, QFileDialog, QInputDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap

class PttEditor(QMainWindow):
  def __init__(self, *args):
    self.loading = True
    super().__init__(*args)
    # Don't know how to do this correctly
    loadUi(io.BytesIO(pttlib.paths.getData("main.ui")),self)
    icon = QIcon() ; pixmap = QPixmap()
    pixmap.loadFromData(pttlib.paths.getData("icon.svg"))
    icon.addPixmap(pixmap)
    self.setWindowIcon(icon)
    self.pwd_edit.editingFinished.connect(self.set_pwd)
    self.open_folder_button.clicked.connect(self.set_pwd)
    self.subfolders_list.itemDoubleClicked.connect(self.traverse_subfolder)
    self.new_subfolder_edit.editingFinished.connect(self.mkdir)
    self.create_subfolder_button.clicked.connect(self.mkdir)
    self.delete_subfolder_button.clicked.connect(self.subfolders_list.delete_selected_folder)
    self.new_symlink_button.clicked.connect(self.new_symlink)
    self.help_button.clicked.connect(self.show_help_about)
    self.track_list.currentItemChanged.connect(self.play_track)
    self.track_list.itemPressed.connect(self.play_track)
    self.share_button.clicked.connect(self.share)
    self.last_player = None
    self.recorder = None
    # Holding down the space bar doesn't seem to be reliable.
    # It often releases and presses again in a short time.
    # So sadly, we have to do software debouncing. ! 
    # At such a high level!
    # WTF?
    # Perhaps this is because I'm using an unstable kernel.
    # I hope so.
    self.bounce_count = 0
    self.set_pwd(os.getcwd())
    self.current_recording_start_time = None
    self.current_recording_track_item = None
    self.loading = False

  def load_tracks(self):
    self.track_list.clear()
    self.just_started = True
    self.track_count = 0
    self.track_list.addItem("Click here and hold down the space bar to start recording.")
    try:
      with open("ptt.m3u","r") as playlist:
        if playlist.readline() != "#EXTM3U\n":
          sys.exit("ptt.m3u corrupted!")
        while True:
          line = playlist.readline()
          if line == "":
            break
          try:
            line = line[len("#EXTINF:"):]
          except IndexError:
            sys.exit("ptt.m3u corrupted!")
          line  = line.split(",", 1)[0]
          duration = int(line)
          line = playlist.readline()
          if line == "":
            sys.exit("ptt.m3u corrupted!")
          filename = line[:-1]
          item = self.new_track_list_item({"filename":filename,"duration":duration})
          self.track_list.addItem(item)
          self.track_count += 1
    except OSError:
      pass

  def format_track_item_text(self,data):
    return str(data["duration"]).rjust(5)+(" sec ["+"-"*data["duration"]+"]").ljust(40)+data["filename"].rjust(8)

  def new_track_list_item(self,data,text = None):
    if text is None:
      text = self.format_track_item_text(data)
    item = QListWidgetItem(text)
    item.setData(Qt.UserRole, data)
    return item

  def set_pwd(self,pwd=None):
    if pwd is None:
      pwd = self.pwd_edit.text()
    if not self.loading:
      self.save_title_and_description()
    os.chdir(pwd)
    self.pwd_edit.setText(pwd)
    self.reload_subfolders_list()
    self.load_tracks()
    self.load_title_and_description()

  def reload_subfolders_list(self):
    self.subfolders_list.clear()
    self.subfolders_list.addItem("..")
    for subfolder in os.listdir(os.getcwd()):
      if os.path.isdir(subfolder):
        self.subfolders_list.addItem(subfolder)

  def traverse_subfolder(self, cur):
    self.set_pwd(os.path.realpath(os.path.join(os.getcwd(),cur.text())))

  def mkdir(self):
    new_dir = self.new_subfolder_edit.text()
    if new_dir:
      os.mkdir(new_dir)
      self.new_subfolder_edit.setText("")
      self.reload_subfolders_list()
      self.set_pwd(os.path.join(os.getcwd(),new_dir))

  def new_symlink(self):
    abs_destination = QFileDialog.getExistingDirectory(
      self,
      "Choose destination",
      os.getcwd(),
      QFileDialog.ShowDirsOnly
      )
    link = os.path.basename(abs_destination)
    while os.path.exists(link):
      text, ok = QInputDialog.getText(self, 'Source exists', link+' exists in the current directory. Please choose a different name:')
      if ok:
        link = text
      else:
        return
    rel_destination = os.path.relpath(abs_destination)
    if os.name == "nt":
      import ctypes
      kdll = ctypes.windll.LoadLibrary("kernel32.dll")
      abs_link = os.path.join(os.getcwd(),link)
      kdll.CreateSymbolicLinkA(abs_destination, abs_link, 1)
    else:
      os.symlink(rel_destination,link)
    self.reload_subfolders_list()

  def play_track(self, cur, prev=None):
    if cur is None:
      return
    if self.last_player:
      self.last_player.terminate()
    if not self.just_started and cur.listWidget().row(cur) > 0:
      self.last_player = subprocess.Popen(["sox",cur.data(Qt.UserRole)["filename"],"-d","--buffer","512"])
    self.just_started = False

  def keyPressEvent(self, key_event):
    if key_event.isAutoRepeat():
        return
    if key_event.key() == Qt.Key_Space:
      self.bounce_count += 1
      if self.recorder is not None:
        return
      # Start recording
      if self.last_player:
        self.last_player.terminate()
      self.last_player = None
      self.track_count += 1
      file_name = str(self.track_count)+".ogg"
      while os.path.exists(file_name):
        self.track_count += 1
        file_name = str(self.track_count)+".ogg"
      self.recorder = subprocess.Popen(["sox","-d",file_name])
      item_data = {"filename":file_name,"duration": 0}
      item = self.new_track_list_item(item_data,text="Recording ...")
      self.track_list.insertItem(self.track_list.currentRow() + 1, item)
      self.track_list.setCurrentRow(self.track_list.currentRow() + 1)
      self.current_recording_track_item = item
      self.current_recording_start_time = time.time()
    elif key_event.key() == Qt.Key_F2:
      self.subfolders_list.setFocus()
      self.subfolders_list.setCurrentRow(0)
    elif key_event.key() == Qt.Key_F3:
      self.tabWidget.setCurrentWidget(self.audio_tab)
      self.track_list.setFocus()
      self.track_list.setCurrentRow(0)
    else:
      super().keyPressEvent(key_event)

  def keyReleaseEvent(self, key_event):
    if key_event.isAutoRepeat():
        return
    if key_event.key() == Qt.Key_Space:
      QTimer.singleShot(300,self.end_recording)
      self.bounce_count -= 1
    else:
      super().keyReleaseEvent(key_event)

  def save_playlist(self):
    with open("ptt.m3u","w") as playlist:
      playlist.write("#EXTM3U\n")
      index = 1
      while index < self.track_list.count():
        track_data = self.track_list.item(index).data(Qt.UserRole)
        path = track_data["filename"]
        playlist.write("#EXTINF:"+str(track_data["duration"])+","+path+"\n")
        playlist.write(path+"\n")
        index += 1

  def end_recording(self):
    # End recording
    if self.recorder and self.bounce_count < 1:
      self.bounce_count = 0
      self.recorder.terminate()
      self.recorder = None
      data = self.current_recording_track_item.data(Qt.UserRole)
      data["duration"] = int(time.time()-self.current_recording_start_time)
      self.current_recording_track_item.setData(Qt.UserRole,data)
      self.current_recording_track_item.setText(self.format_track_item_text(self.current_recording_track_item.data(Qt.UserRole)))
      self.save_playlist()

  def load_title_and_description(self):
    try:
      with open("TITLE","r") as title_fd:
        title = title_fd.read()
    except FileNotFoundError:
      title = ""
    self.title_edit.setText(title)
    try:
      with open("DESCRIPTION.html","r") as description_fd:
        description = description_fd.read()
    except FileNotFoundError:
      description = ""
    self.description_edit.setHtml(description)

  def save_title_and_description(self):
    title = self.title_edit.text()
    if title:
      with open("TITLE","w") as title_fd:
        title_fd.write(title)
    elif os.path.exists("TITLE"):
      os.remove("TITLE")
    description = self.description_edit.toHtml()
    if self.description_edit.toPlainText():
      with open("DESCRIPTION.html","w") as description_fd:
        description_fd.write(description)
    elif os.path.exists("DESCRIPTION.html"):
      os.remove("DESCRIPTION.html")

  def share(self):
    if os.path.exists("ptt.m3u"):
      if self.title_edit.text():
        self.save_title_and_description()
        Share.Share(self).show()
      else:
        self.tabWidget.setCurrentWidget(self.text_tab)
        self.title_edit.setFocus()
        QMessageBox.information(self,"Set a title before sharing...","You need to give your story a title before you can share it.") 
    else:
      QMessageBox.warning(self,"Nothing to share.","You haven't recorded anything to share yet. Record something first!") 

  def closeEvent(self,event):
    self.save_title_and_description()
    super().closeEvent(event)

  def show_help_about(self):
    HelpAbout.HelpAbout(self).show()
