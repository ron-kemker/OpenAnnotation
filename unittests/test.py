# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 09:06:03 2021

@author: Ronald Kemker
"""

import unittest

from AnnotationTool_test import TestAnnotationTool
from menu_test import TestMenu
from fileio_test import TestFileIO

if __name__ == '__main__':
    # Unit Tests
    TestAnnotationTool()
    TestMenu()
    TestFileIO()
    unittest.main()