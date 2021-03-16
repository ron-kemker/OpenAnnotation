# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 20:55:00 2021

@author: Ronald Kemker
"""

import unittest
from AnnotationTool import AnnotationTool
from toolbar import Toolbar
from fileio import Annotation, ROI

class TestToolbar(unittest.TestCase):

    def test_init(self):
        tool = AnnotationTool()
        tool.load_app(True) 


        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.current_file = 0  
        tool.num_pages = 1
        toolbar = Toolbar(tool)

        self.assertEqual(toolbar.root_app, tool)
        self.assertEqual(toolbar.toolbar_width, tool.window_width)
        self.assertEqual(toolbar.toolbar_height, tool.toolbar_height)
        self.assertEqual(len(toolbar.toolbar_frame.winfo_children()), 0)
        
        
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            for p in range(3):
                roi = ROI()
                roi.push(0,0)
                roi.push(100.0,100.0)
                a.push(roi, i%len(tool.class_list))
            tool.annotations.append(a) 
            
        toolbar = Toolbar(tool)
        self.assertEqual(toolbar.root_app, tool)
        self.assertEqual(toolbar.toolbar_width, tool.window_width)
        self.assertEqual(toolbar.toolbar_height, tool.toolbar_height)
        self.assertEqual(len(toolbar.toolbar_frame.winfo_children()), 3)

    def test_draw_image_navigator(self):
        tool = AnnotationTool()
        tool.load_app(True) 

        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.current_file = 0        
        tool.num_pages = 1
        
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            for p in range(3):
                roi = ROI()
                roi.push(0,0)
                roi.push(100.0,100.0)
                a.push(roi, i%len(tool.class_list))
            tool.annotations.append(a) 
            
        toolbar = Toolbar(tool)
        nav_frame = toolbar.toolbar_frame.winfo_children()[0]
        nav_frame_children = nav_frame.winfo_children()
        
        self.assertEqual(len(nav_frame_children), 3)
        self.assertEqual(nav_frame_children[0].cget('text'), "Page 1/2")
        
    def test_next_image(self):
        tool = AnnotationTool()
        tool.load_app(True) 

        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.current_file = 0        
        tool.num_pages = 1
        
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            for p in range(3):
                roi = ROI()
                roi.push(0,0)
                roi.push(100.0,100.0)
                a.push(roi, i%len(tool.class_list))
            tool.annotations.append(a) 
            
        toolbar = Toolbar(tool)
        self.assertEqual(tool.current_file, 0)
        
        truth = [1, 2, 3, 4, 4]
        for i in range(5):
            toolbar._next_image()
            self.assertEqual(tool.current_file, truth[i])
        
    def test_previous_image(self):
        tool = AnnotationTool()
        tool.load_app(True) 

        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.current_file = 0        
        tool.num_pages = 1
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            for p in range(3):
                roi = ROI()
                roi.push(0,0)
                roi.push(100.0,100.0)
                a.push(roi, i%len(tool.class_list))
            tool.annotations.append(a) 
            
        toolbar = Toolbar(tool)
        self.assertEqual(tool.current_file, 0)
        for i in range(5):
            toolbar._next_image()
            
        truth = [3, 2 , 1, 0, 0]
        for i in range(5):
            toolbar._previous_image()
            self.assertEqual(tool.current_file, truth[i])   
            
    def test_delete_from_project_button(self):
        tool = AnnotationTool()
        tool.load_app(True) 

        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.current_file = 0        
        tool.num_pages = 1
        
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            for p in range(3):
                roi = ROI()
                roi.push(0,0)
                roi.push(100.0,100.0)
                a.push(roi, i%len(tool.class_list))
            tool.annotations.append(a) 
            
        toolbar = Toolbar(tool)
        button = toolbar.toolbar_frame.winfo_children()[1]
        
        self.assertEqual(button.cget('text'), '')        
        self.assertEqual(button.cget('width'), 40)        
        self.assertEqual(button.cget('height'), 40)        
            
    def test_delete_from_project(self):

        tool = AnnotationTool()
        tool.load_app(True) 

        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.current_file = 0
        tool.num_pages = 1
        tool.class_count = [5, 5, 5]        
       
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            for p in range(3):
                roi = ROI()
                roi.push(0,0)
                roi.push(100.0,100.0)
                a.push(roi, p%len(tool.class_list))
            tool.annotations.append(a) 
            
        toolbar = Toolbar(tool)
        
        self.assertEqual(len(tool.annotations) , 5)
        self.assertEqual(len(tool.file_list) , 5)
        self.assertListEqual(tool.class_count, [5,5,5])
        toolbar._delete_from_project()
        self.assertEqual(len(tool.annotations) , 4)
        self.assertEqual(len(tool.file_list) , 4)
        self.assertListEqual(tool.class_count, [4,4,4])
            
    def test_draw_class_selection_menu(self):
        
        tool = AnnotationTool()
        tool.load_app(True) 

        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.current_file = 0
        tool.num_pages = 1
        tool.class_count = [5, 5, 5]        
       
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            tool.file_list.append('file%d.jpg' % i)
            for p in range(3):
                roi = ROI()
                roi.push(0,0)
                roi.push(100.0,100.0)
                a.push(roi, p%len(tool.class_list))
            tool.annotations.append(a) 
            
        toolbar = Toolbar(tool)        
        option_menu = toolbar.toolbar_frame.winfo_children()[2]
        self.assertEqual(option_menu.winfo_name(), '!optionmenu')
      
       
        
if __name__ == '__main__':
    unittest.main()