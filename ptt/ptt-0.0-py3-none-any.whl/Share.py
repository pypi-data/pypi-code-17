import os
import io
import zipfile
import shutil
import subprocess
import requests

from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5.QtGui import QDesktopServices

import pttlib.paths
from pttlib import IPFSDag

class Share(QDialog):
  def __init__(self, parent):
    super().__init__(parent)
    loadUi(io.BytesIO(pttlib.paths.getData("share.ui")),self)
    self.export_html_button.clicked.connect(self.export_html_and_open)
    self.export_zip_button.clicked.connect(self.export_zip)
    self.zip_save_as_button.clicked.connect(self.save_zip_as)
    self.publish_online_button.clicked.connect(self.publish_online)
    self.exported_html = False
    self.exported_zip = False
    self.published_online = False

  def export_html(self):
    with open("story.html","w") as story_fd:
      story_template = pttlib.paths.getData("story.html").decode("utf-8")
      story = story_template.replace("%%TITLE",self.parent().title_edit.text())
      story = story.replace("%%DESCRIPTION",self.parent().description_edit.toHtml())
      with open("ptt.m3u","r") as m3u_fd:
        story = story.replace("%%M3U",m3u_fd.read())
      story_fd.write(story) 
    self.exported_html = True

  def export_html_and_open(self):
    self.export_html()
    QDesktopServices.openUrl(QUrl(os.path.join(os.getcwd(),"story.html")))

  @property
  def tracks(self):
    tracks = []
    for index in range(1,self.parent().track_list.count()):
      tracks.append(self.parent().track_list.item(index).data(Qt.UserRole))
    return tracks

  def export_zip(self,cont = None):
    if not self.exported_html:
      self.export_html()
    self.setEnabled(False)
    self.zip_progress_bar.setMaximum(len(self.tracks)-1)
    zipper = Zipper(self,self.tracks)
    zipper.status.connect(self.zip_progress_bar.setFormat)
    zipper.progress.connect(self.zip_progress_bar.setValue)
    def endZip(path):
      self.saved_to_label.setText("Saved to:")
      self.zip_path.setText(path)
      if cont:
        cont()
      else:
        self.setEnabled(True)
      self.exported_zip = True
    zipper.final_location.connect(endZip)
    zipper.start()

  def save_zip_as(self):
    if not self.exported_zip:
      self.export_zip()
    new_path,ok = QFileDialog.getSaveFileName(self, "Save story.zip as", "", ".zip")
    if ok:
      shutil.copyfile("story.zip",new_path)
      self.zip_path.setText(new_path)

  def publish_online(self):
    self.setEnabled(False)
    self.scrollArea.ensureWidgetVisible(self.url_label)
    self.publish_progress_bar.setFormat("Zipping... Please wait.")
    ipfs = IPFSDag.IPFSDag(gateway=self.server_combo_box.currentText())
    def cont():
      self.publish_progress_bar.setMaximum(len(self.tracks)-1)
      publisher = Publisher(self,self.tracks,ipfs)
      def connection_error(error):
        QMessageBox.warning(self,"Connection error.","Failed to connect to "+ipfs.gateway+"\n"+error)
        self.setEnabled(True)
      def end_publishing(url):
        self.url_label.setText("<a href=\""+url+"\">Open in browser.</a>");
        self.setEnabled(True)
        QDesktopServices.openUrl(QUrl(url))
        self.published_online = True
      publisher.connection_error.connect(connection_error)
      publisher.final_location.connect(end_publishing)
      publisher.progress.connect(self.publish_progress_bar.setValue)
      publisher.status.connect(self.publish_progress_bar.setFormat)
      publisher.start()
    if not self.exported_zip:
      self.export_zip(cont)
    else:
      cont()

# Thanks to http://stackoverflow.com/questions/10694971/pyqt-update-gui for help with threading...

class Zipper(QThread):
  status = pyqtSignal(str)
  progress = pyqtSignal(int)
  final_location = pyqtSignal(str)

  def __init__(self, parent, tracks):
    super().__init__(parent)
    self.tracks = tracks

  def run(self):
    with zipfile.ZipFile('story.zip', 'w') as zip:
      zip.write('story.html',os.path.join("story","story.html"))
      for index, track in enumerate(self.tracks):
        zip.write(track["filename"],os.path.join("story",track["filename"]))
        self.progress.emit(index)
        self.status.emit(track["filename"])
    self.status.emit("Done.")
    self.final_location.emit(os.path.join(os.getcwd(),"story.zip"))

class Publisher(QThread):
  status = pyqtSignal(str)
  progress = pyqtSignal(int)
  final_location = pyqtSignal(str)
  connection_error = pyqtSignal(str)

  def __init__(self, parent, tracks,ipfs):
    super().__init__(parent)
    self.tracks = tracks
    self.ipfs = ipfs

  def run(self):
    try:
      self.status.emit("Ensuring IPFS daemon is running... Please wait.")
      ipfsDaemon = subprocess.Popen(["ipfs","daemon"],stdout=subprocess.PIPE) # Launch ipfs daemon if not running.
      if ipfsDaemon.stdout.readline().decode().strip() == "Initializing daemon...":
        while True:
          if ipfsDaemon.stdout.readline().decode().strip() == "Daemon is ready":
            break
      def add_file(file):
        self.status.emit("Uploading: "+file)
        self.ipfs.add(file)
      add_file("story.html")
      add_file("story.zip")
      for index,track in enumerate(self.tracks):
        self.progress.emit(index)
        add_file(track["filename"])
      self.ipfs.push_to_gateway() # This *should* be fast, because all of the files have aready been pushed.
      self.status.emit("Done.")
      url = self.ipfs.get_url()
      ipfsDaemon.terminate() # This will only terminate the daemon if WE started it.
      self.final_location.emit(url)
    except requests.exceptions.ConnectionError as ce:
      ipfsDaemon.terminate() # This will only terminate the daemon if WE started it.
      self.connection_error.emit(str(ce))
