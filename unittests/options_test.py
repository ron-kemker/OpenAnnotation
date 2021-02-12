# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 13:10:26 2021

@author: Ronald Kemker
"""

import unittest
from AnnotationTool import AnnotationTool
from optionmenu import OptionPrompt

class TestOptionPrompt(unittest.TestCase):
    
    def test_init(self):
        tool = AnnotationTool()
        opt = OptionPrompt(tool)
        self.assertTrue(hasattr(opt, 'window_width'))
        self.assertTrue(hasattr(opt, 'window_height'))
        self.assertTrue(hasattr(opt, 'root_app'))
            
        self.assertEqual(opt.window_height, 400)
        self.assertEqual(opt.window_width, 600)
        self.assertEqual(tool, opt.root_app)

    def test_draw_menu(self):
        tool = AnnotationTool()
        opt = OptionPrompt(tool)
        complete = opt.draw_window()
        self.assertTrue(complete)

        self.assertTrue(hasattr(opt, 'option_window'))
        self.assertTrue(hasattr(opt, 'background'))
        self.assertTrue(hasattr(opt, 'selected_size'))
        
        child_truth = ['Option Menu', 'Window Size', '1024x768', 'Ok', 
                       'Cancel']
        children = opt.background.winfo_children()
        
        for i, child in enumerate(children):
            self.assertEqual(child.cget('text'), child_truth[i])
    
    def test_ok_button(self):
        
        tool = AnnotationTool()
        tool.load_app(True)
        tool.annotations = []
        tool.class_list = []
        
        # Nothing Changes
        opt = OptionPrompt(tool)
        opt.draw_window()
        complete = opt.ok_button()
        self.assertTrue(complete)

        # Change Window Size
        opt = OptionPrompt(tool)
        opt.draw_window()
        opt.selected_size.set('800x600')
        complete = opt.ok_button()
        self.assertTrue(complete)
        self.assertEqual(tool.window_width, 800)
        self.assertEqual(tool.window_height, 600)
        self.assertEqual(tool.window_size_index, 1)

if __name__ == '__main__':
    unittest.main()