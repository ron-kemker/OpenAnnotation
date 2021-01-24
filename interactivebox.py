# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 08:01:15 2021

@author: Ronald Kemker
"""

import tkinter as tk
from PIL import ImageTk, Image

class InteractiveBox(object):

    def __init__(self, left, top, right, bottom, color, line_width=5):
        '''
        This is the canvas tool where the image and annotations are drawn on.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None.
    
        '''    
        
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.color = color
        
        self.close_button_size = 20
        self.line_width = line_width
        
        self.height = self.bottom - self.top + self.line_width
        self.width = self.right - self.left + self.line_width
                
    def draw_box(self, root_app, box_id):
        
        self.root_app = root_app
        canvas = root_app.canvas
        self.image_id = root_app.current_file
        self.box_id = box_id
        
        self.rect = canvas.create_rectangle(self.left,
                                self.top,
                                self.right,
                                self.bottom,
                                outline=self.color,
                                width=self.line_width)
        
        close_window_img = Image.open('img/close_window.jpg')
        close_window_img = close_window_img.crop((100,100,720,720))

        sz = self.close_button_size

        photo = ImageTk.PhotoImage(close_window_img.resize((sz,sz), 
                                              Image.ANTIALIAS))        
        
        self.close_button = tk.Button(canvas, 
                        width = self.close_button_size, 
                        height = self.close_button_size,
                        image=photo, 
                        command=lambda box_id=box_id: self.delete_box(box_id),
                        relief='flat',
                        bg=None)
        self.close_button.image = photo
        
        self.close_button.place(x = self.right - self.close_button_size - 2*self.line_width,
                     y = self.top+self.line_width)
       
    
    def right_clicked(self, x, y):
        line_width_half = int(self.line_width / 2)

        if x > self.right-line_width_half and\
            x <= self.right-line_width_half+self.line_width and\
            y > self.top-line_width_half and\
            y <= self.top-line_width_half+self.height:
                return True
            
        else:
            return False

    def left_clicked(self, x, y):
        line_width_half = int(self.line_width / 2)

        if x > self.left-line_width_half and\
            x <= self.left-line_width_half+self.line_width and\
            y > self.top-line_width_half and\
            y <= self.top-line_width_half+self.height:
                return True
            
        else:
            return False

    def top_clicked(self, x, y):
        line_width_half = int(self.line_width / 2)

        if x > self.left-line_width_half and\
            x <= self.left-line_width_half+self.width and\
            y > self.top-line_width_half and\
            y <= self.top-line_width_half+self.line_width:
                return True
            
        else:
            return False

    def bottom_clicked(self, x, y):
        line_width_half = int(self.line_width / 2)

        if x > self.left-line_width_half and\
            x <= self.left-line_width_half+self.width and\
            y > self.bottom-line_width_half and\
            y <= self.bottom-line_width_half+self.line_width:
                return True
            
        else:
            return False
      
    def delete_box(self, box_id):
        lbl = self.root_app.annotations[self.image_id].label[box_id]
        self.root_app.annotations[self.image_id].bbox.pop(box_id)
        self.root_app.annotations[self.image_id].label.pop(box_id)
        self.root_app.class_count[lbl] = self.root_app.class_count[lbl] - 1
        self.root_app._draw_workspace()        