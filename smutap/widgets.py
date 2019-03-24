#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 17:33:34 2019

@author: nick
"""

from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QShortcut, QFrame

"""A QListWidget with multiple selection enabled onto which
audio files for uploading can be dragged. Additionally,
pressing [del] when the widget has focus calls its
deleteSelected method to remove items from the list"""
class MyListWidget(QListWidget):
  def __init__(self, parent=None):
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
