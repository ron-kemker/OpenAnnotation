# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:48:56 2021

@author: Master
"""

import unittest, time, sys, random
from  AnnotationTool import AnnotationTool
from fileio import Annotation, ROI

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
        
        # Make sure function runs to completion
        complete = tool.load_app(True)
        self.assertTrue(complete)
        
        # Now check to make sure the initial buttons are in place
        self.assertTrue(hasattr(tool, 'window'))
        self.assertTrue(hasattr(tool, 'background'))
        self.assertTrue(hasattr(tool, 'new_button'))
        self.assertTrue(hasattr(tool, 'new_wiz_button'))
        self.assertTrue(hasattr(tool, 'load_button'))       
        self.assertTrue(hasattr(tool, 'quit_button'))


    def test_draw_object_class_manager(self):

        tool = AnnotationTool()
        tool.class_list = []
        
        # Make sure function runs to completion        
        complete = tool._draw_object_class_manager()        
        self.assertTrue(complete)
        
        # Functional tests
        self.assertTrue(hasattr(tool, 'obj_mgr'))
        self.assertEqual(tool, tool.obj_mgr.root_app)


    # def _draw_workspace(self):
        
    #     self.app_menu._draw_menu()
        
    #     self.background.destroy()
        
    #     # Build Background Frame                       
    #     self.background = Frame(self.window,
    #                             bg="gray",
    #                             width=self.window_width,
    #                             height=self.window_height)
    #     self.background.place(x=0, 
    #                           y=0,
    #                           width = self.window_width,
    #                           height = self.window_height)

    #     # Draw Toolbar on Left
    #     toolbar = Toolbar(self) 

    def test_draw_workspace(self):
        
        class MockImg(object):
            def __init__(self):
                self.size = [640, 480]
        
        tool = AnnotationTool()
        tool.load_app(True)
        tool.annotations = []
        tool.class_list = []
        
        # Empty Project
        complete = tool._draw_workspace()
        self.assertTrue(complete)
        self.assertTrue(hasattr(tool, 'background'))
        self.assertTrue(hasattr(tool, 'app_menu'))
        self.assertTrue(hasattr(tool, 'canvas_frame'))
        self.assertTrue(hasattr(tool, 'canvas'))
        self.assertFalse(hasattr(tool, 'aspect_ratio'))
        self.assertFalse(hasattr(tool, 'boxes'))
        
        
        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['blue', 'green', 'red']
        tool.current_file = 0
        tool.img = MockImg()
    
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            for p in range(3):
                roi = ROI()
                roi.push(0,0)
                roi.push(100.0,100.0)
                a.push(roi, random.randint(0,2))
            tool.annotations.append(a)
            
        complete = tool._draw_workspace()
        self.assertTrue(complete)
        self.assertTrue(hasattr(tool, 'background'))
        self.assertTrue(hasattr(tool, 'app_menu'))
        self.assertTrue(hasattr(tool, 'canvas_frame'))
        self.assertTrue(hasattr(tool, 'canvas'))
        self.assertTrue(hasattr(tool, 'aspect_ratio'))
        self.assertTrue(hasattr(tool, 'boxes'))        
        self.assertEqual(tool.aspect_ratio, 640/(1024-150))



if __name__ == '__main__':
    unittest.main()