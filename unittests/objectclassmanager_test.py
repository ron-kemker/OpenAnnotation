# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 18:04:24 2021

@author: Ronald Kemker
"""

import unittest
from AnnotationTool import AnnotationTool
from objectclassmanager import ObjectClassManager
from fileio import Annotation, ROI

class TestObjectClassManager(unittest.TestCase):

    def test_init(self):
        tool = AnnotationTool()
        tool.load_app(True) 

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 5, 5]        
                   
        class_mgr = ObjectClassManager(tool)
        self.assertTrue(hasattr(class_mgr, 'root_app'))
        self.assertEqual(tool, class_mgr.root_app)
        self.assertTrue(hasattr(class_mgr, 'class_manager_window'))
        
    def test_choose_color(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 5, 5]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']
         
        self.assertTrue(tool.saved)
        self.assertEqual(len(tool.top_colors_used) , 3)
        self.assertEqual(len(tool.top_colors_free) , 3)
         
        class_mgr = ObjectClassManager(tool)  
        class_mgr._choose_color(0)
        
        self.assertFalse(tool.saved)        
        self.assertEqual(tool.colorspace[0], '#EEEEEE')
        self.assertEqual(tool.colorspace[1], '#FF0000')
        self.assertEqual(len(tool.top_colors_used) , 2)
        self.assertEqual(len(tool.top_colors_free) , 4)
        self.assertEqual(tool.top_colors_free[0], '#0000FF')
        
        class_mgr._choose_color(1)
        self.assertEqual(tool.colorspace[0], '#EEEEEE')
        self.assertEqual(tool.colorspace[1], '#EEEEEE')
        self.assertEqual(len(tool.top_colors_used) , 1)
        self.assertEqual(len(tool.top_colors_free) , 5)
        self.assertEqual(tool.top_colors_free[0], '#FF0000')
        
    def test_draw_frame(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 15, 501]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']
        
        class_mgr = ObjectClassManager(tool)  
        class_mgr.draw_frame()

        self.assertTrue(hasattr(class_mgr, 'class_manager_frame'))        
        self.assertTrue(hasattr(class_mgr, 'new_class_var'))        
        self.assertTrue(hasattr(class_mgr, 'new_class_entry'))        

        frame_children = class_mgr.class_manager_frame.winfo_children()
        self.assertEqual(len(frame_children), 19)
        
        self.assertEqual(frame_children[1].cget("text"), "1. winston")
        self.assertEqual(frame_children[2].cget("bg"), tool.colorspace[0])
        self.assertEqual(frame_children[3].cget("text"), "Rename")
        self.assertEqual(frame_children[4].cget("text"), "Delete")
        self.assertEqual(frame_children[5].cget("text"), 
                         " 5 labeled instances.")        
        self.assertEqual(frame_children[6].cget("text"), "2. prince")
        self.assertEqual(frame_children[7].cget("bg"), tool.colorspace[1])
        self.assertEqual(frame_children[8].cget("text"), "Rename")
        self.assertEqual(frame_children[9].cget("text"), "Delete")
        self.assertEqual(frame_children[10].cget("text"), 
                         " 15 labeled instances.")   
        self.assertEqual(frame_children[11].cget("text"), "3. duckie")
        self.assertEqual(frame_children[12].cget("bg"), tool.colorspace[2])
        self.assertEqual(frame_children[13].cget("text"), "Rename")
        self.assertEqual(frame_children[14].cget("text"), "Delete")
        self.assertEqual(frame_children[15].cget("text"), 
                         " 501 labeled instances.")           
        self.assertEqual(frame_children[17].cget("text"), "Add Class")         
        self.assertEqual(frame_children[18].cget("text"), "Close") 

    def test_rename_class_window(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 15, 501]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']
        
        class_mgr = ObjectClassManager(tool)  
        class_mgr._rename_class_window(0)

        self.assertTrue(hasattr(class_mgr, 'rename_entry'))  
        self.assertTrue(hasattr(class_mgr, 'rename_class_prompt'))  

        frame_children = class_mgr.rename_class_prompt.winfo_children()[0] \
            .winfo_children()
        self.assertEqual(len(frame_children), 4)
        self.assertEqual(frame_children[0].cget("text"), 
                         'Rename \"winston\" Class to:')
        self.assertEqual(frame_children[2].cget("text"), "Ok")
        self.assertEqual(frame_children[3].cget("text"), "Cancel")
        
        class_mgr._rename_class_window(1)

        self.assertTrue(hasattr(class_mgr, 'rename_entry'))  
        self.assertTrue(hasattr(class_mgr, 'rename_class_prompt'))  

        frame_children = class_mgr.rename_class_prompt.winfo_children()[0] \
            .winfo_children()
        self.assertEqual(len(frame_children), 4)
        self.assertEqual(frame_children[0].cget("text"), 
                         'Rename \"prince\" Class to:')
        self.assertEqual(frame_children[2].cget("text"), "Ok")
        self.assertEqual(frame_children[3].cget("text"), "Cancel")        
        
    def test_rename_class_action(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 15, 501]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']

        class_mgr = ObjectClassManager(tool)  

        self.assertTrue(tool.saved)
        self.assertEqual(tool.class_list[0], 'winston' )

        class_mgr._rename_class_window(0)
        class_mgr.rename_class_var.set('')
        class_mgr._rename_class_action(0)
        
        self.assertTrue(tool.saved)
        self.assertEqual(tool.class_list[0], 'winston' )

        class_mgr._rename_class_window(0)
        class_mgr.rename_class_var.set('TestRename')
        class_mgr._rename_class_action(0)
        
        self.assertFalse(tool.saved)
        self.assertEqual(tool.class_list[0], 'TestRename' ) 
      
    def test_add_class(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 15, 501]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']

        class_mgr = ObjectClassManager(tool)  

        self.assertTrue(tool.saved)
        self.assertEqual(tool.class_list[-1], 'duckie' )

        class_mgr.draw_frame()
        class_mgr.new_class_var.set('')
        class_mgr._add_class_action()
        
        self.assertTrue(tool.saved)
        self.assertEqual(tool.class_list[-1], 'duckie' )

        class_mgr.draw_frame()
        class_mgr.new_class_var.set('winston')
        class_mgr._add_class_action()
        
        self.assertTrue(tool.saved)
        self.assertEqual(tool.class_list[-1], 'duckie' ) 

        class_mgr.draw_frame()
        class_mgr.new_class_var.set('TestAdd')
        class_mgr._add_class_action()
        
        self.assertFalse(tool.saved)
        self.assertEqual(tool.class_list[-1], 'TestAdd' )
        self.assertEqual(tool.class_count[-1], 0)
        self.assertEqual(tool.colorspace[-1], '#00FFFF')
        self.assertEqual(len(tool.top_colors_used) , 4)
        self.assertEqual(len(tool.top_colors_free) , 2)
            
    def test_check_before_remove(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 15, 501]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']

        class_mgr = ObjectClassManager(tool)  
        self.assertFalse(hasattr(class_mgr, 'popup_window'))
        class_mgr._check_before_remove(0)
        self.assertTrue(hasattr(class_mgr, 'popup_window'))

        frame_children = class_mgr.popup_window.winfo_children()[0]. \
            winfo_children()
        self.assertEqual(len(frame_children), 3)
        
        self.assertEqual(frame_children[0].cget("text"), 
                         "Delete Class?  You cannot undo this action.")
        self.assertEqual(frame_children[1].cget("text"), "Remove")
        self.assertEqual(frame_children[2].cget("text"), "Cancel")
    
    def test_remove_class(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 15, 501]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']

        class_mgr = ObjectClassManager(tool)  

        self.assertTrue(tool.saved)
        self.assertEqual(tool.class_list[-1], 'duckie' )

        class_mgr.draw_frame()
        class_mgr._remove_class(2)
        
        self.assertEqual(tool.class_list[-1], 'prince' ) 
        self.assertFalse(tool.saved)
        self.assertEqual(tool.class_count[-1], 15)
        self.assertEqual(tool.colorspace[-1], '#FF0000')
        self.assertEqual(len(tool.top_colors_used) , 2)
        self.assertEqual(len(tool.top_colors_free) , 4)
 
if __name__ == '__main__':
    unittest.main()