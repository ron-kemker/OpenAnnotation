# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 20:44:47 2021

@author: Ronald Kemker

Description: This is a quick script to build a stand-alone application.

"""

import PyInstaller.__main__
import os, shutil

PyInstaller.__main__.run([
    'AnnotationTool.py',
    '--onefile',
    '-w']
    )

shutil.rmtree('build')
shutil.copytree('img', 'dist/img')
shutil.copytree('data', 'dist/data')
