# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 08:46:51 2021

@author: Ronald Kemker
"""


import unittest
from AnnotationTool import AnnotationTool
from help import HelpMenu

class TestHelp(unittest.TestCase):

    def test_init(self):
        tool = AnnotationTool()
        help_menu = HelpMenu(tool)
        
        self.assertTrue(hasattr(help_menu, 'root'))
        self.assertTrue(hasattr(help_menu, 'window_width'))
        self.assertTrue(hasattr(help_menu, 'window_height'))
        self.assertTrue(hasattr(help_menu, 'left_pane_width'))
        self.assertTrue(hasattr(help_menu, 'right_pane_width'))
        
        self.assertEqual(tool, help_menu.root)
        self.assertEqual(1024, help_menu.window_width)
        self.assertEqual(768, help_menu.window_height)
        self.assertEqual(300, help_menu.left_pane_width)
        self.assertEqual(723, help_menu.right_pane_width)
            
    def test_draw_menu(self):
        tool = AnnotationTool()
        tool.load_app(True)
        help_menu = HelpMenu(tool)
        help_menu._draw_menu()

        self.assertTrue(hasattr(help_menu, 'window'))
        self.assertTrue(hasattr(help_menu, 'background'))
        self.assertTrue(hasattr(help_menu, 'right_pane'))
        self.assertTrue(hasattr(help_menu, 'help_files'))
        
        self.assertEqual(help_menu.window.title(), 'OpenAnnotation Help')
        
        window_children = help_menu.window.winfo_children()
        background = window_children[0]
        
        self.assertEqual(len(window_children), 1)
        self.assertEqual(background.cget('width'), 1024)
        self.assertEqual(background.cget('height'), 768)
        self.assertEqual(background.cget('bg'), 'gray')

        background_children = background.winfo_children()
        left_pane = background_children[0]
        right_pane = background_children[1]
        
        self.assertEqual(len(background_children), 2)
        self.assertEqual(left_pane.cget('width'), 300)
        self.assertEqual(left_pane.cget('height'), 768)
        self.assertEqual(left_pane.cget('bg'), 'white')        
        self.assertEqual(right_pane.cget('width'), 723)
        self.assertEqual(right_pane.cget('height'), 768)
        self.assertEqual(right_pane.cget('bg'), 'white')    
        self.assertEqual(len(help_menu.help_files), 3)
        
        left_pane_children = left_pane.winfo_children()
        label = left_pane_children[0]
        self.assertEqual(len(left_pane_children), 4)
        self.assertEqual(label.cget('text'), 'Navigation Bar')
        self.assertEqual(label.cget('bg'), 'white')

        right_pane_children = right_pane.winfo_children()
        self.assertEqual(len(right_pane_children), 2)
    
    def test_button_press(self):
        tool = AnnotationTool()
        tool.load_app(True)
        help_menu = HelpMenu(tool)
        help_menu._draw_menu()
        help_menu._button_press(0)
        help_menu._button_press(1)
        help_menu._button_press(2)
        
  
if __name__ == '__main__':
    unittest.main()