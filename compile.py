# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 20:44:47 2021

@author: Ronald Kemker
"""

import PyInstaller.__main__
import os, shutil


install_path = ''


PyInstaller.__main__.run([
    'AnnotationTool.py',
    '--onefile',
    '-w']
    )

shutil.rmtree('build')
shutil.copytree('img', 'dist/img')
