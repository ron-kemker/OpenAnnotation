# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 07:57:48 2021

@author: Ronald Kemker
"""

import random
import tkinter as tk
from tkinter import Frame, Label, Menu, Button, Entry, \
    OptionMenu, StringVar, colorchooser

class ObjectClassManager(object):
    
    def __init__(self, root_app):
        '''
        This brings up a popup window that helps add/remove/rename object 
        classes.
        
        Parameters
        ----------
        root_app : Pass a pointer to the root_application to access "global"
                   variables.
        
        Returns
        -------
        None.
    
        '''           
        self.root_app = root_app
        self.class_manager_window = tk.Toplevel()
        self.class_manager_window.wm_title("Object Class Manager")
        self.class_manager_window.geometry("%dx%d" % (400,400))
        self._add_object_class()


    def _choose_color(self, button_id):
        
        color_code = colorchooser.askcolor(title="Choose Color")
        # class_id = self.root_app.class_list[button_id]
        
        if self.root_app.colorspace[button_id] in self.root_app.top_colors:
            self.root_app.top_colors_free.insert(0, self.root_app.colorspace[button_id])
            self.root_app.top_colors_used.remove(self.root_app.colorspace[button_id])
        self.root_app.colorspace[button_id] = color_code[1]
        self.class_manager_frame.destroy()
        self._add_object_class()   
        self.root_app.saved = False
        self.root_app._draw_workspace()
        
    def _add_object_class(self):
        self.class_manager_frame = Frame(self.class_manager_window,
                                         height=400,
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
                                  bg=self.root_app.colorspace[i],
                                  command=lambda i=i: self._choose_color(i))
            

            color_button.grid(row=i+1, column=1, pady=1)

            rename_button = Button(self.class_manager_frame, 
                                   text="Rename", 
                                   command=lambda i=i: self._rename_class(i))
            rename_button.grid(row=i+1, column=2, pady=1)
            
            remove_button = Button(self.class_manager_frame, 
                                   text="Delete", 
                                   command=lambda i=i: self._check_before_remove(i))
            remove_button.grid(row=i+1, column=3, pady=1)
            
            
            instances = self.root_app.class_count[i]
            instance_label = Label(self.class_manager_frame, 
                                   text=' %d labeled instances.' % instances)
            instance_label.grid(row=i+1, column=4)
        
        self.new_class_var = None
        
        self.new_class_entry = Entry(self.class_manager_frame,
                      textvariable=self.new_class_var)
        self.new_class_entry.grid(row=len(self.root_app.class_list)+1, 
                                  column=0)
        add_button = Button(self.class_manager_frame, 
                               text="Add Class", 
                               command=self._add_class)
        add_button.grid(row=len(self.root_app.class_list)+1, column=2)
                    
        close_button = Button(self.class_manager_frame, 
                              text="Close",
                              command=self._close_class_manager)
        close_button.grid(row=len(self.root_app.class_list)+2, 
                          column=0, 
                          columnspan=4)

    def _rename_class_action(self, button_id):
        
        old_class = self.root_app.class_list[button_id]
        new_class = self.rename_entry.get()
        
        if new_class == '':
            print('Field was empty.  Please provide a new class name.')
        else:
            self.root_app.class_list[button_id] = new_class            
            self.rename_class_prompt.destroy()
            self.class_manager_frame.destroy()
            self._add_object_class()
            
            for a, ann in enumerate(self.root_app.annotations):
                for b, lbl in enumerate(ann.label):
                    if lbl == old_class:
                        self.root_app.annotations[a].bbox[b][-1] = new_class
                        self.root_app.annotations[a].label[b] = new_class
                        
        
    def _rename_class(self, button_id):
        
        self.rename_class_prompt = tk.Toplevel()
        self.rename_class_prompt.wm_title("Rename Class")
        self.rename_class_prompt.geometry("%dx%d" % (400,200))
        current_class = self.root_app.class_list[button_id]

        self.rename_class_frame = Frame(self.rename_class_prompt,
                                         height=400,
                                         width=400)
        self.rename_class_frame.pack()
        label = Label(self.rename_class_frame, 
                      text='Rename \"%s\" Class to:' % current_class)
        label.grid(row=0, column=0, columnspan=2)
        
        self.new_class_name_var = None
        self.rename_entry = Entry(self.rename_class_frame, 
                      textvariable=self.new_class_name_var)
        self.rename_entry.grid(row=1, column=0, columnspan=2)
        
        i = button_id
        rename_button = Button(self.rename_class_frame, 
                            text="Ok", 
                            command=lambda i=i: self._rename_class_action(i))
        rename_button.grid(row=2, column=0)
                    
        close_button = Button(self.rename_class_frame, 
                              text="Cancel",
                              command=self.rename_class_prompt.destroy)
        close_button.grid(row=2, column=1)        
    
    
    def _add_class(self):
                
        new_class = self.new_class_entry.get()
        
        if new_class == "":
            print("Provide new class name.")
        elif new_class in self.root_app.class_list:
            print("Class already exists.")
        else:
            
            if len(self.root_app.top_colors_free) > 0:
                col = self.root_app.top_colors_free.pop(0)
                self.root_app.top_colors_used.append(col)

            else:
                col = "#%06x" % random.randint(0, 0xFFFFFF)
                
            self.root_app.colorspace.append(col)
            self.root_app.class_list.append(new_class)
            self.root_app.class_count.append(0)
        self.class_manager_frame.destroy()
        self._add_object_class()
    
    def _check_before_remove(self, button_id):
        self.popup_window = tk.Toplevel()
        self.popup_window.geometry("300x100") 
        self.popup_window.wm_title("Remove Class?")
        
        bkgd_frame = Frame(self.popup_window)
        bkgd_frame.place(x=0, y=0, width=300, height=100)
        
        prompt_txt = "Delete Class?  You cannot undo this action."
        prompt = Label(bkgd_frame, text=prompt_txt)
        prompt.place(x=10, y=0, width=280, height=30)
        
        i=button_id
        yes_button = Button(bkgd_frame, 
                            text="Remove", 
                            command=lambda i=i: self._remove_class(i))
        yes_button.place(x=90, y=30, height=30, width=50)
        
        cancel_button = Button(bkgd_frame, text="Cancel", 
                               command=self.popup_window.destroy)
        cancel_button.place(x=160, y=30, height=30, width=50)

        
    def _remove_class(self, button_id):
        color = self.root_app.colorspace[button_id]
        
        if color in self.root_app.top_colors:
            self.root_app.top_colors_free.insert(0, color)
            self.root_app.top_colors_used.remove(color)            
        
        # class_label = self.root_app.class_list.pop(button_id)
        self.root_app.colorspace.pop(button_id)
        self.root_app.class_count.pop(button_id)
        self.root_app.class_list.pop(button_id)

        for i, annotation in enumerate(self.root_app.annotations):
            deleted = 0
            num_roi = annotation.size()
            for ii in range(num_roi):
                class_id = self.root_app.annotations[i].label[ii-deleted]
                if class_id == button_id:
                    self.root_app.annotations[i].pop(ii-deleted)
                    deleted += 1
                elif class_id > button_id:
                    self.root_app.annotations[i].label[ii-deleted] =\
                        self.root_app.annotations[i].label[ii-deleted] - 1
        
        self.class_manager_frame.destroy()
        self._add_object_class() 

        if hasattr(self, 'popup_window'):
            self.popup_window.destroy()                

    def _close_class_manager(self):
        self.class_manager_window.destroy()
        self.root_app._draw_workspace()