# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 20:24:55 2021

@author: Ronald Kemker
"""


import tkinter as tk
from tkinter import Frame, Label, StringVar, OptionMenu, Button

class OptionPrompt(object):
    
    def __init__(self, root_app):
        '''
        Popup for a New Project Wizard GUI.
        
        Parameters
        ----------
        root_app : Pass a pointer to the Main App object to access parent
                   variables.
        
        Returns
        -------
        None.
    
        '''
        
        # Parent AnnotationTool Object
        self.root_app = root_app

        # Static Window Dimensions
        self.window_width = 600
        self.window_height = 400
        
    def draw_window(self):
        '''
        Draws the Option Menu Window
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None.
    
        '''
        
        # Popup for the Option Menu
        self.option_window = tk.Toplevel()
        self.option_window.grab_set()
        self.option_window.wm_title("Options")
        self.option_window.geometry("%dx%d" % (self.window_width,
                                               self.window_height))
        
        # Window Background Frame
        self.background = Frame(self.option_window, 
                                width = self.window_width,
                                height = self.window_height,
                                bg='white') 
        self.background.place(x=0, y=0, width = self.window_width, 
                              height=self.window_height)
        
        
        # Build the Interface (Drop-Down Menu) for the Window Resize Function
        label = Label(self.background, text='Option Menu', 
                      font='Helvetica 12 bold', 
                      bg='white')
        label.place(x=self.window_width/2 - 30, y= 10)
        
        label = Label(self.background, text='Window Size',
                      font='Helvetica 10 bold', 
                      bg='white')
        label.place(x= 10, y= 50)
        
        self.selected_size = StringVar(self.background)
        self.selected_size.set(self.root_app.window_size_strings[self.root_app.window_size_index])
        option_menu = OptionMenu(self.background, 
                                 self.selected_size,
                                 *self.root_app.window_size_strings)
        option_menu.place(x=110, 
                          y=50, 
                          width = 100, 
                          height = 25)        

        # Ok/Cancel Buttons
        button = Button(self.background, text='Ok', command=self.ok_button)
        button.place(x=self.window_width/2 - 110, y= self.window_height - 50, 
                     width = 100, height=25)

        button = Button(self.background, text='Cancel', 
                        command=self.option_window.destroy)
        button.place(x=self.window_width/2 + 10, y= self.window_height - 50, 
                     width = 100, height=25)
        
        return True
        
    def ok_button(self):
        '''
        Popup for a New Project Wizard GUI.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None.
    
        '''
        
        # Resize the Main App Window
        new_size_string = self.selected_size.get()
        self.option_window.destroy()
        self.root_app.window_size_index = \
            self.root_app.window_size_strings.index(new_size_string)
        self.root_app.window.geometry(new_size_string)
        new_size = new_size_string.split("x")
        self.root_app.window_width = int(new_size[0])
        self.root_app.window_height = int(new_size[1])
        self.root_app.canvas_width = self.root_app.window_width -\
            self.root_app.navigator_width
        self.root_app.canvas_height = self.root_app.window_height -\
            self.root_app.toolbar_height
        
        # Redraw the Window
        self.root_app._draw_workspace()
        
        return True