# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:48:56 2021

@author: Master
"""

import unittest, time, sys
from  AnnotationTool import AnnotationTool
from menu import AppMenu, Annotation

class Event(object):
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class TestAnnotationTool(unittest.TestCase):
    
    def test_init(self):

        tool = AnnotationTool()
        
        # Initial List Objects
        self.assertListEqual(tool.file_ext, ['.jpg', '.png'])
        self.assertListEqual(tool.top_colors, ['#0000FF', '#FF0000','#00FF00',
                                               '#00FFFF','#FF00FF', '#FFFF00'])
        
        # Initial Boolean Objects
        self.assertTrue(tool.saved)
        self.assertFalse(tool.project_open)
        
        # Initial Numerical Objects
        self.assertEqual(tool.window_width, 1024)
        self.assertEqual(tool.window_height, 768)
        self.assertEqual(tool.toolbar_width, 150)
        self.assertEqual(tool.footer_height, 25)
        self.assertEqual(tool.canvas_width, 874)
        self.assertEqual(tool.canvas_height, 743)

        # Make sure Appmenu has correct "root_app"
        self.assertEqual(tool, tool.app_menu.root_app)
        
    def test_load_app(self):

        # Make sure that the Window hasn't been created yet
        tool = AnnotationTool()
        self.assertFalse(hasattr(tool, 'window'))
        self.assertFalse(hasattr(tool, 'background'))
        self.assertFalse(hasattr(tool, 'new_button'))
        self.assertFalse(hasattr(tool, 'new_wiz_button'))
        self.assertFalse(hasattr(tool, 'load_button'))       
        self.assertFalse(hasattr(tool, 'quit_button'))
        
        # Now check to make sure the initial buttons are in place
        tool.load_app(True)
        self.assertTrue(hasattr(tool, 'window'))
        self.assertTrue(hasattr(tool, 'background'))
        self.assertTrue(hasattr(tool, 'new_button'))
        self.assertTrue(hasattr(tool, 'new_wiz_button'))
        self.assertTrue(hasattr(tool, 'load_button'))       
        self.assertTrue(hasattr(tool, 'quit_button'))
        
        


        

        
if __name__ == '__main__':
    unittest.main()