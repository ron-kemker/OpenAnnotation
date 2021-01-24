# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 21:25:58 2021

@author: Master
"""

import glob, exif, pickle, csv
from PIL import Image
from plum._exceptions import UnpackError


import tkinter as tk
from tkinter import Frame, Label, Menu, Button
from tkinter.filedialog import askopenfilename, asksaveasfilename, \
    askdirectory

class AppMenu(object):
   
    def __init__(self, root_app):
        '''
        This is the menu bar at the top of the application.
        
        Parameters
        ----------
        root_app : Pass a pointer to the root_application to access "global"
                   variables.
        
        Returns
        -------
        None.
    
        '''           
        
        self.root_app = root_app

    def _draw_menu(self):
        # Build File Menu
        menu = Menu(self.root_app.window)
        self.root_app.window.config(menu=menu)
        fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New Project", 
                             command=self._new)
        fileMenu.add_command(label="Open Project", command=self._open)
        
        
        if self.root_app.project_open:
            fileMenu.add_command(label="Save Project", command=self._save)
            fileMenu.add_command(label="Close Project", command=self._close)
        
        fileMenu.add_separator()
        
        if self.root_app.project_open:
            fileMenu.add_command(label="Import File", 
                                 command=self._import_file)
            fileMenu.add_command(label="Import Directory", 
                                 command=self._import_files_in_directory) 
            fileMenu.add_command(label="Export Project to CSV", 
                                  command=self._csv_exporter)
            fileMenu.add_separator()
        
        fileMenu.add_command(label="Quit", command=self._quit)
        
        if self.root_app.project_open:

            toolMenu = Menu(menu)
            menu.add_cascade(label="Tools", menu=toolMenu)
            toolMenu.add_command(label="Class Manager", 
                                 command=self.root_app._draw_object_class_manager)
            
            if len(self.root_app.annotations):
                toolMenu.add_command(label="Reset Image", 
                                     command=self.root_app._reset_image)

    def file_to_annotation(self, file):
        self.root_app.annotations.append(Annotation(file))
        try:   
            meta = exif.Image(file)
            if meta.has_exif:
                if 'orientation' in dir(meta):
                   if meta.orientation == 6:
                       self.root_app.annotations[-1].rotation = Image.ROTATE_270
                   elif meta.orientation == 3:
                       self.root_app.annotations[-1].rotation = Image.ROTATE_180
                   elif meta.orientation == 8:
                       self.root_app.annotations[-1].rotation = Image.ROTATE_90   
        except UnpackError:
            print('%s does not have exif formatted metadata.' % file)

    def _import_file(self):
        
        file = askopenfilename(filetypes=(("Image File",
                                           self.root_app.file_ext),
                                          ),
                                                initialdir = "/",
                                                title = "Select file")

        if not file:
            return
        
        elif file not in self.root_app.file_list:
            self.root_app.file_list.append(file)
            self.file_to_annotation(file)
    
            
            # Build Toolbar Frame
        
            # If this is the first image being loaded, then add it to canvas
            if not hasattr(self, 'img'):
                self.root_app._load_image_from_file()  
            self.root_app._draw_workspace()
            self.root_app.saved = False       
            
        else:
            print('File already in the project.')
    
    def _import_files_in_directory(self):
        new_dir = askdirectory()
        
        if not new_dir:
            return
        
        tmp_file_list = []
        for fe in self.root_app.file_ext:
            tmp_file_list += glob.glob(new_dir + '\*%s' % fe)


        for file in tmp_file_list:
            self.file_to_annotation(file)

        self.root_app.file_list += tmp_file_list
        # If this is the first image being loaded, then add it to canvas
        if not hasattr(self, 'img'):
            self.root_app._load_image_from_file()  
        self.root_app._draw_workspace()
        self.root_app.saved = False    
    
    def _new(self):
        # self.root = askdirectory()
        
        self.root_app.file_list = []
        self.root_app.project_open = True
 
        self.root_app.annotations = [] 
        self.root_app._draw_workspace()
        self.root_app.saved = False

    def _open(self):
        self.root_app.saved = True
        self.root_app.project_open = True

        file_name = askopenfilename(filetypes=(("PKL files","*.pkl"),),
                                                initialdir = "/",
                                                title = "Select file")
        with open(file_name, 'rb') as f:
            mat = pickle.load(f)
        self.root_app.annotations = mat['annotations']
        self.root_app.file_list = mat['file_list']
        self.root_app.class_list = mat['class_list']
        self.root_app.current_file = mat['current_file']
        self.root_app.file_ext = mat['file_ext']
        self.root_app.colorspace = mat['colorspace']
        self.root_app.top_colors_free = mat['top_colors_free']
        self.root_app.top_colors_used = mat['top_colors_used']
        self.root_app.class_count = mat['class_count']

        # Build Toolbar Frame
        self.root_app._load_image_from_file()  
        self.root_app._draw_workspace()
        
    def _save(self):
        
        save_dict = {'annotations': self.root_app.annotations,
                     'file_list': self.root_app.file_list,
                     'class_list': self.root_app.class_list,
                     'current_file':self.root_app.current_file,
                     'file_ext': self.root_app.file_ext,
                     'colorspace': self.root_app.colorspace,
                     'top_colors_free': self.root_app.top_colors_free,
                     'top_colors_used': self.root_app.top_colors_used,
                     'class_count' : self.root_app.class_count,                     
                     }
        
        file_name = asksaveasfilename(filetypes=(("PKL files","*.pkl"),),
                                                initialdir = "/",
                                                title = "Select file")
        if file_name != '':        
            f = open(file_name, "wb")
            pickle.dump(save_dict, f)
            f.close()
            self.root_app.saved = True

    def _close(self):
        self.root_app.project_open = False
        
        if not self.root_app.saved:
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
        self.root_app.background.destroy()
        self.root_app.__init__()
        self._draw_menu()
                   
        self.root_app.background = Frame(self.root_app.window,
                                width=self.root_app.window_width,
                                height=self.root_app.window_height)
        self.root_app.background.pack()
                
        # Create Load Screen Buttons
        new_button = Button(self.root_app.background, text="New Project", 
                            width = 20,
                            height=3, 
                            command=self._new)
        new_button.grid(row=0, column=0, sticky='n', pady=2 )

        load_button = Button(self.root_app.background, text="Load Project", 
                             width=20,
                            height=3, 
                            command=self._open)
        load_button.grid(row=1, column=0, sticky='n', pady=2  )

        quit_button = Button(self.root_app.background, text="Quit", width=20, 
                             height=3, 
                            command=self._quit)
        quit_button.grid(row=2, column=0, sticky='n', pady=2  )

    def _quit(self):
        
        if not self.root_app.saved:
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
                               command=self.root_app.window.destroy)
            no_button.grid(row=1, column=1)           
            cancel_button = Button(bkgd_frame, text="Cancel", 
                                   command=popup_window.destroy)
            cancel_button.grid(row=1, column=2)            
        else:
            self.root_app.window.destroy()


    def _csv_exporter(self):
        '''
        Creates a CSV of the entire project.  Format is:
        
            filename, label, x0, y0, x1, y1, rotation

        Returns
        -------
        None.

        '''

        file_name = asksaveasfilename(filetypes=(("CSV files","*.csv"),),
                                                initialdir = "/",
                                                title = "Select file")
        if file_name == '':  
            return
        else:
            file_name = file_name + '.csv'
        
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')            
            header = ['filename','label','left','top','right','bottom',
                      'rotation']
            writer.writerow(header)
        
        
            for i, image in enumerate(self.root_app.annotations):
                for b, box in enumerate(image.bbox):
                    
                    row = [image.filename,image.label[b], box[1], box[0],
                           box[3],box[2],image.rotation]
                    writer.writerow(row)
        
        
            
class Annotation(object):
    
    def __init__(self, filename):
        self.filename = filename
        self.bbox = []
        self.label = []
        self.rotation = -1
        self.ignore = False
    
    def add_label(self, top, left, bottom, right, label):
        self.bbox.append([top, left, bottom, right, label])
        self.label.append(label)