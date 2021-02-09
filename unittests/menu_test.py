# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 20:41:37 2021

@author: Ronald Kemker
"""

from PIL import Image
import unittest
from AnnotationTool import AnnotationTool
from menu import AppMenu
from fileio import Annotation, ROI

class MockMeta(object):
    def __init__(self, orientation):
        self.has_exif = True
        self.orientation = orientation

class MockImg(object):
    def __init__(self, x=640, y=480):
        self.size = [x, y]
        
class TestMenu(unittest.TestCase):

    def test_init(self):
        tool = AnnotationTool()
        menu = AppMenu(tool)
        self.assertEqual(menu.root_app, tool)
        
    def test_draw_menu(self):
        tool = AnnotationTool()
        tool.load_app(True)
        
        appMenu = AppMenu(tool)   
        menu, fileMenu, toolMenu, helpMenu = appMenu._draw_menu()
        
        self.assertTrue(menu.winfo_exists())
        self.assertEqual(len(menu.winfo_children()), 2)
        self.assertEqual(menu.entrycget(1, 'label'), 'File')
        self.assertEqual(menu.entrycget(2, 'label'), 'Help')        
        
        self.assertTrue(fileMenu.winfo_exists())
        self.assertEqual(fileMenu.entrycget(1, 'label'), 'New Blank Project')
        self.assertEqual(fileMenu.entrycget(2, 'label'), 'New Project Wizard')
        self.assertEqual(fileMenu.entrycget(3, 'label'), 'Open Project')
        self.assertEqual(fileMenu.entrycget(5, 'label'), 'Quit')
        
        self.assertFalse(toolMenu)
        
        self.assertTrue(helpMenu.winfo_exists())
        self.assertEqual(helpMenu.entrycget(1, 'label'), 
                         "OpenAnnotation Documentation")
        self.assertEqual(helpMenu.entrycget(2, 'label'), 
                         "About OpenAnnotation")        
        
        
        tool.project_open = True
        tool.annotations = []
        menu, fileMenu, toolMenu, helpMenu = appMenu._draw_menu()
        
        self.assertTrue(menu.winfo_exists())
        self.assertEqual(len(menu.winfo_children()), 3)
        self.assertEqual(menu.entrycget(1, 'label'), 'File')
        self.assertEqual(menu.entrycget(2, 'label'), 'Tools')   
        self.assertEqual(menu.entrycget(3, 'label'), 'Help')   
        
        self.assertTrue(fileMenu.winfo_exists())
        self.assertEqual(fileMenu.entrycget(1, 'label'), 'New Blank Project')
        self.assertEqual(fileMenu.entrycget(2, 'label'), 'New Project Wizard')
        self.assertEqual(fileMenu.entrycget(3, 'label'), 'Open Project')
        self.assertEqual(fileMenu.entrycget(4, 'label'), 'Save Project')
        self.assertEqual(fileMenu.entrycget(5, 'label'), 'Close Project')
        self.assertEqual(fileMenu.entrycget(7, 'label'), "Import File")
        self.assertEqual(fileMenu.entrycget(8, 'label'), "Import Directory")
        self.assertEqual(fileMenu.entrycget(9, 'label'), 
                         "Export Project to CSV")        
        self.assertEqual(fileMenu.entrycget(11, 'label'), 'Quit')
        
        self.assertTrue(toolMenu.winfo_exists())
        self.assertEqual(toolMenu.entrycget(1, 'label'), "Class Manager")
        self.assertEqual(toolMenu.entrycget(2, 'label'), 'Options')
        self.assertEqual(toolMenu.entrycget(3, 'label'), "Options")
        
        self.assertTrue(helpMenu.winfo_exists())
        self.assertEqual(helpMenu.entrycget(1, 'label'), 
                         "OpenAnnotation Documentation")
        self.assertEqual(helpMenu.entrycget(2, 'label'), 
                         "About OpenAnnotation") 

        tool.annotations.append(Annotation())
        self.assertTrue(toolMenu.winfo_exists())
        _, _, toolMenu, _ = appMenu._draw_menu()

        self.assertEqual(toolMenu.entrycget(1, 'label'), "Class Manager")
        self.assertEqual(toolMenu.entrycget(2, 'label'), 'Options')
        self.assertEqual(toolMenu.entrycget(3, 'label'), "Reset Image")
        self.assertEqual(toolMenu.entrycget(4, 'label'), 'Select Image #')

    def test_select_image(self):
        tool = AnnotationTool()
        tool.load_app(True)
        
        appMenu = AppMenu(tool)
        complete = appMenu.select_image()
        self.assertTrue(complete)
        self.assertTrue(hasattr(appMenu, 'prompt'))
        self.assertTrue(hasattr(appMenu, 'prompt_entry'))
        
        prompt_frame = appMenu.prompt.winfo_children()[0]
        frame_child = prompt_frame.winfo_children()
        
        arr = ["Move to Image #", '', "Ok", "Cancel"]
        for i, child in enumerate(frame_child):
            self.assertEqual(frame_child[i].cget('text'), arr[i])
            
    def test_select_image_action(self):
        tool = AnnotationTool()
        tool.load_app(True)
        tool.annotations = [Annotation(), Annotation(), Annotation()]
        
        appMenu = AppMenu(tool)
        appMenu.select_image()
        appMenu.prompt_entry.insert(0, "1")
        complete = appMenu.select_image_action()
        self.assertTrue(complete)
        
        appMenu.select_image()
        appMenu.prompt_entry.insert(0, "4")
        complete = appMenu.select_image_action()
        self.assertFalse(complete)

        appMenu.select_image()
        appMenu.prompt_entry.insert(0, "-1")
        complete = appMenu.select_image_action()
        self.assertFalse(complete)
        
    def test_file_to_annotation(self):
        tool = AnnotationTool()
        tool.load_app(True)
        tool.annotations = []
        
        appMenu = AppMenu(tool)
        
        complete = appMenu.file_to_annotation('test.jpg', MockMeta(6))
        self.assertTrue(complete)
        self.assertEqual(tool.annotations[-1].rotation, Image.ROTATE_270)
        
        complete = appMenu.file_to_annotation('test2.jpg', MockMeta(3))
        self.assertTrue(complete)
        self.assertEqual(tool.annotations[-1].rotation, Image.ROTATE_180)
        
        complete = appMenu.file_to_annotation('test3.jpg', MockMeta(8))
        self.assertTrue(complete)
        self.assertEqual(tool.annotations[-1].rotation, Image.ROTATE_90)

    def test_import_file(self):
        
        tool = AnnotationTool()
        tool.load_app(True)
        tool.annotations = []
        tool.file_list = []
        tool.current_file = 0
        tool.class_list = []
        tool.img = MockImg(640, 480)

        appMenu = AppMenu(tool)
        
        self.assertTrue(tool.saved)
        complete = appMenu._import_file('test.jpg', MockMeta(6))
        self.assertTrue(complete)
        self.assertEqual(len(tool.annotations), 1)
        self.assertFalse(tool.saved)

        tool.saved = True
        self.assertTrue(tool.saved)
        complete = appMenu._import_file('test2.jpg', MockMeta(6))
        self.assertTrue(complete) 
        self.assertEqual(len(tool.annotations), 2)
        self.assertFalse(tool.saved)

        tool.saved = True
        self.assertTrue(tool.saved)
        complete = appMenu._import_file('test.jpg', MockMeta(6))
        self.assertTrue(complete) 
        self.assertEqual(len(tool.annotations), 2)
        self.assertTrue(tool.saved)
        
        complete = appMenu._import_file('', MockMeta(6))
        self.assertFalse(complete) 
        self.assertEqual(len(tool.annotations), 2)
        self.assertTrue(tool.saved)

    
    def test_import_files_in_directory(self):
        tool = AnnotationTool()
        tool.load_app(True)
        tool.annotations = [Annotation(), Annotation()]
        tool.file_list = ['file1.jpg', 'file2.jpg']
        tool.current_file = 0
        tool.class_list = []
        tool.img = MockImg(640, 480)

        appMenu = AppMenu(tool)

        self.assertTrue(tool.saved)
        complete = appMenu._import_files_in_directory('path/',MockMeta(6))
        self.assertTrue(complete)
        self.assertEqual(len(tool.annotations), 2)
        self.assertFalse(tool.saved)

        tool.saved = True
        self.assertTrue(tool.saved)
        complete = appMenu._import_files_in_directory('path/', MockMeta(6))
        self.assertTrue(complete) 
        self.assertEqual(len(tool.annotations), 2)
        self.assertFalse(tool.saved)

        tool.saved = True
        self.assertTrue(tool.saved)        
        complete = appMenu._import_files_in_directory('', MockMeta(6))
        self.assertFalse(complete) 
        self.assertEqual(len(tool.annotations), 2)
        self.assertTrue(tool.saved)
        
    def test_new(self):
        
        tool = AnnotationTool()
        tool.load_app(True)   
        
        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
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
        
        appMenu = AppMenu(tool)
        complete = appMenu._new()
        
        self.assertTrue(complete)
        self.assertEqual(tool.file_list, [])
        self.assertTrue(tool.project_open)
        self.assertEqual(tool.annotations, [])
        self.assertEqual(tool.top_colors_free, tool.top_colors)
        self.assertEqual(tool.top_colors_used, [])
        self.assertEqual(tool.class_count, [])
        self.assertEqual(tool.current_file, 0)
        self.assertEqual(tool.class_list, [])
        self.assertEqual(tool.colorspace, [])
        
    def test_open(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        
        # Annotation added
        tool.annotations = []
        tool.file_list = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
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
                a.push(roi, i%len(tool.class_list))
            tool.annotations.append(a)           

        appMenu = AppMenu(tool)
        complete = appMenu._open('file.oaf')
        self.assertTrue(complete)
        self.assertEqual(tool.class_count, [6, 6, 3])
        self.assertTrue(tool.project_open)
        self.assertTrue(tool.saved)
        self.assertEqual(tool.top_colors_used, tool.colorspace)
        self.assertEqual(tool.top_colors_free, tool.top_colors[3:])

        appMenu = AppMenu(tool)
        complete = appMenu._open('')
        self.assertFalse(complete)

    def test_save(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        
  
        tool.saved = False
        appMenu = AppMenu(tool)
        complete = appMenu._save('file.oaf')
        self.assertTrue(complete)
        self.assertTrue(tool.saved)
       
        tool.saved = False
        appMenu = AppMenu(tool)
        complete = appMenu._save('')
        self.assertFalse(complete)   
        self.assertFalse(tool.saved)
        
    def test_close(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.saved = False
        tool.project_open = True
  
        appMenu = AppMenu(tool)
        complete = appMenu._close()
        
        pop = appMenu.popup_window
        self.assertTrue(complete)
        self.assertFalse(tool.project_open)
        self.assertTrue(pop.winfo_exists())
        
        arr = ["Close without saving?", "Save", "Close", "Cancel"]
        for i in range(4):
            widget = pop.winfo_children()[0].winfo_children()[i]
            self.assertEqual(arr[i], widget.cget('text'))
                    
    def test_save_close_command(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        
  
        tool.saved = False
        appMenu = AppMenu(tool)
        complete = appMenu._save_close_command('file.oaf')
        self.assertTrue(complete)

        complete = appMenu._save_close_command('')
        self.assertFalse(complete)
        
    def test_close_command(self):
        pass
    
    def test_quit(self):
        pass
    
    def test_csv_exporter(self):
        pass
    
    def test_draw_about_box(self):
        pass
    
    def test_new_project_wizard(self):
        pass
    
    
if __name__ == '__main__':
    unittest.main()