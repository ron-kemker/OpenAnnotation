# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 20:49:18 2021

@author: Ronald Kemker
"""


from tkinter import Canvas, ttk
from PIL import ImageTk, Image
import multiprocessing as mp

def helper_open_image(filename, navigator_width, rotation):
    '''
    Helper function for parallelization in Navigator __init__
      
    Parameters
    ----------
    filename : string
        Path to image file
    navigator_width : int
        The number of pixels that the navigator window is (for scaling)
    rotation : int
        The rotation of the raw image
    
    Raises
    ------
    None        
    
    Returns
    -------
    img : PIL Image file
        Scaled to fit within the navigator canvas
        
    '''   
    img = Image.open(filename)

    if rotation > 0:
        img = img.transpose(rotation)

    scale = img.size[0] / navigator_width
                        
    new_size = (int(img.size[0] / scale), 
                int(img.size[1] / scale))

    return img.resize(new_size,Image.NEAREST)    

class Navigator(object):
        
    def __init__(self, root_app):
        '''
        Navigator Class
          
        Parameters
        ----------
        root_app : AnnotationTool object
            Pass Parent Object to access global variables
        
        Attributes
        ----------
        root_app : AnnotationTool object
            Parent Object        
        
        Raises
        ------
        None        
        
        Returns
        -------
        None
            
        '''           
        self.root_app = root_app

        container = ttk.Frame(root_app.background,
                              width = root_app.navigator_width,
                              height = root_app.canvas_height)
        canvas = Canvas(container,
                        width = root_app.navigator_width,
                        height = root_app.canvas_height)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, 
                                  orient="vertical", 
                                  command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas,
                                     width = root_app.navigator_width,
                                     height = root_app.canvas_height)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        start = root_app.page * root_app.img_per_page
        end = min(start + root_app.img_per_page, len(root_app.file_list))

        # This is slow, so I am using the multiprocessing library to paralleize
        # the code.
        args = []
        if self.root_app.window.winfo_ismapped():

            for i in range(start,end):
                args.append((root_app.file_list[i], 
                             root_app.navigator_width,
                             root_app.annotations[i].rotation))
            
            with mp.Pool(mp.cpu_count()) as pool:
                results = pool.starmap(helper_open_image, args)

        for i, ii in enumerate(range(start, end)):
            
            if self.root_app.window.winfo_ismapped():
                pil_img = ImageTk.PhotoImage(results[i])
            else:
                pil_img = None
            
            button = ttk.Button(scrollable_frame, 
                       image = pil_img,
                       command = lambda ii=ii: self.change_image(ii))
            button.image = pil_img
            button.pack(fill='x')
            

        container.place(x=root_app.canvas_width-21, y=root_app.toolbar_height)
        scrollbar.pack(side="right", fill="y")

  
    def change_image(self , i):
        '''
        Change the image in the main canvas
          
        Parameters
        ----------
        i : int
            The index of the image to open
        
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
        self.root_app.current_file = i
        self.root_app._load_image_from_file()  
        self.root_app.draw_canvas()