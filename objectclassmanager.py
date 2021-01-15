# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 07:57:48 2021

@author: Master
"""


import tkinter as tk
from tkinter import Frame, Label, Menu, Button, Entry, \
    OptionMenu, StringVar, colorchooser

class ObjectClassManager(object):
    
    def __init__(self, root_app):
        
        self.root_app = root_app
        self.class_manager_window = tk.Toplevel()
        self.class_manager_window.wm_title("Object Class Manager")
        self.class_manager_window.geometry("%dx%d" % (400,400))

        self._add_object_class()

    def _choose_color(self, button_id):
        color_code = colorchooser.askcolor(title="Choose Color")
        class_id = self.root_app.class_list[button_id]
        self.root_app.colorspace[class_id] = color_code[1]
        self.class_manager_frame.destroy()
        self._add_object_class()   
        self.root_app.saved = False
        self.root_app._draw_workspace()
        
    def _add_object_class(self):
        self.class_manager_frame = Frame(self.class_manager_window,
                                         height=200,
                                         width=400)
        self.class_manager_frame.pack()
        
        top_label = Label(self.class_manager_frame, 
                          text="",)
        top_label.grid(row=0, column=0, columnspan=3)
                
        for i, c in enumerate(self.root_app.class_list):
            
            class_label = Label(self.class_manager_frame, 
                                text="%d. %s" % ((i+1), c))
            class_label.grid(row=i+1, column=0, sticky='w', pady=1)
            
            color_button = Button(self.class_manager_frame, 
                                  width=1, 
                                  height=1,
                                  bg=self.root_app.colorspace[c],
                                  command=lambda i=i: self._choose_color(i))
            

            color_button.grid(row=i+1, column=1, pady=1)
            
            remove_button = Button(self.class_manager_frame, 
                                   text="X", 
                                   command=lambda i=i: self._remove_class(i))
            remove_button.grid(row=i+1, column=2, pady=1)
        
        self.new_class_var = None
        
        self.new_class_entry = Entry(self.class_manager_frame,
                      textvariable=self.new_class_var)
        self.new_class_entry.grid(row=len(self.root_app.class_list)+1, 
                                  column=0)
        add_button = Button(self.class_manager_frame, 
                               text="+", 
                               command=self._add_class)
        add_button.grid(row=len(self.root_app.class_list)+1, column=2)
                    
        close_button = Button(self.class_manager_frame, 
                              text="Close",
                              command=self._close_class_manager)
        close_button.grid(row=len(self.root_app.class_list)+2, 
                          column=0, 
                          columnspan=3)
    
    def _add_class(self):
                
        new_class = self.new_class_entry.get()
        
        if new_class == "":
            print("Provide new class name.")
        elif new_class in self.root_app.class_list:
            print("Class already exists.")
        else:
            self.root_app.colorspace[new_class] = self.root_app.top_colors.pop(0)
            self.root_app.class_list.append(new_class)
        self.class_manager_frame.destroy()
        self._add_object_class()
            
    def _remove_class(self, button_id):
        color = self.root_app.colorspace[self.root_app.class_list[button_id]]
        # del self.root_app.colorspace[self.root_app.class_list[button_id]]
        self.root_app.top_colors.insert(0, color)
        class_label = self.root_app.class_list.pop(button_id)
        del self.root_app.colorspace[class_label]

        
        #TODO: Prompt if you really want to delete the class        
        for annotation in self.root_app.annotations:
            indices = [i for i, x in enumerate(annotation.label) if x == class_label]
            for ind in sorted(indices, reverse = True):  
                del annotation.label[ind] 
                del annotation.bbox[ind]

        self.class_manager_frame.destroy()
        self._add_object_class()                 

        
    def _close_class_manager(self):
        self.class_manager_window.destroy()
        self.root_app._draw_workspace()
        
if __name__ == "__main__":

    import types    

    root_app = types.SimpleNamespace()
    root_app.class_list = ['Winston', 'Prince']
    root_app.top_colors = ['Green', 'Cyan', 'Magenta', 'Yellow']
    root_app.colorspace = {'Winston': 'Blue', 'Prince': 'Red'}
    root_app._draw_workspace = lambda: print('Redraw Workspace')
    obj_mgr = ObjectClassManager(root_app)
    obj_mgr.class_manager_window.mainloop()
