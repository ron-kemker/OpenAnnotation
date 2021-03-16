# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 08:19:21 2021

@author: Ronald Kemker
"""

from tkinter import Frame, Label, Button, StringVar, OptionMenu
from PIL import ImageTk, Image, ImageOps
from navigator import Navigator

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
        self.toolbar_width = self.root_app.window_width
        self.toolbar_height = self.root_app.toolbar_height
        
        # Tool Bar Frame
        self.toolbar_frame = Frame(self.root_app.background, 
                                   bg='gray',
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
        None
        
        Raises
        ------
        None        
        
        Returns
        -------
        None
            
        '''    

        button_size = 40
        
        nav_frame = Frame(self.toolbar_frame, 
                          width = self.root_app.navigator_width,
                          height = self.toolbar_height)
        
        nav_frame.place(x=self.root_app.canvas_width-20,
                        y=0, 
                        width = self.root_app.navigator_width,
                        height = self.toolbar_height
                        )
        
        nav_text_label = Label(nav_frame, 
                                font='Helvetica 12 bold',
                                justify='center',
                                text="Page %d/%d" % (self.root_app.page+1, 
                                               self.root_app.num_pages+1))
        nav_text_label.place(x=0, y=5, 
                                  width=self.root_app.navigator_width, 
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
                                    bg='black', command=self.next_page)
        right_button.image = right_photo
        right_button.place(x=150, 
                                y=5, 
                                width=button_size, 
                                height=button_size)
        

        left_button = Button(nav_frame, image=left_photo, 
                        bg='black', command=self.previous_page)
        left_button.image = left_photo
        left_button.place(x=10, 
                                y=5, 
                                width=button_size, 
                                height=button_size)
        

    def next_page(self):
        self.root_app.page = min(self.root_app.page + 1, self.root_app.num_pages)
        self.root_app._draw_workspace()
    
    def previous_page(self):
        self.root_app.page = max(self.root_app.page - 1, 0)
        self.root_app._draw_workspace()


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
        
        button_size = 40


        if self.root_app.window.winfo_ismapped():
            img = Image.open('img/delete.png')
            photo = ImageTk.PhotoImage(img.resize((button_size-1, 
                                                   button_size-1), 
                                              Image.ANTIALIAS)) 
        else:
            photo = None
               
        button = Button(self.toolbar_frame,
                            image = photo,
                            command=self._delete_from_project,
                            width = button_size,
                            height = button_size)
        button.image = photo
        
        
        button.place(x=10, 
                     y=5, 
                     width=button_size, 
                     height=button_size)


    
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
        
        for idx in self.root_app.annotations[self.root_app.current_file].label:
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
               
        self.root_app.selected_class = StringVar(self.toolbar_frame)
        self.root_app.selected_class.set(self.root_app.class_list[0])
        option_menu = OptionMenu(self.toolbar_frame, self.root_app.selected_class,
                                 *self.root_app.class_list)
    
        option_menu.place(x=60, 
                          y=5, 
                          width = 100, 
                          height = 40)