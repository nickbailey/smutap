#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 18:47:56 2019

@author: nick
"""

from distutils.core import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='smutap',
    version='0.1.0',
    author='Nick Bailey',
    author_email='nickbailey@github.com',
    packages=['smutap'], #, 'smutap.test'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE',
    description='Send MUsic To an Audio Player',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
)