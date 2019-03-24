#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 17:02:08 2019

@author: nick
"""

import unittest

import uploader
import widgets

import PyQt5.QtWidgets
        

class TestUploader(unittest.TestCase):
    
    def test_instantiation(self):
        ul = widgets.MyListWidget()
        self.assertNotEqual(uploader.Uploader(ul), None)
    
    def setUp(self):
        self.app = PyQt5.QtWidgets.QApplication(['test_uploader'])

if __name__ == '__main__':
    unittest.main()
