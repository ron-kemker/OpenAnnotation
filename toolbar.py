# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 08:19:21 2021

@author: Master
"""


import tkinter as tk
from tkinter import Frame, Label, Button, StringVar, OptionMenu
from PIL import ImageTk, Image, ImageOps


class Toolbar(object):
    
    def __init__(self, root_app):
        self.root_app = root_app
        self.toolbar_width = self.root_app.toolbar_width
        self.toolbar_height = self.root_app.window_height
        
        # Tool Bar Frame
        self.toolbar_frame = Frame(self.root_app.background, 
                                   bg='blue',
                                   width=self.toolbar_width,
                                   height=self.toolbar_height)
        self.toolbar_frame.grid(column=0, row=0, sticky='NW')
        
        # Draw Tools
        self._draw_image_navigator()
        # self._draw_rotation_menu()
        self._delete_from_project_button()
        self._reset_image_button()
        
        if len(self.root_app.class_list) > 0:
            self._draw_class_selection_menu()
            
            
    def _draw_rotation_menu(self):
        
        rot_frame = Frame(self.toolbar_frame, 
                                     bg=None, 
                                     width=self.toolbar_width,
                                     height = 50,
                                     pady = 10, 
                                     padx = 10)
        rot_frame.grid(column=0, row=1)
        
        label = Label(rot_frame, text="Image Rotation:", bg=None)
        label.grid(row=0, column=0, columnspan=3)
        
        right_arrow = Image.open('img/right_curve_arrow.png')
        left_arrow = ImageOps.mirror(right_arrow)      
        
        
        photo = ImageTk.PhotoImage(right_arrow.resize((30,30), 
                                              Image.ANTIALIAS))
        self.right_button = Button(rot_frame, image=photo, 
                                   bg='white', command=self._rotate_right)
        self.right_button.image = photo
        self.right_button.grid(row=1, column=2)
        
        left_arrow = ImageOps.mirror(right_arrow)      
        photo = ImageTk.PhotoImage(left_arrow.resize((30,30), 
                                              Image.ANTIALIAS))
        self.left_button = Button(rot_frame, image=photo, 
                       bg='white', command=self._rotate_left)
        self.left_button.image = photo
        self.left_button.grid(row=1, column=0)
        
        self.nav_text_label = Label(rot_frame, bg=None, 
            text="%d°" % self.root_app.annotations[self.root_app.current_file].rotation)
        self.nav_text_label.grid(row=1, column=1)        
    
 
    def _rotate_right(self):
        self.root_app.saved = False
        self.root_app.annotations[self.root_app.current_file].rotation = \
            (self.root_app.annotations[self.root_app.current_file].rotation-90) % 360
        self.root_app._load_image_from_file()  
        self.root_app._draw_workspace()

    def _rotate_left(self):
        self.root_app.saved = False
        self.root_app.annotations[self.root_app.current_file].rotation = \
            (self.root_app.annotations[self.root_app.current_file].rotation+90) % 360
        self.root_app._load_image_from_file()  
        self.root_app._draw_workspace()

       
    def _draw_image_navigator(self):
        
        nav_frame = Frame(self.toolbar_frame, bg=None, 
                                     width=self.toolbar_width, 
                                     height=50,
                                     pady = 10, 
                                     padx=10)
        nav_frame.grid(column=0, row=0)
        
        label = Label(nav_frame, text="Image Navigator:", bg=None)
        label.grid(row=0, column=0, columnspan=3)
        
        left_arrow = Image.open('img/left_arrow.png')
        right_arrow = ImageOps.mirror(left_arrow)      
        
        
        photo = ImageTk.PhotoImage(right_arrow.resize((30,30), 
                                              Image.ANTIALIAS))
        self.right_button = Button(nav_frame, image=photo, 
                                   bg='white', command=self._next_image)
        self.right_button.image = photo
        self.right_button.grid(row=1, column=2)
        
        left_arrow = ImageOps.mirror(right_arrow)      
        photo = ImageTk.PhotoImage(left_arrow.resize((30,30), 
                                              Image.ANTIALIAS))
        self.left_button = Button(nav_frame, image=photo, 
                       bg='white', command=self._previous_image)
        self.left_button.image = photo
        self.left_button.grid(row=1, column=0)
        
        self.nav_text_label = Label(nav_frame, bg=None, 
                                    text="%d/%d" % (self.root_app.current_file+1, 
                                                    len(self.root_app.file_list)))
        self.nav_text_label.grid(row=1, column=1)

    def _next_image(self):
        self.root_app.current_file = min(self.root_app.current_file + 1, 
                                   len(self.root_app.file_list)-1)
        self.root_app._load_image_from_file()  
        self.root_app._draw_workspace()

    def _previous_image(self):
        self.root_app.current_file = max(self.root_app.current_file - 1, 0)
        self.root_app._load_image_from_file()  
        self.root_app._draw_workspace()
    
    def _delete_from_project_button(self):
        
        button = Button(self.toolbar_frame,
                            text="Remove from Project",
                            fg="black",
                            command=self._delete_from_project,
                            pady=10)
        
        button.grid(row=2, column=0, pady=5)
    
    def _delete_from_project(self):
        
        self.root_app.annotations.pop(self.root_app.current_file)
        self.root_app.file_list.pop(self.root_app.current_file)
        self.root_app._load_image_from_file()  
        self.root_app._draw_workspace()
        
        
    def _draw_class_selection_menu(self):
        
        self.root_app.selected_class = StringVar(self.toolbar_frame)
        self.root_app.selected_class.set(self.root_app.class_list[0])
        option_menu = OptionMenu(self.toolbar_frame, 
                                 self.root_app.selected_class,
                                 *self.root_app.class_list)
    
        option_menu.grid(row=3, column=0)
        
    def _reset_image_button(self):
        button = Button(self.toolbar_frame,
                            text="Reset Image",
                            fg="black",
                            command=self._reset_image,
                            pady=10)
        
        button.grid(row=4, column=0, pady=5)        
        
    def _reset_image(self):
        idx = self.root_app.current_file
        self.root_app.annotations[idx].label = []
        self.root_app.annotations[idx].bbox = []
        self.root_app._draw_workspace()


if __name__ == "__main__":
    
    import types    

    root_app = types.SimpleNamespace()
    root_app.window_height = 768
    root_app.toolbar_width = 150
    root_app.current_file = 0
       
    obj_mgr = Toolbar(root_app)
    obj_mgr.class_manager_window.mainloop()
