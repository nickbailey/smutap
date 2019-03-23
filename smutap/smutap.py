#!/usr/bin/python3

import os

"""End-user configuration"""
# Where the music is (needs trailing '/')
mediaSource = '/auto/hamlet/media/Audio/'
# Where the music goes (use USERNAME in Windoze)
mediaTarget = '/media/' + os.getenv('USER') + '/WALKMAN/MUSIC/'
# Rules to convert media types. Inoput from source, output to target
rules = {
        'audio/flac': 'ffmpeg -i {source} -codec:a libmp3lame -qscale:a 2 -map_metadata 0 {target}',
        'audio/mp3':  'cat {source} > {target}'
        }

import sys
import mimetypes
import subprocess
from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot, QUrl, QSignalMapper
from PyQt5.QtGui import QKeySequence, QDesktopServices
from PyQt5.QtWidgets import QApplication, QWidget, \
  QHBoxLayout, QVBoxLayout, \
  QListWidget, QAbstractItemView, QShortcut, \
  QPushButton, \
  QLabel, QFrame

"""Upload a file to the media player given the file path"""
# Useful links:
#   https://askubuntu.com/a/178991
class Uploader(QWidget):

  def __init__(self, sourcesList, parent=None):
    super(Uploader, self).__init__(parent)
    self.sList = sourcesList
    
  """Remove p from the beginning of s if it's there"""
  @staticmethod
  def stripPrefix(s, p):
    return s[len(p):] if s.startswith(p) else s

  """Deal with single quotes in strings which are going to be single-quoted"""
  @staticmethod
  def escSQuote(s):
      return "\\'".join("'" + p + "'" for p in s.split("'"))

  @pyqtSlot()
  def uploadMedia(self):
    maxItemNameLen = 65
    
    currentItem = 0
    for i in range(len(self.sList)):
      item = self.sList.item(currentItem).text()
      mimetype = mimetypes.guess_type(self.sList.item(currentItem).text())[0]
      print('{}{}: {}'.format(
              '...' if len(item) > maxItemNameLen else '',
              item[maxItemNameLen:],
              mimetype
      ))
      
      # Path within target is the sourced path with the mediaSource
      # or home directory (as appropraite) stripped off
      targetPath = Uploader.stripPrefix(item, mediaSource)
      targetPath = Uploader.stripPrefix(targetPath, os.getenv('HOME')+'/')
      
      # Not allowed \ in DOS names, so get rid of them now.
      # Can't do it later: we'll be escaping single quotes.
      targetPath = targetPath.replace('\\', '')
      
      # Change or add an extension
      targetPath = os.path.splitext(mediaTarget + targetPath)[0]+'.mp3'
      
       # Remove characters not allowed in DOS filesystems
      targetPath = targetPath.translate({ord(c): None for c in ':*"<>|'})
      
      # Fix any single quotes in the path
      targetDir = Uploader.escSQuote(os.path.dirname(targetPath))
      targetPath = Uploader.escSQuote(targetPath)
      
     
      print("Need to create "+targetDir)
      print ("source is {}. target is {}".format(mediaSource,targetPath))
      command = rules[mimetype].format(
              source = Uploader.escSQuote(item),
              target = targetPath
      )
      
      result = subprocess.call(
              'mkdir -p {} && {}'.format(targetDir, command),
              shell = True
      )
      
      print (command)
      print ('Returned {}\n'.format(result))
      
      if (result == 0):
        self.sList.takeItem(currentItem)
      else:
        self.sList.item(currentItem).setForeground(Qt.red)
        currentItem += 1
        

"""A QListWidget with multiple selection enabled onto which
audio files for uploading can be dragged. Additionally,
pressing [del] when the widget has focus calls its
deleteSelected method to remove items from the list"""
class MyListWidget(QListWidget):
  def __init__(self, parent):
    super(MyListWidget, self).__init__(parent)
    self.setAcceptDrops(True)
    self.setDragDropMode(QAbstractItemView.InternalMove)
    self.setSelectionMode(QAbstractItemView.MultiSelection)
    
    self.deleteShortcut = QShortcut(QKeySequence(Qt.Key_Delete), self)
    self.deleteShortcut.activated.connect(self.deleteSelected);

  def dragEnterEvent(self, event):
    if event.mimeData().hasUrls():
      event.acceptProposedAction()
    else:
      super(MyListWidget, self).dragEnterEvent(event)

  def dragMoveEvent(self, event):
    super(MyListWidget, self).dragMoveEvent(event)

  def dropEvent(self, event):
    if event.mimeData().hasUrls():
      for url in event.mimeData().urls():
        # TODO: check whether the paths are directories and if so recursively
        # add allowed audio file formats contained in them.
        self.addItem(url.path())
      event.acceptProposedAction()
    else:
      super(MyListWidget,self).dropEvent(event)
  
  @pyqtSlot()
  def deleteSelected(self):
    # In C++ you can just delete an item, but not in Python...
    for item in self.selectedItems():
      self.takeItem(self.row(item))

"""A pretty separator to make BoxLayouts look nice"""
class Separator(QFrame):
  def __init__(self, parent):
    super(Separator, self).__init__(parent)
    self.setFrameShape(QFrame.HLine);
    self.setFrameShadow(QFrame.Sunken);
    
"""Construct the main GUI window. Printing all the files
that have been dropped on it happen when the doPrinting method
is invoked. As jobs are successfully submitted for printing,
they are removed from the list, but see notes about error detection
below"""
class MyWindow(QWidget):
      
  def __init__(self):
    super(MyWindow,self).__init__()
    self.setGeometry(100,100,600,400)
    self.setWindowTitle("Send to Player")

    self.list = MyListWidget(self)
    self.uploader = Uploader(self.list, self)

    layout = QHBoxLayout(self)
    layout.addWidget(self.list)
    
    self.browserMapper = QSignalMapper()
    self.openSourceButton = QPushButton('&Open Music Archive')
    self.openSourceButton.released.connect(self.browserMapper.map)
    self.browserMapper.setMapping(self.openSourceButton, mediaSource)
    self.openTargetButton = QPushButton('Open &Player')
    self.openTargetButton.released.connect(self.browserMapper.map)
    self.browserMapper.setMapping(self.openTargetButton, mediaTarget)
    self.browserMapper.mapped[str].connect(
            lambda b: QDesktopServices.openUrl(QUrl(b))
    )
    
    self.submitButton = QPushButton('&Send to Player')
    self.submitButton.released.connect(self.uploader.uploadMedia)
    self.deleteSelectedButton = QPushButton('&Delete\nSelected')
    self.deleteSelectedButton.released.connect(self.list.deleteSelected)
    
    controls = QVBoxLayout()
    controls.addWidget(QLabel('Filesystem Browsers'))
    controls.addWidget(self.openSourceButton)
    controls.addWidget(self.openTargetButton)
    controls.addWidget(Separator(self))
    controls.addWidget(self.deleteSelectedButton)
    controls.addWidget(Separator(self))
    controls.addStretch()
    controls.addWidget(self.submitButton);

    layout.addLayout(controls)
    
    self.setLayout(layout)

    
if __name__ == '__main__':

  app = QApplication(sys.argv)
  #app.setStyle("plastique")

  window = MyWindow()
  window.show()
  
  #QDesktopServices.openUrl(QUrl(mediaSource))
  #QDesktopServices.openUrl(QUrl(mediaTarget))

  sys.exit(app.exec_())
