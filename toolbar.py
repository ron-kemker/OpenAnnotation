# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 08:19:21 2021

@author: Ronald Kemker
"""

from tkinter import Frame, Label, Button, StringVar, OptionMenu
from PIL import ImageTk, Image, ImageOps

class Toolbar(object):
    
    def __init__(self, root_app):
        '''
        Toolbar Class
          
        Parameters
        ----------
        root_app : AnnotationTool object
            Pass Parent Object to access global variables
        
        Attributes
        ----------
        root_app : AnnotationTool object
            Parent Object        
        toolbar_width : int
            Width of the Toolbar
        toolbar_height : int
            Height of the Toolbar
        toolbar_frame : tkinter Frame object
            Fram that contains the entire Toolbar object
        
        Raises
        ------
        None        
        
        Returns
        -------
        None
            
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
          
                
    def _draw_image_navigator(self):
        '''
        Draws the image navigator inside the Toolbar Frame
          
        Parameters
        ----------
        None
        
        Attributes
        ----------
        toolbar_cumulative_height : int
            This is the vertical y-axis index for the lowest widget in the 
            Toolbar project
        
        Raises
        ------
        None        
        
        Returns
        -------
        None
            
        '''    

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

        nav_text_label = Label(nav_frame, bg='black', 
                                font='Helvetica 12 bold',
                                fg='white',
                                text="%d/%d" % (self.root_app.current_file+1, 
                                                len(self.root_app.file_list)))
        nav_text_label.place(x=0, y=top_label_height, 
                                  width=self.toolbar_width, 
                                  height=button_size)        
        
        
        # Only load images when not testing
        if self.root_app.window.winfo_ismapped():
 
            left_arrow = Image.open('img/left_arrow.png')
            right_arrow = ImageOps.mirror(left_arrow)      
            left_photo = ImageTk.PhotoImage(left_arrow.resize((button_size,
                                                               button_size), 
                                              Image.ANTIALIAS))
            right_photo = ImageTk.PhotoImage(right_arrow.resize((button_size,
                                                                 button_size), 
                                                  Image.ANTIALIAS))
        else:
            left_photo = None
            right_photo = None
            
        right_button = Button(nav_frame, image=right_photo, 
                                   bg='black', command=self._next_image)
        right_button.image = right_photo
        right_button.place(x=self.toolbar_width - button_size - 10, 
                                y=top_label_height, 
                                width=button_size, 
                                height=button_size)
        

        left_button = Button(nav_frame, image=left_photo, 
                       bg='black', command=self._previous_image)
        left_button.image = left_photo
        left_button.place(x=10, 
                               y=top_label_height, 
                               width=button_size, 
                               height=button_size)
        

        self.toolbar_cumulative_height = self.toolbar_cumulative_height + \
            nav_frame_height


    def _next_image(self):
        '''
        Moves to the next image in the project
          
        Parameters
        ----------
        None
        
        Attributes
        ----------
        None
        
        Raises
        ------
        None        
        
        Returns
        -------
        None
            
        '''           

        self.root_app.current_file = min(self.root_app.current_file + 1, 
                                   len(self.root_app.file_list)-1)
        self.root_app._load_image_from_file()  
        self.root_app._draw_workspace()


    def _previous_image(self):
        '''
        Moves to the previous image in the project
          
        Parameters
        ----------
        None
        
        Attributes
        ----------
        None
        
        Raises
        ------
        None        
        
        Returns
        -------
        None
            
        '''   
        
        self.root_app.current_file = max(self.root_app.current_file - 1, 0)
        self.root_app._load_image_from_file()  
        self.root_app._draw_workspace()
    
    
    def _delete_from_project_button(self):
        '''
        Draw the Remove Image from Project Button
          
        Parameters
        ----------
        None
        
        Attributes
        ----------
        None
        
        Raises
        ------
        None        
        
        Returns
        -------
        None
            
        '''       
        
        button_width = 120
        button_height = 50
                
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
        '''
        command action tied to the "Remove from Project" button
          
        Parameters
        ----------
        None
        
        Attributes
        ----------
        None
        
        Raises
        ------
        None        
        
        Returns
        -------
        None
            
        '''        
        
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
        '''
        Draw the drop down menu that is used to select which class is being
        currently annotated
          
        Parameters
        ----------
        None
        
        Attributes
        ----------
        selected_class : tkinter StringVar object
            This is the variable assigned to the object class selection drop
            down menu
        
        Raises
        ------
        None        
        
        Returns
        -------
        None
            
        '''       
        
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
        option_menu = OptionMenu(frame, self.root_app.selected_class,
                                 *self.root_app.class_list)
    
        option_menu.place(x=10, 
                          y=label_height, 
                          width = self.toolbar_width - 20, 
                          height = frame_height-label_height)