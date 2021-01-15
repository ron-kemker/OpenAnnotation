# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 09:26:18 2020

@author: Ronald Kemker
"""

import tkinter as tk
from tkinter import Frame, Label, Menu, Button, Entry, \
    OptionMenu, StringVar, Canvas, Event
from tkinter.filedialog import askopenfilename, asksaveasfilename, \
    askdirectory
from PIL import ImageTk, Image, ImageOps
import glob
import exif 
import pickle
import numpy as np

from objectclassmanager import ObjectClassManager
from toolbar import Toolbar

class AnnotationTool(object):
    
    def __init__(self, file_ext = '.jpg'):
        '''
        TODO: Network labeling capability
        TODO: Store relative image position (vs absolute)
        TODO: Include class object count
        TODO: Resize box capability
        TODO: ROI Tool
        TODO: Selectable box deletion
        Parameters
        ----------
        file_ext : TYPE, optional
            DESCRIPTION. The default is '.jpg'.

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

        self.colorspace = {}
        self.top_colors = ['Blue', 'Red', 'Green', 'Cyan', 'Magenta', 
                           'Yellow'] # TODO: Support Additional Colors

    def load_app(self):
        
        # Build Window
        self.window = tk.Tk()
        self.window.title("Image Annotation Tool")  # to define the title
        self.window.geometry("%dx%d" % (self.window_width,self.window_height))
        self._draw_menu()
                   
        self.background = Frame(self.window,
                                width=self.window_width,
                                height=self.window_height)
        self.background.pack()
                
        # Create Load Screen Buttons
        new_button = Button(self.background, text="New Project", width = 20,
                            height=3, 
                            command=self._new)
        new_button.grid(row=0, column=0, sticky='n', pady=2 )

        load_button = Button(self.background, text="Load Project", width=20,
                            height=3, 
                            command=self._open)
        load_button.grid(row=1, column=0, sticky='n', pady=2  )

        quit_button = Button(self.background, text="Quit", width=20, 
                             height=3, 
                            command=self._quit)
        quit_button.grid(row=2, column=0, sticky='n', pady=2  )
        
        self.window.mainloop()

    def _new(self):
        self.root = askdirectory()
        self.file_list = glob.glob(self.root + '\*%s' % self.file_ext)
        self.project_open = True
 
        self.annotations = []
        for ii, file in enumerate(self.file_list):
            self.annotations.append(Annotation(file))
            meta = exif.Image(file)
            if meta.has_exif:
               if 'orientation' in dir(meta):
                   if meta.orientation == 6:
                       self.annotations[-1].rotation = Image.ROTATE_270
                   elif meta.orientation == 3:
                       self.annotations[-1].rotation = Image.ROTATE_180
                   elif meta.orientation == 8:
                       self.annotations[-1].rotation = Image.ROTATE_90

        
        # Build Toolbar Frame
        self._load_image_from_file()  
        self._draw_workspace()
        self.saved = False

    def _open(self):
        self.saved = True
        self.project_open = True

        file_name = askopenfilename(filetypes=(("PKL files","*.pkl"),),
                                                initialdir = "/",
                                                title = "Select file")
        with open(file_name, 'rb') as f:
            mat = pickle.load(f)
        self.annotations = mat['annotations']
        self.file_list = mat['file_list']
        self.class_list = mat['class_list']
        self.current_file = mat['current_file']
        self.file_ext = mat['file_ext']
        self.colorspace = mat['colorspace']

        # Build Toolbar Frame
        self._load_image_from_file()  
        self._draw_workspace()
        
    def _save(self):
        
        save_dict = {'annotations': self.annotations,
                     'file_list': self.file_list,
                     'class_list': self.class_list,
                     'current_file':self.current_file,
                     'file_ext': self.file_ext,
                     'colorspace': self.colorspace,
                     }
        
        file_name = asksaveasfilename(filetypes=(("PKL files","*.pkl"),),
                                                initialdir = "/",
                                                title = "Select file")
        if file_name != '':        
            f = open(file_name, "wb")
            pickle.dump(save_dict, f)
            f.close()
            self.saved = True

    def _close(self):
        self.project_open = False
        
        if not self.saved:
            self.popup_window = tk.Toplevel()
            self.popup_window.geometry("300x100") 
            self.popup_window.wm_title("Save Work?")
            
            bkgd_frame = Frame(self.popup_window, width=300, height=100)
            bkgd_frame.pack()
            
            prompt_txt = "Close without saving?"
            prompt = Label(bkgd_frame, text=prompt_txt)
            prompt.grid(row=0, column=0, columnspan=3, sticky='nsew')
            
            yes_button = Button(bkgd_frame, text="Save", 
                                command=self._save_close_command)
            yes_button.grid(row=1, column=0)
            no_button = Button(bkgd_frame, text="Close", 
                               command=self._close_command)
            no_button.grid(row=1, column=1)           
            cancel_button = Button(bkgd_frame, text="Cancel", 
                                   command=self.popup_window.destroy)
            cancel_button.grid(row=1, column=2)            
        else:
            self._close_command()

    def _save_close_command(self):
        self._save()
        self._close_command()
        
    def _close_command(self):        
        
        if hasattr(self, 'popup_window'):
            self.popup_window.destroy()
        self.background.destroy()
        self.__init__()
        self._draw_menu()
                   
        self.background = Frame(self.window,
                                width=self.window_width,
                                height=self.window_height)
        self.background.pack()
                
        # Create Load Screen Buttons
        new_button = Button(self.background, text="New Project", width = 20,
                            height=3, 
                            command=self._new)
        new_button.grid(row=0, column=0, sticky='n', pady=2 )

        load_button = Button(self.background, text="Load Project", width=20,
                            height=3, 
                            command=self._open)
        load_button.grid(row=1, column=0, sticky='n', pady=2  )

        quit_button = Button(self.background, text="Quit", width=20, 
                             height=3, 
                            command=self._quit)
        quit_button.grid(row=2, column=0, sticky='n', pady=2  )


    def _quit(self):
        
        if not self.saved:
            popup_window = tk.Toplevel()
            popup_window.geometry("300x100") 
            popup_window.wm_title("Save Work?")
            
            bkgd_frame = Frame(popup_window, width=300, height=100)
            bkgd_frame.pack()
            
            prompt_txt = "Quit without saving?"
            prompt = Label(bkgd_frame, text=prompt_txt)
            prompt.grid(row=0, column=0, columnspan=3, sticky='nsew')
            
            yes_button = Button(bkgd_frame, text="Save", command=self._save)
            yes_button.grid(row=1, column=0)
            no_button = Button(bkgd_frame, text="Quit", 
                               command=self.window.destroy)
            no_button.grid(row=1, column=1)           
            cancel_button = Button(bkgd_frame, text="Cancel", 
                                   command=popup_window.destroy)
            cancel_button.grid(row=1, column=2)            
        else:
            self.window.destroy()
        

    def _draw_menu(self):
        # Build File Menu
        menu = Menu(self.window)
        self.window.config(menu=menu)
        fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New Project", 
                             command=self._new)
        fileMenu.add_command(label="Open Project", command=self._open)
        
        
        if self.project_open:
            fileMenu.add_command(label="Save Project", command=self._save)
            fileMenu.add_command(label="Close Project", command=self._close)
        
        fileMenu.add_separator()
        
        if self.project_open:
            fileMenu.add_command(label="Import File", command=None)
            fileMenu.add_command(label="Import Directory", command=None)        
            fileMenu.add_separator()
        
        fileMenu.add_command(label="Quit", command=self._quit)
        
        
        if self.project_open:

            toolMenu = Menu(menu)
            menu.add_cascade(label="Tools", menu=toolMenu)
            toolMenu.add_command(label="Class Manager", 
                                 command=self._draw_object_class_manager)
        
            toolMenu.add_command(label="Export Project to CSV", 
                                  command=self._csv_exporter)

    def _draw_object_class_manager(self):
        
        obj_mgr = ObjectClassManager(self)
        
    def _draw_workspace(self):
        
        self._draw_menu()
        
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
        
        for i, label in enumerate(self.annotations[self.current_file].bbox):
            self.canvas.create_rectangle(label[1], 
                                  label[0],
                                  label[3],
                                  label[2],
                                  outline=self.colorspace[label[-1]],
                                  width=5)
        
        # Only allow bounding boxes to be drawn if they can be tied to a class
        if len(self.class_list):        
            self.canvas.bind("<Button-1>",self._on_click)
            self.canvas.bind("<B1-Motion>", self._on_move_press)
            self.canvas.bind("<ButtonRelease-1>",self._on_release)

    def _csv_exporter(self):
        return
        

    def _on_click(self, event):
        self.box_start = (event.x, event.y)
        color = self.colorspace[self.selected_class.get()]
        self.rect = self.canvas.create_rectangle(self.box_start[0], 
                                                 self.box_start[1], 
                                                 self.box_start[0]+1, 
                                                 self.box_start[0]+1, 
                                                 width=5,
                                                 outline=color)

    def _on_release(self, event):
        
        top = min(self.box_start[1], self.box_end[1])
        bottom = max(self.box_start[1], self.box_end[1])
        left = min(self.box_start[0], self.box_end[0])
        right = max(self.box_start[0], self.box_end[0])
        label = self.selected_class.get()
        self.annotations[self.current_file].add_label(top, 
                                                      left, 
                                                      bottom, 
                                                      right, 
                                                      label)
        self.saved = False
        
    def _on_move_press(self, event):
        self.box_end = (event.x, event.y)
        self.canvas.coords(self.rect, 
                           self.box_start[0], 
                           self.box_start[1],
                           self.box_end[0],
                           self.box_end[1])


    def _load_image_from_file(self):
        self.img = Image.open(self.file_list[self.current_file])
        
        self.file_list[self.current_file]
        
        rot = self.annotations[self.current_file].rotation
        self.img = self.img.transpose(rot)
        
        
class Annotation(object):
    
    def __init__(self, filename):
        self.filename = filename
        self.bbox = []
        self.label = []
        self.rotation = 0
        self.ignore = False
    
    def add_label(self, top, left, bottom, right, label):
        self.bbox.append([top, left, bottom, right, label])
        self.label.append(label)

    
if __name__ == "__main__":
    
    tool = AnnotationTool()
    tool.load_app()