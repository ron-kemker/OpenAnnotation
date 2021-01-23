# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:26:18 2020

@author: Ronald Kemker
"""

import tkinter as tk
from tkinter import Frame, Button, Canvas
from PIL import ImageTk, Image

from menu import AppMenu
from objectclassmanager import ObjectClassManager
from toolbar import Toolbar
from interactivebox import InteractiveBox

class AnnotationTool(object):
    
    def __init__(self, file_ext = ['.jpg']):
        '''

        Parameters
        ----------
        file_ext : LIST of STRINGs, optional
            The file extension of the images being imported. The default is 
            ['.jpg'].

        Returns
        -------
        None.

        '''
        
        self.class_list = []
        self.file_ext = file_ext
        self.window_width = 1024
        self.window_height = 768
        self.toolbar_width = 150
        self.image_frame_width = self.window_width - self.toolbar_width
        self.current_file = 0
        self.project_open = False
        self.saved = True
        self.app_menu = AppMenu(self)

        self.colorspace = {}
        self.top_colors = ['Blue', 'Red', 'Green', 'Cyan', 'Magenta', 
                           'Yellow'] 
        self.top_colors_free = self.top_colors.copy()
        self.top_colors_used = []

    def load_app(self):
        
        # Build Window
        self.window = tk.Tk()
        self.window.title("Image Annotation Tool")  # to define the title
        self.window.geometry("%dx%d" % (self.window_width,self.window_height))
        self.app_menu._draw_menu()
                   
        self.background = Frame(self.window,
                                width=self.window_width,
                                height=self.window_height)
        self.background.pack()
                
        # Create Load Screen Buttons
        new_button = Button(self.background, text="New Project", width = 20,
                            height=3, 
                            command=self.app_menu._new)
        new_button.grid(row=0, column=0, sticky='n', pady=2 )

        load_button = Button(self.background, text="Load Project", width=20,
                            height=3, 
                            command=self.app_menu._open)
        load_button.grid(row=1, column=0, sticky='n', pady=2  )

        quit_button = Button(self.background, text="Quit", width=20, 
                             height=3, 
                            command=self.app_menu._quit)
        quit_button.grid(row=2, column=0, sticky='n', pady=2  )
        
        self.window.mainloop()
        
    def _draw_object_class_manager(self):
        
        obj_mgr = ObjectClassManager(self)
        
    def _draw_workspace(self):
        
        self.app_menu._draw_menu()
        
        self.background.destroy()
        
        # Build Background Frame                       
        self.background = Frame(self.window,
                                bg="black",
                                width=self.window_width,
                                height=self.window_height)
        self.background.pack()

        # Draw Toolbar on Left
        toolbar = Toolbar(self)
        
        # Draw Canvas on Right        
        self.canvas_frame = Frame(self.background, bg='green',
                    width=self.image_frame_width,
                    height=self.window_height)
        self.canvas_frame.grid(column=1, row=0)        
        
        self.aspect_ratio = max(self.img.size[0]/(self.image_frame_width),
                                self.img.size[1]/(self.window_height)) 
                            
        new_size = (int(self.img.size[0]/self.aspect_ratio), 
                    int(self.img.size[1]/self.aspect_ratio))
        
        
        
        self.canvas = Canvas(self.canvas_frame,
                                   width=self.image_frame_width, 
                                   height=self.window_height)
        self.canvas.pack()
        
        pil_img = ImageTk.PhotoImage(self.img.resize(new_size, 
                                              Image.ANTIALIAS))
        self.canvas.image = pil_img
        self.canvas.create_image(0, 0, anchor=tk.NW, image=pil_img)
        
        self.boxes = []
        
        for i, label in enumerate(self.annotations[self.current_file].bbox):
            
            left = label[1] / self.aspect_ratio
            top = label[0] / self.aspect_ratio
            right = label[3] / self.aspect_ratio
            bottom = label[2] / self.aspect_ratio
            color = self.colorspace[label[-1]]
            
            box = InteractiveBox(left, top, right, bottom, color)
            box.draw_box(self, i)
            self.boxes.append(box)
            
        # Only allow bounding boxes to be drawn if they can be tied to a class
        if len(self.class_list):        
            self.canvas.bind("<Button-1>",self._on_click)
            self.canvas.bind("<ButtonRelease-1>",self._on_release)
            self.canvas.bind("<B1-Motion>", self._on_move_press)


    def _on_click(self, event):
        
        self.clicked = (event.x, event.y)
        
        for i, box in enumerate(self.boxes):
            if box.right_clicked(self.clicked[0], self.clicked[1]):
                self.box_resize_mode = 'RIGHT'
                self.resize_box_id = i
                return
            elif box.left_clicked(self.clicked[0], self.clicked[1]):
                self.box_resize_mode = 'LEFT'
                self.resize_box_id = i
                return
            elif box.top_clicked(self.clicked[0], self.clicked[1]):
                self.box_resize_mode = 'TOP'
                self.resize_box_id = i
                return
            elif box.bottom_clicked(self.clicked[0], self.clicked[1]):
                self.box_resize_mode = 'BOTTOM'
                self.resize_box_id = i
                return
        
        self.box_resize_mode = 'NEW'
        
    def _on_release(self, event):
        
        if self.box_resize_mode == 'NEW':

            top = min(self.clicked[1], event.y)
            bottom = max(self.clicked[1], event.y)
            left = min(self.clicked[0], event.x)
            right = max(self.clicked[0], event.x)
            label = self.selected_class.get()
            color = self.colorspace[self.selected_class.get()]
            
            box = InteractiveBox(left, top, right, bottom, color)
            
            self.canvas.delete(self.rect)
            del self.rect
            box.draw_box(self, len(self.annotations[self.current_file].bbox))
            
            top = self.aspect_ratio * top
            bottom = self.aspect_ratio * bottom
            left = self.aspect_ratio * left
            right = self.aspect_ratio * right
            
            self.annotations[self.current_file].add_label(top, 
                                                          left, 
                                                          bottom, 
                                                          right, 
                                                          label)
            
        self._draw_workspace()
        self.saved = False
        self.box_resize_mode = 'NEW'
        
    def _on_move_press(self, event):
        
        if hasattr(self, 'resize_box_id'):
            box_id = self.resize_box_id
        
        if self.box_resize_mode != 'NEW':
            if hasattr(self.boxes[box_id],'close_button'):
                self.boxes[box_id].close_button.destroy()
               
        if self.box_resize_mode == 'RIGHT':
            self.canvas.coords(self.boxes[box_id].rect, 
                   self.boxes[box_id].left, 
                   self.boxes[box_id].top,
                   event.x,
                  self.boxes[box_id].bottom)
            self.boxes[box_id].right = event.x
            self.annotations[self.current_file].bbox[box_id][3] = event.x
        elif self.box_resize_mode == 'LEFT':
            self.canvas.coords(self.boxes[self.resize_box_id].rect, 
                   event.x, 
                   self.boxes[self.resize_box_id].top,
                   self.boxes[self.resize_box_id].right,
                   self.boxes[self.resize_box_id].bottom)
            self.boxes[self.resize_box_id].left = event.x
            self.annotations[self.current_file].bbox[box_id][1] = event.x
        elif self.box_resize_mode == 'TOP':
            self.canvas.coords(self.boxes[self.resize_box_id].rect, 
                   self.boxes[self.resize_box_id].left, 
                   event.y,
                   self.boxes[self.resize_box_id].right,
                   self.boxes[self.resize_box_id].bottom)
            self.boxes[self.resize_box_id].top = event.y
            self.annotations[self.current_file].bbox[box_id][0] = event.y
        elif self.box_resize_mode == 'BOTTOM':
            self.canvas.coords(self.boxes[self.resize_box_id].rect, 
                   self.boxes[self.resize_box_id].left, 
                   self.boxes[self.resize_box_id].top,
                   self.boxes[self.resize_box_id].right,
                   event.y)
            self.boxes[self.resize_box_id].bottom = event.y
            self.annotations[self.current_file].bbox[box_id][2] = event.y

        elif not hasattr(self, 'rect'):
    
            color = self.colorspace[self.selected_class.get()]
            self.rect = self.canvas.create_rectangle(self.clicked[0], 
                                                     self.clicked[1], 
                                                     self.clicked[0], 
                                                     self.clicked[1], 
                                                     width=5,
                                                     outline=color)
        else:
            self.box_end = (event.x, event.y)
            self.canvas.coords(self.rect, 
                               self.clicked[0], 
                               self.clicked[1],
                               event.x,
                               event.y)
        
    def _load_image_from_file(self):
        self.img = Image.open(self.file_list[self.current_file])
        
        self.file_list[self.current_file]
        
        rot = self.annotations[self.current_file].rotation
        self.img = self.img.transpose(rot)
                
    def _reset_image(self):
        self.annotations[self.current_file].label = []
        self.annotations[self.current_file].bbox = []
        self._draw_workspace()
        

    
if __name__ == "__main__":
    
    tool = AnnotationTool()
    tool.load_app()