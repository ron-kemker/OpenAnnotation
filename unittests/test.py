# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 09:06:03 2021

@author: Ronald Kemker
"""

import unittest

from AnnotationTool_test import TestAnnotationTool
from menu_test import TestMenu
from toolbar_test import TestToolbar
from options_test  import TestOptionPrompt
from fileio_test import TestFileIO
from help_test import TestHelp
from objectclassmanager_test import TestObjectClassManager
from interactivebox_test import TestInteractiveBox
from project_wizard_test import TestProjectWizard
from navigator_test import TestNavigator

if __name__ == '__main__':
    # Unit Tests
    TestAnnotationTool()
    TestMenu()
    TestToolbar()
    TestOptionPrompt()
    TestFileIO()
    TestHelp()
    TestObjectClassManager()
    TestInteractiveBox()
    TestProjectWizard()
    TestNavigator()
    
    # TODO: Integration Testing
    
    # TODO: Functional Demo 
    
    unittest.main()