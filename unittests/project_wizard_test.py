# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 18:13:42 2021

@author: Ronald Kemker
"""

import unittest
from AnnotationTool import AnnotationTool
from project_wizard import ProjectWizard
from fileio import Annotation, ROI
from menu import AppMenu

class MockMeta(object):
    def __init__(self, orientation):
        self.has_exif = True
        self.orientation = orientation

class MockImg(object):
    def __init__(self, x=640, y=480):
        self.size = [x, y]
        
class TestProjectWizard(unittest.TestCase):
    
    def test_init(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        menu = AppMenu(tool)
        tool.annotations = []
        tool.class_list = []
        
        wizard = ProjectWizard(menu)
        self.assertTrue(hasattr(wizard, 'root_app'))
        self.assertEqual(tool, wizard.root_app)
        self.assertTrue(hasattr(wizard, 'menu_app'))
        self.assertTrue(hasattr(wizard, 'window_width'))
        self.assertTrue(hasattr(wizard, 'window_height'))
        self.assertTrue(hasattr(wizard, 'left_pane_width'))
        self.assertTrue(hasattr(wizard, 'right_pane_width'))
        self.assertEqual(wizard.window_width, 1024)
        self.assertEqual(wizard.window_height, 768)
        self.assertEqual(wizard.left_pane_width, 300)
        self.assertEqual(wizard.right_pane_width, 723)

        self.assertTrue(hasattr(wizard, 'wizard_window'))
        self.assertTrue(hasattr(wizard, 'background'))
        self.assertEqual(wizard.background.cget('width'), 1024)
        self.assertEqual(wizard.background.cget('height'), 768)
        
    def test_draw_left_pane(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        menu = AppMenu(tool)
        tool.annotations = []
        tool.class_list = []
        
        wizard = ProjectWizard(menu)
        self.assertTrue(hasattr(wizard, 'left_pane'))
        
        children = wizard.left_pane.winfo_children()
        
        self.assertEqual(len(children), 5)
        self.assertEqual(children[0].cget('text'), 
                         'Import File(s) to Project')
        self.assertEqual(children[1].cget('text'), 
                         'Import Entire Directory to Project')
        self.assertEqual(children[2].cget('text'), 
                         'Project has 0 files for annotation.')
        self.assertEqual(children[3].cget('text'), 
                         'Build Project')        
        self.assertEqual(children[4].cget('text'), 
                         'Main Menu')        


    def test_draw_right_pane(self):
        
        tool = AnnotationTool()
        tool.load_app(True) 
        menu = AppMenu(tool)
        tool.annotations = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 5, 5]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']
        
        wizard = ProjectWizard(menu)
        self.assertTrue(hasattr(wizard, 'right_pane'))
        
        children = wizard.right_pane.winfo_children()
        
        self.assertEqual(len(children), 5)
        self.assertEqual(children[0].cget('text'), 
                         'Object Class Manager')

        for i in range(3):
            child = children[i+1].winfo_children()
            self.assertEqual(child[0].cget('text'), 
                         '%d. %s' % (i+1, tool.class_list[i]))            
            self.assertEqual(child[1].cget('bg'), tool.colorspace[i])    
            self.assertEqual(child[2].cget('text'), 'Rename')    
            self.assertEqual(child[3].cget('text'), 'Delete')                

        child = children[-1].winfo_children()
        self.assertEqual(child[1].cget('text'), 'Add Class')                
        
            
    def test_choose_color(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        menu = AppMenu(tool)
        tool.annotations = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 5, 5]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']
        
        wizard = ProjectWizard(menu)
        
        self.assertEqual(len(tool.top_colors_used) , 3)
        self.assertEqual(len(tool.top_colors_free) , 3)
         
        wizard._choose_color(0)
        
        self.assertEqual(tool.colorspace[0], '#EEEEEE')
        self.assertEqual(tool.colorspace[1], '#FF0000')
        self.assertEqual(len(tool.top_colors_used) , 2)
        self.assertEqual(len(tool.top_colors_free) , 4)
        self.assertEqual(tool.top_colors_free[0], '#0000FF')
        
        wizard._choose_color(1)
        self.assertEqual(tool.colorspace[0], '#EEEEEE')
        self.assertEqual(tool.colorspace[1], '#EEEEEE')
        self.assertEqual(len(tool.top_colors_used) , 1)
        self.assertEqual(len(tool.top_colors_free) , 5)
        self.assertEqual(tool.top_colors_free[0], '#FF0000') 
        
    def test_import_file(self):
        tool = AnnotationTool()
        tool.load_app(True)
        tool.annotations = []
        tool.file_list = []
        tool.current_file = 0
        tool.class_list = []
        tool.img = MockImg(640, 480)

        appMenu = AppMenu(tool)
        wizard = ProjectWizard(appMenu)
        
        complete = wizard._import_file(('test.jpg', ), MockMeta(6))
        self.assertTrue(complete)
        self.assertEqual(len(tool.annotations), 1)

        complete = wizard._import_file(('test2.jpg', ), MockMeta(6))
        self.assertTrue(complete) 
        self.assertEqual(len(tool.annotations), 2)

        complete = wizard._import_file(('test.jpg', ), MockMeta(6))
        self.assertTrue(complete) 
        self.assertEqual(len(tool.annotations), 2)

        complete = wizard._import_file(('test.png', ), MockMeta(6))
        self.assertTrue(complete) 
        self.assertEqual(len(tool.annotations), 3)

        complete = wizard._import_file('', MockMeta(6))
        self.assertFalse(complete) 
        self.assertEqual(len(tool.annotations), 3)

                                
    def test_import_files_in_directory(self):
        tool = AnnotationTool()
        tool.load_app(True)
        tool.annotations = [Annotation(), Annotation(), Annotation()]
        tool.file_list = ['file1.jpg', 'file2.jpg', 'file3.png']
        tool.current_file = 0
        tool.class_list = []
        tool.img = MockImg(640, 480)

        appMenu = AppMenu(tool)
        wizard = ProjectWizard(appMenu)        

        complete = wizard._import_files_in_directory('path/',MockMeta(6))
        self.assertTrue(complete)
        self.assertEqual(len(tool.annotations), 3)

        complete = wizard._import_files_in_directory('path/', MockMeta(6))
        self.assertTrue(complete) 
        self.assertEqual(len(tool.annotations), 3)

        complete = wizard._import_files_in_directory('', MockMeta(6))
        self.assertFalse(complete) 
        self.assertEqual(len(tool.annotations), 3)
          
    def test_rename_class_action(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 15, 501]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']

        appMenu = AppMenu(tool)
        wizard = ProjectWizard(appMenu)  
        
        self.assertEqual(tool.class_list[0], 'winston' )

        wizard._rename_class_window(0)
        wizard.rename_class_var.set('')
        wizard._rename_class_action(0)
        
        self.assertEqual(tool.class_list[0], 'winston' )

        wizard._rename_class_window(0)
        wizard.rename_class_var.set('TestRename')
        wizard._rename_class_action(0)
        
        self.assertEqual(tool.class_list[0], 'TestRename' ) 
                           
    def test_rename_class_window(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 15, 501]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']
        
        appMenu = AppMenu(tool)
        wizard = ProjectWizard(appMenu)          
        
        wizard._rename_class_window(0)

        self.assertTrue(hasattr(wizard, 'rename_entry'))  
        self.assertTrue(hasattr(wizard, 'rename_class_prompt'))  

        frame_children = wizard.rename_class_prompt.winfo_children()[0] \
            .winfo_children()
        self.assertEqual(len(frame_children), 4)
        self.assertEqual(frame_children[0].cget("text"), 
                         'Rename \"winston\" Class to:')
        self.assertEqual(frame_children[2].cget("text"), "Ok")
        self.assertEqual(frame_children[3].cget("text"), "Cancel")
        
        wizard._rename_class_window(1)

        self.assertTrue(hasattr(wizard, 'rename_entry'))  
        self.assertTrue(hasattr(wizard, 'rename_class_prompt'))  

        frame_children = wizard.rename_class_prompt.winfo_children()[0] \
            .winfo_children()
        self.assertEqual(len(frame_children), 4)
        self.assertEqual(frame_children[0].cget("text"), 
                         'Rename \"prince\" Class to:')
        self.assertEqual(frame_children[2].cget("text"), "Ok")
        self.assertEqual(frame_children[3].cget("text"), "Cancel")     
    
    
    def test_add_class(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []

        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        tool.class_count = [5, 15, 501]        
        
        tool.top_colors_free = ['#00FFFF', '#FF00FF', '#FFFF00']
        tool.top_colors_used = ['#0000FF', '#FF0000', '#00FF00']

        appMenu = AppMenu(tool)
        wizard = ProjectWizard(appMenu)  
        
        self.assertEqual(tool.class_list[-1], 'duckie' )

        wizard._draw_right_pane()
        wizard.new_class_var.set('')
        wizard._add_class_action()
        
        self.assertEqual(tool.class_list[-1], 'duckie' )

        wizard._draw_right_pane()
        wizard.new_class_var.set('winston')
        wizard._add_class_action()
        
        self.assertEqual(tool.class_list[-1], 'duckie' ) 

        wizard._draw_right_pane()
        wizard.new_class_var.set('TestAdd')
        wizard._add_class_action()
        
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

        appMenu = AppMenu(tool)
        wizard = ProjectWizard(appMenu)          
        
        self.assertFalse(hasattr(wizard, 'popup_window'))
        wizard._check_before_remove(0)
        self.assertTrue(hasattr(wizard, 'popup_window'))

        frame_children = wizard.popup_window.winfo_children()[0]. \
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

        appMenu = AppMenu(tool)
        wizard = ProjectWizard(appMenu)  
        
        self.assertEqual(tool.class_list[-1], 'duckie' )

        wizard._draw_right_pane()
        wizard._remove_class(2)
        
        self.assertEqual(tool.class_list[-1], 'prince' ) 
        self.assertEqual(tool.class_count[-1], 15)
        self.assertEqual(tool.colorspace[-1], '#FF0000')
        self.assertEqual(len(tool.top_colors_used) , 2)
        self.assertEqual(len(tool.top_colors_free) , 4)

        
    def test_cancel_project(self):
        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        
        
        appMenu = AppMenu(tool)
        wizard = ProjectWizard(appMenu) 
        
        self.assertTrue(tool.saved)
        self.assertTrue(wizard.wizard_window.winfo_exists())
        wizard._cancel_project()
        self.assertTrue(tool.saved)
        self.assertFalse(wizard.wizard_window.winfo_exists())

    def test_build_project(self):

        tool = AnnotationTool()
        tool.load_app(True) 
        tool.annotations = []
        tool.class_list = ['winston', 'prince', 'duckie']
        tool.colorspace = ['#0000FF', '#FF0000', '#00FF00']
        
        
        appMenu = AppMenu(tool)
        wizard = ProjectWizard(appMenu) 
        
        self.assertTrue(tool.saved)
        self.assertTrue(wizard.wizard_window.winfo_exists())
        wizard._build_project()
        self.assertFalse(tool.saved)
        self.assertFalse(wizard.wizard_window.winfo_exists())
            
if __name__ == '__main__':
    unittest.main()
