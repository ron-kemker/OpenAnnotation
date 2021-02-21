# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 16:44:48 2021

@author: Ronald Kemker
"""

import unittest
from AnnotationTool import AnnotationTool
from interactivebox import InteractiveBox
from fileio import Annotation, ROI

class MockImg(object):
    def __init__(self, x=640, y=480):
        self.size = [x, y]

class TestInteractiveBox(unittest.TestCase):

    def test_init(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 5, 5]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']

        ibox = InteractiveBox(tool, 10, 10, 200, 200, tool.colorspace[0])
        
        self.assertTrue(hasattr(ibox, 'root_app'))
        self.assertTrue(hasattr(ibox, 'left'))
        self.assertTrue(hasattr(ibox, 'right'))
        self.assertTrue(hasattr(ibox, 'top'))
        self.assertTrue(hasattr(ibox, 'bottom'))
        self.assertTrue(hasattr(ibox, 'color'))
        self.assertTrue(hasattr(ibox, 'close_button_size'))
        self.assertTrue(hasattr(ibox, 'line_width'))
        self.assertTrue(hasattr(ibox, 'height'))
        self.assertTrue(hasattr(ibox, 'width'))
        
        self.assertEqual(ibox.close_button_size, 20)
        self.assertEqual(ibox.line_width, 5)        
        self.assertEqual(ibox.height, 195)
        self.assertEqual(ibox.width, 195)
        
    def test_draw_box(self):

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
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']
        tool.img = MockImg()

        tool._draw_workspace()
        canvas_children = tool.canvas.winfo_children()
        ibox = InteractiveBox(tool, 10, 10, 200, 200, tool.colorspace[0])
        self.assertEqual(len(canvas_children), 3)
        
        ibox.draw_box(0)
        
        canvas_children = tool.canvas.winfo_children()
        self.assertTrue(hasattr(ibox, 'rect'))
        self.assertTrue(hasattr(ibox, 'close_button'))
        self.assertEqual(len(canvas_children), 4)
           
    def test_right_clicked(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        
        ibox = InteractiveBox(tool, 10, 10, 200, 200, tool.colorspace[0])
        
        self.assertTrue(ibox.right_clicked(200, 202))
        self.assertTrue(ibox.right_clicked(200, 8))
        self.assertTrue(ibox.right_clicked(198, 100))
        self.assertTrue(ibox.right_clicked(202, 100))

        self.assertFalse(ibox.right_clicked(197, 100))
        self.assertFalse(ibox.right_clicked(203, 100))
        self.assertFalse(ibox.right_clicked(200, 7))
        self.assertFalse(ibox.right_clicked(200, 203))

    def test_left_clicked(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        
        ibox = InteractiveBox(tool, 10, 10, 200, 200, tool.colorspace[0])
        
        self.assertTrue(ibox.left_clicked(10, 202))
        self.assertTrue(ibox.left_clicked(10, 8))
        self.assertTrue(ibox.left_clicked(8, 100))
        self.assertTrue(ibox.left_clicked(12, 100))

        self.assertFalse(ibox.left_clicked(7, 100))
        self.assertFalse(ibox.left_clicked(13, 100))
        self.assertFalse(ibox.left_clicked(10, 7))
        self.assertFalse(ibox.left_clicked(10, 203))

    def test_top_clicked(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        
        ibox = InteractiveBox(tool, 10, 10, 200, 200, tool.colorspace[0])
        
        self.assertTrue(ibox.top_clicked(8, 10))
        self.assertTrue(ibox.top_clicked(202, 10))
        self.assertTrue(ibox.top_clicked(100, 8))
        self.assertTrue(ibox.top_clicked(100, 12))

        self.assertFalse(ibox.top_clicked(7, 10))
        self.assertFalse(ibox.top_clicked(203, 10))
        self.assertFalse(ibox.top_clicked(100, 7))
        self.assertFalse(ibox.top_clicked(100, 13))

    def test_bottom_clicked(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        
        ibox = InteractiveBox(tool, 10, 10, 200, 200, tool.colorspace[0])
        
        self.assertTrue(ibox.bottom_clicked(202, 200))
        self.assertTrue(ibox.bottom_clicked(8, 200))
        self.assertTrue(ibox.bottom_clicked(100, 198))
        self.assertTrue(ibox.bottom_clicked(100, 202))

        self.assertFalse(ibox.bottom_clicked(100, 197))
        self.assertFalse(ibox.bottom_clicked(100, 203))
        self.assertFalse(ibox.bottom_clicked(7, 200))
        self.assertFalse(ibox.bottom_clicked(203, 200))
      
    def test_delete_box(self):
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
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']
        tool.img = MockImg()

        tool._draw_workspace()
        ibox = InteractiveBox(tool, 10, 10, 200, 200, tool.colorspace[0])
        ibox.draw_box(0)
        
        self.assertEqual(len(tool.annotations[0].roi) , 3)
        ibox.delete_box(0)
        self.assertEqual(len(tool.annotations[0].roi) , 2)
        ibox.delete_box(0)
        self.assertEqual(len(tool.annotations[0].roi) , 1)
  
if __name__ == '__main__':
    unittest.main()
