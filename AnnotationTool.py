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
from fileio import ROI

class AnnotationTool(object):
    
    def __init__(self):
        '''
        This is the main annotation tool object.  Running this .py file will
        open the application.
        
        Parameters
        ----------
        None
    
        Attributes
        ----------
        file_ext : list (Default = ['.jpg', '.png']) 
            Image file extensions currently supported by OpenAnnotation
        window_size_strings : list (Default = ["1024x768", "800x600"])
            These are the supported Window Sizes.
        window_size_index : int
            Which window size in window_size_strings is currently selected
        window_width : int
            The number of pixels the window width is
        window_height : int
            The number of pixels the window height is
        toolbar_width : int
            The number of pixels the Toolbar width is
        footer_height : int
            The number of pixels the footer height is
        canvas_width : int
            The remaining window size is for the Canvas object
        canvas_height : int
            The remaining window size is for the Canvas object
        project_open : bool
            This tracks if the project is open for display purposes
        saved : bool
            This tracks if the current project is saved
        app_menu : The OpenAnnotation AppMenu object
            Initialize the menu across the top of the window
        top_colors : list
            The default colors are blue, red, green, cyan, yellow, and magenta
                
        Raises
        ------
        None
    
        Returns
        -------
        None

        '''
        self.file_ext = ['.jpg', '.png']
        self.window_size_strings = ["1024x768", "800x600"]
        self.window_size_index = 0
        self.window_width = 1024
        self.window_height = 768
        self.toolbar_width = 150
        self.footer_height = 25
        self.canvas_width = self.window_width - self.toolbar_width
        self.canvas_height = self.window_height - self.footer_height
        self.project_open = False
        self.saved = True
        self.app_menu = AppMenu(self)
        self.top_colors = ['#0000FF', '#FF0000', '#00FF00', '#00FFFF', 
                           '#FF00FF', '#FFFF00'] 

    def load_app(self, test=False):
        '''
        This loads the main window for the OpenAnnotation applications
        
        Parameters
        ----------
        test : bool (Default = False)
            If test=True, then the window is not actually drawn
    
        Attributes
        ----------
        window : tkinter Tk object
            This is the main application window
        background : tkinter Frame object
            This is the frame that covers the entire window object
                
        Raises
        ------
        None
    
        Returns
        -------
        complete : bool
            Returns True for unittesting

        '''        
        # Build Window
        self.window = tk.Tk()
            
        self.window.title("OpenAnnotation 0.1")  # to define the title
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

        new_wiz_button = Button(self.background, 
                                     text="New Project Wizard", 
                                     width = 20,
                                     height=3, 
                                     command=self.app_menu._new_project_wizard)
        new_wiz_button.grid(row=1, column=0, sticky='n', pady=2 )

        load_button = Button(self.background, text="Load Project", 
                            width=20,
                            height=3, 
                            command=self.app_menu._open)
        load_button.grid(row=2, column=0, sticky='n', pady=2)

        quit_button = Button(self.background, text="Quit", 
                            width=20, 
                            height=3, 
                            command=self.app_menu._quit)
        quit_button.grid(row=3, column=0, sticky='n', pady=2)
        
        if not test:
            self.window.mainloop()

        return True
        
    def _draw_object_class_manager(self):
        '''
        This draws the Object Class Management Tool in a popup window
        
        Parameters
        ----------
        None
    
        Attributes
        ----------
        obj_mgr : OpenAnnotation ObjectClassManager object
            This is the Object Class Management tool accessible from the
            toolbar up top
                
        Raises
        ------
        None
    
        Returns
        -------
        complete : bool
            Returns True for unittesting

        '''          
        self.obj_mgr = ObjectClassManager(self)
        return True
        
    def _draw_workspace(self):
        '''
        This draws the main project in the background frame
        
        Parameters
        ----------
        None
    
        Attributes
        ----------
        background : tkinter Frame object
            This is the frame that covers the entire window object
        canvas : tkinter Canvas object
            This is what the image is drawn on
        aspect_ratio : float
            Compute the scale factor to shrink/increase the image to fit in
            the canvas
        boxes : list
            A list for the OpenAnnotation InteractiveBox objects
            
        Raises
        ------
        None
    
        Returns
        -------
        complete : bool
            Returns True for unittesting
    
        '''         
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
        canvas_frame = Frame(self.background, bg='green',
                    width=self.canvas_width,
                    height=self.canvas_height)
        canvas_frame.place(x=self.toolbar_width,
                                y=0, 
                                width = self.canvas_width,
                                height = self.canvas_height,
                                )
        
        self.canvas = Canvas(canvas_frame,
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
                              text='OpenAnnotation built by Ron Kemker',
                              fg='white',
                              bg='black')
        footer_label.place(x=0, y=0)
                
        if len(self.annotations):
            self.aspect_ratio = max(self.img.size[0]/(self.canvas_width),
                                    self.img.size[1]/(self.canvas_height)) 
                                
            new_size = (int(self.img.size[0]/self.aspect_ratio), 
                        int(self.img.size[1]/self.aspect_ratio))
            
            if self.window.winfo_ismapped():

                pil_img = ImageTk.PhotoImage(self.img.resize(new_size, 
                                                      Image.ANTIALIAS))
            else:
                pil_img = None
                
            self.canvas.image = pil_img
            self.canvas.create_image(0, 0, anchor=tk.NW, image=pil_img)
            
            self.boxes = []
            
            for i, roi in enumerate(self.annotations[self.current_file].roi):
                
                left, top, right, bottom = roi.getBox()
                lbl = self.annotations[self.current_file].label[i]
                
                left = left / self.aspect_ratio
                top = top / self.aspect_ratio
                right = right / self.aspect_ratio
                bottom = bottom / self.aspect_ratio
                color = self.colorspace[lbl]
                
                box = InteractiveBox(self, left, top, right, bottom, color)
                box.draw_box(self, i)
                self.boxes.append(box)
            
        # Only allow bounding boxes to be drawn if they can be tied to a class
        if len(self.class_list) and len(self.annotations):        
            self.canvas.bind("<Button-1>",self._on_click)
            self.canvas.bind("<ButtonRelease-1>",self._on_release)
            self.canvas.bind("<B1-Motion>", self._on_move_press)

        return True

    def _on_click(self, event):
        '''
        This handles the click-hold Event
        
        Parameters
        ----------
        event : tkinter Event
            Event that handles the mouse being clicked, creating the first of
            two bounding box corners
    
        Attributes
        ----------
        clicked : tuple
            The (x,y) coordinate for the mouse click event
        box_resize_mode : string
            Defines the type of box action that will occur.  Options are
            'RIGHT', 'LEFT', 'TOP', 'BOTTOM', or 'NEW'.
        resize_box_id : int
            This is which ROI object has been clicked on
            
        Raises
        ------
        None
    
        Returns
        -------
        complete : bool
            Returns True for unittesting
    
        '''    
        
        self.clicked = (event.x, event.y)
        
        for i, box in enumerate(self.boxes):
            if box.right_clicked(self.clicked[0], self.clicked[1]):
                self.box_resize_mode = 'RIGHT'
                self.resize_box_id = i
                return True
            elif box.left_clicked(self.clicked[0], self.clicked[1]):
                self.box_resize_mode = 'LEFT'
                self.resize_box_id = i
                return True
            elif box.top_clicked(self.clicked[0], self.clicked[1]):
                self.box_resize_mode = 'TOP'
                self.resize_box_id = i
                return True
            elif box.bottom_clicked(self.clicked[0], self.clicked[1]):
                self.box_resize_mode = 'BOTTOM'
                self.resize_box_id = i
                return True
        
        self.box_resize_mode = 'NEW'
        return True
    
    def _on_release(self, event):
        '''
        This handles when the mouse left-button has been released, which adds
        a new bounding box or resizes an existing box.
        
        Parameters
        ----------
        event : tkinter Event
            Event that handles the mouse being clicked, creating the first of
            two bounding box corners
    
        Attributes
        ----------
        None
            
        Raises
        ------
        None
    
        Returns
        -------
        complete : bool
            Returns True for unittesting
    
        '''            
        if self.box_resize_mode == 'NEW':

            top = min(self.clicked[1], event.y)
            bottom = max(self.clicked[1], event.y)
            left = min(self.clicked[0], event.x)
            right = max(self.clicked[0], event.x)
            label = self.class_list.index(self.selected_class.get())
            color = self.colorspace[label]
            
            box = InteractiveBox(self, left, top, right, bottom, color)
            
            self.canvas.delete(self.rect)
            del self.rect
            box.draw_box(self, len(self.annotations[self.current_file].roi))
            
            top = self.aspect_ratio * top
            bottom = self.aspect_ratio * bottom
            left = self.aspect_ratio * left
            right = self.aspect_ratio * right
            
            roi = ROI()
            roi.push(left, top)
            roi.push(right, bottom)
            self.annotations[self.current_file].push(roi,label)
            
            self.class_count[label] = self.class_count[label] + 1
        self._draw_workspace()
        self.saved = False
        self.box_resize_mode = 'NEW'
        return True
        
    def _on_move_press(self, event):
        '''
        This handles the event where the mouse left-button is held down and 
        the cursor is moved across the screen.
        
        Parameters
        ----------
        event : tkinter Event
            Event that handles the mouse being clicked, creating the first of
            two bounding box corners
    
        Attributes
        ----------
        rect : tkinter Canvas create_rectangle object
            The bounding box that will be drawn on the Canvas
        box_end : tuple
            The (x,y) coordinate for the mouse motion event
            
        Raises
        ------
        None
    
        Returns
        -------
        complete : bool
            Returns True for unittesting
    
        '''            
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
            self.annotations[self.current_file].roi[box_id].points[1][0] =\
                event.x * self.aspect_ratio
        elif self.box_resize_mode == 'LEFT':
            self.canvas.coords(self.boxes[self.resize_box_id].rect, 
                   event.x, 
                   self.boxes[self.resize_box_id].top,
                   self.boxes[self.resize_box_id].right,
                   self.boxes[self.resize_box_id].bottom)
            self.boxes[self.resize_box_id].left = event.x
            self.annotations[self.current_file].roi[box_id].points[0][0] =\
                event.x * self.aspect_ratio
        elif self.box_resize_mode == 'TOP':
            self.canvas.coords(self.boxes[self.resize_box_id].rect, 
                   self.boxes[self.resize_box_id].left, 
                   event.y,
                   self.boxes[self.resize_box_id].right,
                   self.boxes[self.resize_box_id].bottom)
            self.boxes[self.resize_box_id].top = event.y
            self.annotations[self.current_file].roi[box_id].points[0][1] =\
                event.y * self.aspect_ratio
        elif self.box_resize_mode == 'BOTTOM':
            self.canvas.coords(self.boxes[self.resize_box_id].rect, 
                   self.boxes[self.resize_box_id].left, 
                   self.boxes[self.resize_box_id].top,
                   self.boxes[self.resize_box_id].right,
                   event.y)
            self.boxes[self.resize_box_id].bottom = event.y
            self.annotations[self.current_file].roi[box_id].points[1][1] =\
                event.y * self.aspect_ratio

        elif not hasattr(self, 'rect'):
    
            label = self.selected_class.get()
            color = self.colorspace[self.class_list.index(label)]
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

        return True

        
    def _load_image_from_file(self):
        '''
        This uses PIL to load the current Image displayed in the project
        
        Parameters
        ----------
        None
    
        Attributes
        ----------
        img : PIL Image object
            The Image is opened and rotated upright using EXIF metadata
            
        Raises
        ------
        None
    
        Returns
        -------
        complete : bool
            Returns True for unittesting
    
        '''   
        self.img = Image.open(self.file_list[self.current_file])
        
        rot = self.annotations[self.current_file].rotation
        if rot > 0:
            self.img = self.img.transpose(rot)
                
    def _reset_image(self):
        '''
        This deletes all annotations made on a given image
        
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
        complete : bool
            Returns True for unittesting
    
        '''           
        for lbl in self.annotations[self.current_file].label:
            self.class_count[lbl] = self.class_count[lbl] - 1
        
        self.annotations[self.current_file].label = []
        self.annotations[self.current_file].roi = []
        self._draw_workspace()
        return True
        
if __name__ == "__main__":
    
    tool = AnnotationTool()
    tool.load_app()
    