# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 08:01:15 2021

@author: Ronald Kemker
"""

import tkinter as tk
from PIL import ImageTk, Image

class InteractiveBox(object):

    def __init__(self, root_app, left, top, right, bottom, color, line_width=5):
        '''
        This is the canvas tool where the image and annotations are drawn on.
          
        Parameters
        ----------
        root_app : AnnotationTool object 
            Used to access parent variables.
        left : int
            The left coordinate (x0) in the bounding box
        top : int
            The top coordinate (y0) in the bounding box
        right : int
            The right coordinate (x1) in the bounding box
        bottom : int
            The bottom coordinate (y1) in the bounding box
        color : string or color object
            The color of the bounding box
        line_width : int (Default = 5)
            The line width (in pixels) of the bounding box
            
        Attributes
        ----------
        root_app : AnnotationTool object 
            Used to access parent variables.
        left : int
            The left coordinate (x0) in the bounding box
        top : int
            The top coordinate (y0) in the bounding box
        right : int
            The right coordinate (x1) in the bounding box
        bottom : int
            The bottom coordinate (y1) in the bounding box
        color : string or color object
            The color of the bounding box
        close_button_size : int (Default = 20)    
            The size of the close button in pixels
        line_width : int (Default = 5)
            The line width (in pixels) of the bounding box
        height : int
            The distance between y0 and y1
        width : int
            The distance between x0 and x1
            
        Raises
        ------
        None
    
        Returns
        -------
        None
            
        '''
                
        self.root_app = root_app
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.color = color
        
        self.close_button_size = 20
        self.line_width = line_width
        
        self.height = self.bottom - self.top + self.line_width
        self.width = self.right - self.left + self.line_width
                
    def draw_box(self, box_id):
        '''
        This is the canvas tool where the image and annotations are drawn on.
          
        Parameters
        ----------
        box_id : int
            The integer value assigned to the annotation in the image.  This 
            is used to create the delete annotation "X" in the InteractiveBox.
        close_button : tkinter Button object
            An "X" in the top-right corner of the bounding box.  If clicked,
            this deletes the bounding box.
            
        Attributes
        ----------
        rect : tkinter Rectangle object
            Graphical representation of corresponding bounding box
            
        Raises
        ------
        None
    
        Returns
        -------
        None
            
        '''        
        
        self.rect = self.root_app.canvas.create_rectangle(self.left,
                                self.top,
                                self.right,
                                self.bottom,
                                outline=self.color,
                                width=self.line_width)
        
        if self.root_app.window.winfo_ismapped():
        
            close_window_img = Image.open('img/close_window.jpg')
            close_window_img = close_window_img.crop((100,100,720,720))
    
            sz = self.close_button_size
    
            photo = ImageTk.PhotoImage(close_window_img.resize((sz,sz), 
                                                  Image.ANTIALIAS))        
        else:
            photo = None
            
        self.close_button = tk.Button(self.root_app.canvas, 
                        width = self.close_button_size, 
                        height = self.close_button_size,
                        image=photo, 
                        command=lambda box_id=box_id: self.delete_box(box_id),
                        relief='flat',
                        bg=None)
        self.close_button.image = photo
        
        self.close_button.place(x = self.right - self.close_button_size - \
                           2*self.line_width, y = self.top+self.line_width)
       

    def right_clicked(self, x, y):
        '''
        Did we click somewhere along the right side of the bounding box?
          
        Parameters
        ----------
        x : int
            x-position (in pixels) that corresponds to a mouse click
        y : int
            y-position (in pixels) that corresponds to a mouse click
            
        Attributes
        ----------
        None
            
        Raises
        ------
        None
    
        Returns
        -------
        clicked : boolean
            If clicked on the right edge, return True.  Else, return false.
            
        '''
        
        line_width_half = int(self.line_width / 2)

        if x >= self.right-line_width_half and\
            x < self.right-line_width_half+self.line_width and\
            y >= self.top-line_width_half and\
            y < self.top-line_width_half+self.height:
                return True
            
        else:
            return False

    def left_clicked(self, x, y):
        '''
        Did we click somewhere along the left side of the bounding box?
          
        Parameters
        ----------
        x : int
            x-position (in pixels) that corresponds to a mouse click
        y : int
            y-position (in pixels) that corresponds to a mouse click
            
        Attributes
        ----------
        None
            
        Raises
        ------
        None
    
        Returns
        -------
        clicked : boolean
            If clicked on the left edge, return True.  Else, return false.
            
        '''
        
        line_width_half = int(self.line_width / 2)

        if x >= self.left-line_width_half and\
            x < self.left-line_width_half+self.line_width and\
            y >= self.top-line_width_half and\
            y < self.top-line_width_half+self.height:
                return True
            
        else:
            return False

    def top_clicked(self, x, y):
        '''
        Did we click somewhere along the top side of the bounding box?
          
        Parameters
        ----------
        x : int
            x-position (in pixels) that corresponds to a mouse click
        y : int
            y-position (in pixels) that corresponds to a mouse click
            
        Attributes
        ----------
        None
            
        Raises
        ------
        None
    
        Returns
        -------
        clicked : boolean
            If clicked on the top edge, return True.  Else, return false.
            
        '''        
        
        line_width_half = int(self.line_width / 2)

        if x >= self.left-line_width_half and\
            x < self.left-line_width_half+self.width and\
            y >= self.top-line_width_half and\
            y < self.top-line_width_half+self.line_width:
                return True
            
        else:
            return False

    def bottom_clicked(self, x, y):
        '''
        Did we click somewhere along the bottom side of the bounding box?
          
        Parameters
        ----------
        x : int
            x-position (in pixels) that corresponds to a mouse click
        y : int
            y-position (in pixels) that corresponds to a mouse click
            
        Attributes
        ----------
        None
            
        Raises
        ------
        None
    
        Returns
        -------
        clicked : boolean
            If clicked on the bottom edge, return True.  Else, return false.
            
        '''
        
        line_width_half = int(self.line_width / 2)

        if x >= self.left-line_width_half and\
            x < self.left-line_width_half+self.width and\
            y >= self.bottom-line_width_half and\
            y < self.bottom-line_width_half+self.line_width:
                return True
            
        else:
            return False
      
    def delete_box(self, box_id):
        '''
        Delete the corresponding bounding box
          
        Parameters
        ----------
        box_id : int
            Delete the bounding box corresponding to the annotation at index
            box_id.
            
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

        image_id = self.root_app.current_file
        lbl = self.root_app.annotations[image_id].label[box_id]
        self.root_app.annotations[image_id].pop(box_id)
        self.root_app.class_count[lbl] = self.root_app.class_count[lbl] - 1
        self.root_app._draw_workspace()        