# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 08:49:14 2021

@author: Ronald Kemker
"""


import tkinter as tk
from tkinter import Frame, Label, Button
from glob import glob

class HelpMenu(object):
    
    def __init__(self, root_app):
        '''
        This is the Help Menu that comes up when clicking "Help->
        OpenAnnotation Documentation" in the menu toolbar.  
        
        Note: The help files that load here are located in data/help.  They
        are .txt format.  The first line is the title that is loaded into the
        button on the left pane.

        Parameters
        ----------
        root_app : AnnotationTool Object
            This is the Parent Object.

        Returns
        -------
        None.

        '''
        self.root = root_app # AnnotationTool object
        self.window_width = 1024
        self.window_height = 768
        self.left_pane_width = 300
        self.right_pane_width = self.window_width - self.left_pane_width - 1

    def _draw_menu(self):
        '''
        Initial Draw of the HelpMenu

        Returns
        -------
        None.

        '''
        
        # Popup Window
        self.window = tk.Toplevel()
        self.window.wm_title("OpenAnnotation Help")
        self.window.geometry("%dx%d" % (self.window_width,
                                        self.window_height))          
        
        # Gray Background
        self.background = Frame(self.window, 
                                bg='gray',
                                width=self.window_width,
                                height=self.window_height)
        
        self.background.pack()
        
        # Navigation toolbar on the left
        left_pane = Frame(self.background, width=self.left_pane_width,
                               height = self.window_height, bg='white')
        left_pane.place(x=0, y=0, width=self.left_pane_width, 
                             height=self.window_height)
        
        # Text from the individual tutorial goes on the right.
        self.right_pane = Frame(self.background, width=self.right_pane_width,
                               height = self.window_height, bg='white')
        self.right_pane.place(x=self.left_pane_width+1, 
                              y=0, 
                              width=self.right_pane_width, 
                              height=self.window_height)
        
        # Open the .txt file containing the tutorial item
        if self.root.window.winfo_ismapped():
            self.help_files = glob('data/help/*.txt')
        else:
            self.help_files = glob('../data/help/*.txt')
           
        
        label = Label(left_pane, 
                      text='Navigation Bar', 
                      bg='white', 
                      width=self.left_pane_width,
                      justify='left',
                      font=('Arial', 14, 'bold'),
                      anchor='nw')
        label.place(x=10, y=10, width=self.left_pane_width, 
                    height=self.window_height)
        
        for i, file in enumerate(self.help_files):
            
            # Load the text file
            f = open(file, 'r')
            lines = f.readlines()
            f.close()
            
            # Add a Navigation Button on the left
            button = Button(left_pane, 
                          text="\u2022  "+lines[0][:-1],
                          width=self.left_pane_width, 
                          justify='left',
                          font=('Arial', 12),
                          anchor='w',
                          command= lambda i=i: self._button_press(i),
                          activebackground = 'gray',
                          activeforeground = 'white',
                          bg='white',
                          fg = 'blue',
                          relief="flat")
            button.place(x=10, 
                        y=40+i * 25,
                        width=self.left_pane_width,
                        height=25)
            
            # Start with the default "New Project Tutorial"
            if i == 0:
                title = Label(self.right_pane, 
                              text=lines[0][:-1],
                              width=self.right_pane_width, 
                              justify='left',
                              font=('Arial', 14, 'bold'),
                              anchor='nw',
                              bg='white')
                title.place(x=10, y=10, width=self.right_pane_width, 
                           height=self.window_height)
                
                body = Label(self.right_pane, 
                              text=''.join(lines[1:]),
                              width=self.right_pane_width, 
                              justify='left',
                              font=('Arial', 12),
                              anchor='nw',
                              bg='white')
                body.place(x=10, y=35, width=self.right_pane_width, 
                           height=self.window_height)
            
    def _button_press(self, button_id):
        '''
        Update the right frame when one of the buttons in the navigation pane
        is clicked

        Parameters
        ----------
        button_id : INTEGER
            This is the index from the corresponding button on the left.

        Returns
        -------
        None.

        '''
        
        # Open up the file
        f = open(self.help_files[button_id], 'r')
        lines = f.readlines()
        f.close()        

        # Update the right pane with the corresponding text
        title = Label(self.right_pane, 
                      text=lines[0][:-1],
                      width=self.right_pane_width, 
                      justify='left',
                      font=('Arial', 14, 'bold'),
                      anchor='nw',
                      bg='white')
        title.place(x=10, y=10, width=self.right_pane_width, 
                   height=self.window_height)
        
        body = Label(self.right_pane, 
                      text=''.join(lines[1:]),
                      width=self.right_pane_width, 
                      justify='left',
                      font=('Arial', 12),
                      anchor='nw',
                      bg='white')
        body.place(x=10, y=35, width=self.right_pane_width, 
                   height=self.window_height)
         