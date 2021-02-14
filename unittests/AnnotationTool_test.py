# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:48:56 2021

@author: Master
"""

import unittest, time, sys, random
from  AnnotationTool import AnnotationTool
from fileio import Annotation, ROI

class MockImg(object):
    def __init__(self, x=640, y=480):
        self.size = [x, y]

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
        self.assertListEqual(tool.window_size_strings , 
                             ["1024x768", "800x600"])
        
        
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
        self.assertEqual(tool.window_size_index , 0)

        # Make sure Appmenu has correct "root_app"
        self.assertEqual(tool, tool.app_menu.root_app)
        
    def test_load_app(self):

        # Make sure that the Window hasn't been created yet
        tool = AnnotationTool()
        self.assertFalse(hasattr(tool, 'window'))
        self.assertFalse(hasattr(tool, 'background'))
        
        # Make sure function runs to completion
        complete = tool.load_app(True)
        self.assertTrue(complete)
        
        # Now check to make sure the initial buttons are in place
        self.assertTrue(hasattr(tool, 'window'))
        self.assertTrue(hasattr(tool, 'background'))
        tool.window.destroy()

    def test_draw_object_class_manager(self):

        tool = AnnotationTool()
        tool.class_list = []
        
        # Make sure function runs to completion        
        complete = tool._draw_object_class_manager()        
        self.assertTrue(complete)
        
        # Functional tests
        self.assertTrue(hasattr(tool, 'obj_mgr'))
        self.assertEqual(tool, tool.obj_mgr.root_app)
        tool.obj_mgr.class_manager_window.destroy()

        
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
        self.assertTrue(hasattr(tool, 'canvas'))
        self.assertTrue(hasattr(tool, 'aspect_ratio'))
        self.assertTrue(hasattr(tool, 'boxes'))        
        self.assertEqual(tool.aspect_ratio, 640/(1024-150))
        self.assertEqual(3, len(tool.boxes))
        tool.window.destroy()

    def test_on_click(self):
                    
        tool = AnnotationTool()
        tool.load_app(True)

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
        
        tool._draw_workspace()
                
        # Click Top 
        complete = tool._on_click(Event(10, 0))        
        self.assertTrue(complete)
        self.assertEqual('TOP', tool.box_resize_mode)
        self.assertEqual(0, tool.resize_box_id)
        
        # Click Bottom
        complete = tool._on_click(Event(10, 100/tool.aspect_ratio))        
        self.assertTrue(complete)
        self.assertEqual('BOTTOM', tool.box_resize_mode)
        self.assertEqual(0, tool.resize_box_id)   
        
        # Click Left
        complete = tool._on_click(Event(0, 60))        
        self.assertTrue(complete)
        self.assertEqual('LEFT', tool.box_resize_mode)
        self.assertEqual(0, tool.resize_box_id)
        
        # Click Right        
        complete = tool._on_click(Event(100/tool.aspect_ratio, 60))        
        self.assertTrue(complete)
        self.assertEqual('RIGHT', tool.box_resize_mode)
        self.assertEqual(0, tool.resize_box_id)
        
        # Click elsewhere to create a new box
        complete = tool._on_click(Event(60, 60))        
        self.assertTrue(complete)
        self.assertEqual('NEW', tool.box_resize_mode)
        tool.window.destroy()

    def test_on_release(self):
        
        tool = AnnotationTool()
        tool.load_app(True)

        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['blue', 'green', 'red']
        tool.class_count = [0 , 0 , 0]
        tool.current_file = 0
        tool.img = MockImg()
    
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            tool.annotations.append(a)        
        
        tool._draw_workspace()
                
        tool._on_click(Event(10, 10)) 
        
        for i in range(11, 31):
            tool._on_move_press(Event(i,i))
        
        complete = tool._on_release(Event(30, 30))
        self.assertTrue(complete)
        self.assertEqual(0,  tool.annotations[0].label[0])
        self.assertEqual([1,0,0],  tool.class_count)
        self.assertEqual([10*tool.aspect_ratio,10*tool.aspect_ratio], 
                          tool.annotations[0].roi[0].points[0])
        self.assertEqual([30*tool.aspect_ratio,30*tool.aspect_ratio], 
                          tool.annotations[0].roi[0].points[1])        
        self.assertFalse(tool.saved)
        self.assertEqual(tool.box_resize_mode , 'NEW')
        tool.window.destroy()

    def test_on_move_press(self):

        tool = AnnotationTool()
        tool.load_app(True)

        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['blue', 'green', 'red']
        tool.class_count = [0 , 0 , 0]
        tool.current_file = 0
        tool.img = MockImg()
    
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            tool.annotations.append(a)        
        
        tool._draw_workspace()
                
        tool._on_click(Event(10, 10)) 
        self.assertFalse(hasattr(tool, 'rect'))
        complete = tool._on_move_press(Event(11,11))
        self.assertTrue(complete)
        self.assertTrue(hasattr(tool, 'rect'))

        complete = tool._on_move_press(Event(12,12))
        self.assertTrue(complete)        
        self.assertTrue(hasattr(tool, 'rect'))
        self.assertTrue(hasattr(tool, 'box_end'))

        # Create a new Box
        tool._on_click(Event(10, 10)) 
        for i in range(11, 26):
            tool._on_move_press(Event(i,i))
        tool._on_release(Event(25, 25))


        tool.resize_box_id = 0
        tool.box_resize_mode = 'RIGHT'
        self.assertEqual(tool.annotations[0].roi[0].points[1], 
                          [25*tool.aspect_ratio , 25*tool.aspect_ratio])
        complete = tool._on_move_press(Event(20,25))
        
        self.assertTrue(complete)               
        self.assertEqual(tool.annotations[0].roi[0].points[1], 
                          [20*tool.aspect_ratio , 25*tool.aspect_ratio])


        tool.box_resize_mode = 'LEFT'
        self.assertEqual(tool.annotations[0].roi[0].points[0], 
                          [10*tool.aspect_ratio , 10*tool.aspect_ratio])
        complete = tool._on_move_press(Event(15,10))
        
        self.assertTrue(complete)               
        self.assertEqual(tool.annotations[0].roi[0].points[0], 
                          [15*tool.aspect_ratio , 10*tool.aspect_ratio])
        
        
        tool.box_resize_mode = 'TOP'
        self.assertEqual(tool.annotations[0].roi[0].points[0], 
                          [15*tool.aspect_ratio , 10*tool.aspect_ratio])
        complete = tool._on_move_press(Event(15,15))
        
        self.assertTrue(complete)               
        self.assertEqual(tool.annotations[0].roi[0].points[0], 
                          [15*tool.aspect_ratio , 15*tool.aspect_ratio])
        
        
        tool.box_resize_mode = 'BOTTOM'
        self.assertEqual(tool.annotations[0].roi[0].points[1], 
                          [20*tool.aspect_ratio , 25*tool.aspect_ratio])
        complete = tool._on_move_press(Event(20,20))
        
        self.assertTrue(complete)               
        self.assertEqual(tool.annotations[0].roi[0].points[1], 
                          [20*tool.aspect_ratio , 20*tool.aspect_ratio])
        tool.window.destroy()
        

    def test_reset_image(self):
        
        tool = AnnotationTool()
        tool.load_app(True)   
        
        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['blue', 'green', 'red']
        tool.current_file = 0
        tool.class_count = [0 , 15 , 0]
        tool.img = MockImg()
    
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            for p in range(3):
                roi = ROI()
                roi.push(0,0)
                roi.push(100.0,100.0)
                a.push(roi, 1)
            tool.annotations.append(a)        
        
        tool._draw_workspace()        
        
        self.assertEqual(tool.annotations[tool.current_file].size(), 3)
        complete = tool._reset_image()
        self.assertEqual(tool.annotations[tool.current_file].size(), 0)

        self.assertTrue(complete)
        
        tool.window.destroy()

if __name__ == '__main__':
    unittest.main()