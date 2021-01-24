# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:26:18 2020

@author: Ronald Kemker
"""

import tkinter as tk
from tkinter import Frame, Button, Canvas, Label
from PIL import ImageTk, Image

from menu import AppMenu
from objectclassmanager import ObjectClassManager
from toolbar import Toolbar
from interactivebox import InteractiveBox

class AnnotationTool(object):
    
    def __init__(self):
        '''
        This is the main annotation tool object.  Running this .py file will
        open the application.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        None.

        '''
        
        self.class_list = []
        self.file_ext = ['.jpg', '.png']
        self.window_width = 1024
        self.window_height = 768
        self.toolbar_width = 150
        self.footer_height = 25
        self.canvas_width = self.window_width - self.toolbar_width
        self.canvas_height = self.window_height - self.footer_height
        self.current_file = 0
        self.project_open = False
        self.saved = True
        self.app_menu = AppMenu(self)

        self.colorspace = {}
        self.top_colors = ['Blue', 'Red', 'Green', 'Cyan', 'Magenta', 
                           'Yellow'] 
        self.top_colors_free = self.top_colors.copy()
        self.top_colors_used = []
        self.class_count = {}

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
        new_button = Button(self.background, text="New Blank Project", 
                            width = 20,
                            height=3, 
                            command=self.app_menu._new)
        new_button.grid(row=0, column=0, sticky='n', pady=2 )

        load_button = Button(self.background, text="Load Project", 
                            width=20,
                            height=3, 
                            command=self.app_menu._open)
        load_button.grid(row=1, column=0, sticky='n', pady=2)

        quit_button = Button(self.background, text="Quit", 
                            width=20, 
                            height=3, 
                            command=self.app_menu._quit)
        quit_button.grid(row=2, column=0, sticky='n', pady=2)
        
        self.window.mainloop()
        
    def _draw_object_class_manager(self):
        
        obj_mgr = ObjectClassManager(self)
        
    def _draw_workspace(self):
        
        self.app_menu._draw_menu()
        
        self.background.destroy()
        
        # Build Background Frame                       
        self.background = Frame(self.window,
                                bg="gray",
                                width=self.window_width,
                                height=self.window_height)
        self.background.place(x=0, 
                              y=0,
                              width = self.window_width,
                              height = self.window_height)

        # Draw Toolbar on Left
        toolbar = Toolbar(self)
        
        # Draw Canvas on Right        
        self.canvas_frame = Frame(self.background, bg='green',
                    width=self.canvas_width,
                    height=self.canvas_height)
        self.canvas_frame.place(x=self.toolbar_width,
                                y=0, 
                                width = self.canvas_width,
                                height = self.canvas_height,
                                )
        
        self.canvas = Canvas(self.canvas_frame,
                                   width=self.canvas_width, 
                                   height=self.canvas_height)
        self.canvas.place(x=0,
                         y=0, 
                         width = self.canvas_width,
                         height = self.canvas_height,
                                )
        
        footer_frame = Frame(self.background, 
                             bg='black',
                             height=self.footer_height,
                             width=self.window_width,
                             )
        footer_frame.place(x=0, 
                           y=self.canvas_height, 
                           width=self.window_width,
                           height = self.footer_height)
        
        footer_label = Label(footer_frame, 
                              text='AnnotationTool built by Ron Kemker',
                              fg='white',
                              bg='black')
        footer_label.place(x=0, y=0)
        
        if len(self.annotations):
            self.aspect_ratio = max(self.img.size[0]/(self.canvas_width),
                                    self.img.size[1]/(self.canvas_height)) 
                                
            new_size = (int(self.img.size[0]/self.aspect_ratio), 
                        int(self.img.size[1]/self.aspect_ratio))
        
            pil_img = ImageTk.PhotoImage(self.img.resize(new_size, 
                                                  Image.ANTIALIAS))
            self.canvas.image = pil_img
            self.canvas.create_image(0, 0, anchor=tk.NW, image=pil_img)
            
            self.boxes = []
            
            for i, lbl in enumerate(self.annotations[self.current_file].bbox):
                
                left = lbl[1] / self.aspect_ratio
                top = lbl[0] / self.aspect_ratio
                right = lbl[3] / self.aspect_ratio
                bottom = lbl[2] / self.aspect_ratio
                color = self.colorspace[lbl[-1]]
                
                box = InteractiveBox(left, top, right, bottom, color)
                box.draw_box(self, i)
                self.boxes.append(box)
            
        # Only allow bounding boxes to be drawn if they can be tied to a class
        if len(self.class_list) and len(self.annotations):        
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
            self.class_count[label] = self.class_count[label] + 1
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
            self.annotations[self.current_file].bbox[box_id][3] = event.x \
                * self.aspect_ratio
        elif self.box_resize_mode == 'LEFT':
            self.canvas.coords(self.boxes[self.resize_box_id].rect, 
                   event.x, 
                   self.boxes[self.resize_box_id].top,
                   self.boxes[self.resize_box_id].right,
                   self.boxes[self.resize_box_id].bottom)
            self.boxes[self.resize_box_id].left = event.x
            self.annotations[self.current_file].bbox[box_id][1] = event.x \
                * self.aspect_ratio
        elif self.box_resize_mode == 'TOP':
            self.canvas.coords(self.boxes[self.resize_box_id].rect, 
                   self.boxes[self.resize_box_id].left, 
                   event.y,
                   self.boxes[self.resize_box_id].right,
                   self.boxes[self.resize_box_id].bottom)
            self.boxes[self.resize_box_id].top = event.y
            self.annotations[self.current_file].bbox[box_id][0] = event.y \
                * self.aspect_ratio
        elif self.box_resize_mode == 'BOTTOM':
            self.canvas.coords(self.boxes[self.resize_box_id].rect, 
                   self.boxes[self.resize_box_id].left, 
                   self.boxes[self.resize_box_id].top,
                   self.boxes[self.resize_box_id].right,
                   event.y)
            self.boxes[self.resize_box_id].bottom = event.y
            self.annotations[self.current_file].bbox[box_id][2] = event.y \
                * self.aspect_ratio

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
        if rot > 0:
            self.img = self.img.transpose(rot)
                
    def _reset_image(self):
        
        for lbl in self.annotations[self.current_file].label:
            self.class_count[lbl] = self.class_count[lbl] - 1
        
        self.annotations[self.current_file].label = []
        self.annotations[self.current_file].bbox = []
        self._draw_workspace()
        
if __name__ == "__main__":
    
    tool = AnnotationTool()
    tool.load_app()
    