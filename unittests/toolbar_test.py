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
        toolbar = Toolbar(tool)

        self.assertEqual(toolbar.root_app, tool)
        self.assertEqual(toolbar.toolbar_width, tool.toolbar_width)
        self.assertEqual(toolbar.toolbar_height, tool.window_height)
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
        self.assertEqual(toolbar.toolbar_width, tool.toolbar_width)
        self.assertEqual(toolbar.toolbar_height, tool.window_height)
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
        
        self.assertEqual(len(nav_frame_children), 4)
        self.assertEqual(nav_frame_children[0].cget('text'), "Image Navigator")
        self.assertEqual(nav_frame_children[1].cget('text'), "1/5")
        
    def test_next_image(self):
        tool = AnnotationTool()
        tool.load_app(True) 

        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.current_file = 0        
       
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
        frame = toolbar.toolbar_frame.winfo_children()[1]
        
        self.assertEqual(len(frame.winfo_children()), 1)
        self.assertEqual(frame.cget('bg'), 'black')
        
        button = frame.winfo_children()[0]
        self.assertEqual(button.cget('text'), 'Remove from Project')        
        self.assertEqual(button.cget('fg'), 'black')        
            
    def test_delete_from_project(self):

        tool = AnnotationTool()
        tool.load_app(True) 

        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.current_file = 0
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
        frame = toolbar.toolbar_frame.winfo_children()[2]
                
        self.assertEqual(frame.cget('width'), toolbar.toolbar_width)
        self.assertEqual(frame.cget('height'), 70)
        self.assertEqual(frame.cget('bg'), 'black')
        
        frame_children = frame.winfo_children()

        self.assertEqual(len(frame_children) , 2)
        self.assertEqual(frame_children[0].cget('text'), 
                         'Select Class')
        
if __name__ == '__main__':
    unittest.main()