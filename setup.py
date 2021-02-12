# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 15:21:25 2021

@author: Ronald Kemker
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
       
setuptools.setup(
    name="openannotation-ron-kemker", # Replace with your own username
    version="0.1.0",
    author="Ronald Kemker",
    author_email="rmkemker@mtu.edu",
    description="Open-Source Annotation Tool for Computer Vision Projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ron-kemker/OpenAnnotation",
    packages=['tkinter', 'PIL'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)