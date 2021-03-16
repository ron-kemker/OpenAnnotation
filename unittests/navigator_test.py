# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 20:59:13 2021

@author: Ronald Kemker
"""

import unittest
from AnnotationTool import AnnotationTool
from toolbar import Toolbar
from fileio import Annotation, ROI
from navigator import Navigator, helper_open_image

class MockImg(object):
    def __init__(self, x=640, y=480):
        self.size = [x, y]

class TestNavigator(unittest.TestCase):
    
    def test_init(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.file_list = []
        tool.annotations = []
        tool.class_list = ['winston', 'prince', 'duckie']

        tool._draw_workspace()

        navigator = Navigator(tool)   
        self.assertEqual(tool, navigator.root_app)
        
        background = tool.window.winfo_children()[2]
        navigator = background.winfo_children()[2]
        
        self.assertEqual(len(navigator.winfo_children()), 2)
        
        canvas = navigator.winfo_children()[0]
        scrollbar = navigator.winfo_children()[1]
        
        self.assertEqual(canvas.cget('width'), '200')
        self.assertEqual(canvas.cget('height'), '718')
        self.assertEqual(scrollbar.winfo_name(), '!scrollbar')
        
        
    def test_helper_open_image(self):
        
        img = helper_open_image('../img/delete.png', 200, 0)
        self.assertEqual(img.width, 200)
        self.assertEqual(img.height, 200)
    
    def test_change_image(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.file_list = []
        tool.annotations = []
        tool.current_file = 0
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
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
            
        tool.img = MockImg()            
        tool._draw_workspace()

        navigator = Navigator(tool)

        self.assertEqual(tool.current_file, 0)  
        navigator.change_image(1)
        self.assertEqual(tool.current_file, 1)  

if __name__ == '__main__':
    unittest.main()