#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 18:05:59 2019

@author: nick
"""

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

