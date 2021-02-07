# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 08:19:21 2021

@author: Ronald Kemker
"""


import tkinter as tk
from tkinter import Frame, Label, Button, StringVar, OptionMenu
from PIL import ImageTk, Image, ImageOps

class Toolbar(object):
    
    def __init__(self, root_app):
        '''
        This is the toolbar on the far left side.
        
        Parameters
        ----------
        root_app : Pass a pointer to the root_application to access "global"
                   variables.
        
        Returns
        -------
        None.
    
        '''            

        self.root_app = root_app
        self.toolbar_width = self.root_app.toolbar_width
        self.toolbar_height = self.root_app.window_height
        
        self.toolbar_cumulative_height = 0
        
        # Tool Bar Frame
        self.toolbar_frame = Frame(self.root_app.background, 
                                   bg='black',
                                   width=self.toolbar_width,
                                   height=self.toolbar_height)
        self.toolbar_frame.place(x=0,
                                 y=0, 
                                 height = self.toolbar_height,
                                 width = self.toolbar_width)
        
        # Draw Tools
        if len(self.root_app.annotations):
            self._draw_image_navigator()
            self._delete_from_project_button()
            
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
        
        button_size = 40
        top_label_height = 20
        nav_frame_height = button_size + top_label_height + 5
        
        nav_frame = Frame(self.toolbar_frame, bg='black', 
                                     width=self.toolbar_width, 
                                     height=nav_frame_height)
        
        nav_frame.place(x=0, y=0, height=nav_frame_height, 
                        width = self.toolbar_width)
        
        label = Label(nav_frame, text="Image Navigator", bg='black',
                      fg='white', font='Helvetica 12 bold')
        label.place(x=0, y=0, height=top_label_height, 
                    width=self.toolbar_width)

        self.nav_text_label = Label(nav_frame, bg='black', 
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    text="%d/%d" % (self.root_app.current_file+1, 
                                                    len(self.root_app.file_list)))
        self.nav_text_label.place(x=0, y=top_label_height, 
                                  width=self.toolbar_width, 
                                  height=button_size)        
        
        left_arrow = Image.open('img/left_arrow.png')
        right_arrow = ImageOps.mirror(left_arrow)      
        
        photo = ImageTk.PhotoImage(right_arrow.resize((button_size,button_size), 
                                              Image.ANTIALIAS))
        self.right_button = Button(nav_frame, image=photo, 
                                   bg='black', command=self._next_image)
        self.right_button.image = photo
        self.right_button.place(x=self.toolbar_width - button_size - 10, 
                                y=top_label_height, 
                                width=button_size, 
                                height=button_size)
        
        left_arrow = ImageOps.mirror(right_arrow)      
        photo = ImageTk.PhotoImage(left_arrow.resize((button_size,button_size), 
                                              Image.ANTIALIAS))
        self.left_button = Button(nav_frame, image=photo, 
                       bg='black', command=self._previous_image)
        self.left_button.image = photo
        self.left_button.place(x=10, 
                               y=top_label_height, 
                               width=button_size, 
                               height=button_size)
        

        self.toolbar_cumulative_height = self.toolbar_cumulative_height + \
            nav_frame_height

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
        
        button_width = 120
        button_height = 50
        
        self
        
        frame = Frame(self.toolbar_frame, bg='black')
        frame.place(x = 0, 
                    y = self.toolbar_cumulative_height,
                    width = self.toolbar_width,
                    height = button_height + 20)
        
        button = Button(frame,
                            text="Remove from Project",
                            fg="black",
                            command=self._delete_from_project)
        
        button.place(x=int(self.toolbar_width/2) - int(button_width/2), 
                     y=10, 
                     width=button_width, 
                     height=button_height)

        self.toolbar_cumulative_height = self.toolbar_cumulative_height + \
            button_height + 20

    
    def _delete_from_project(self):
        
        for lbl in self.root_app.annotations[self.root_app.current_file].label:
            idx = self.class_list.index(lbl)
            self.root_app.class_count[idx] = self.root_app.class_count[idx] - 1
        
        self.root_app.annotations.pop(self.root_app.current_file)
        self.root_app.file_list.pop(self.root_app.current_file)
        
        if self.root_app.current_file == len(self.root_app.file_list):
            self.root_app.current_file = self.root_app.current_file - 1
        
        self.root_app._load_image_from_file()  
        self.root_app._draw_workspace()
        
        
    def _draw_class_selection_menu(self):
        
        frame_height = 70
        label_height = 20
        
        frame = Frame(self.toolbar_frame, bg='black')
        frame.place(x=0,
                    y=self.toolbar_cumulative_height,
                    height=frame_height,
                    width = self.toolbar_width)

        label = Label(frame, 
                      text='Select Class', 
                      bg='black',
                      font='Helvetica 12 bold',
                      fg='white')
        label.place(x=0,y=0, height=label_height, width = self.toolbar_width)
        
        self.root_app.selected_class = StringVar(frame)
        self.root_app.selected_class.set(self.root_app.class_list[0])
        option_menu = OptionMenu(frame, 
                                 self.root_app.selected_class,
                                 *self.root_app.class_list)
    
        option_menu.place(x=10, 
                          y=label_height, 
                          width = self.toolbar_width - 20, 
                          height = frame_height-label_height)