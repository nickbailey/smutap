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

from uploader import Uploader
from widgets import MyListWidget, Separator
    
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
