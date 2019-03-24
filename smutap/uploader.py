#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 17:11:22 2019

@author: nick
"""

import config

import mimetypes, os, subprocess
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import Qt

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
      targetPath = Uploader.stripPrefix(item, config.mediaSource)
      targetPath = Uploader.stripPrefix(targetPath, os.getenv('HOME')+'/')
      
      # Not allowed \ in DOS names, so get rid of them now.
      # Can't do it later: we'll be escaping single quotes.
      targetPath = targetPath.replace('\\', '')
      
      # Change or add an extension
      targetPath = os.path.splitext(config.mediaTarget + targetPath)[0]+'.mp3'
      
       # Remove characters not allowed in DOS filesystems
      targetPath = targetPath.translate({ord(c): None for c in ':*"<>|'})
      
      # Fix any single quotes in the path
      targetDir = Uploader.escSQuote(os.path.dirname(targetPath))
      targetPath = Uploader.escSQuote(targetPath)
      
     
      print("Need to create "+targetDir)
      print ("source is {}. target is {}".format(config.mediaSource,
                                                 targetPath))
      command = config.rules[mimetype].format(
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
        
