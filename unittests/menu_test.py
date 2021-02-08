# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 20:41:37 2021

@author: Ronald Kemker
"""

import unittest
from AnnotationTool import AnnotationTool
from menu import AppMenu
from fileio import Annotation

class TestAnnotationTool(unittest.TestCase):

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
        appMenu.select_image()
        
        self.assertTrue(hasattr(appMenu, 'prompt'))
        self.assertTrue(hasattr(appMenu, 'prompt_entry'))
        
        prompt_frame = appMenu.prompt.winfo_children()[0]
        frame_child = prompt_frame.winfo_children()
        
        arr = ["Move to Image #", '', "Ok", "Cancel"]
        for i, child in enumerate(frame_child):
            self.assertEqual(frame_child[i].cget('text'), arr[i])
            

    # def select_image_action(self):
    #     '''
    #     Retrieves a value from select_image Entry and sets the current_file to
    #     that value

    #     Returns
    #     -------
    #     None.

    #     '''
        
    #     # Pull the value from the entry box
    #     entry_val = int(self.prompt_entry.get())-1
        
    #     # If a valid number is entered
    #     if entry_val >= 0 and entry_val < len(self.root_app.annotations): 
    #         # Set the current file
    #         self.root_app.current_file = entry_val
             
    #         # Refresh GUI
    #         self.root_app._load_image_from_file() 
    #         self.root_app._draw_workspace()
    #         # Destroy Prompt
    #         self.prompt.destroy()
    #     else:
    #         print('Project Image Index Out of Bounds')


    def test_select_image_action(self):
        tool = AnnotationTool()
        tool.load_app(True)
        
        appMenu = AppMenu(tool)
        appMenu.select_image()
        appMenu.select_image_action()
    
    def test_file_to_annotation(self):
        pass
    
    def test_import_file(self):
        pass
    
    def test_import_files_in_directory(self):
        pass
    
    def test_new(self):
        pass
    
    def test_open(self):
        pass
    
    def test_save(self):
        pass
    
    def test_close(self):
        pass
    
    def test_save_close_command(self):
        pass
    
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