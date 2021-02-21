# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 07:57:48 2021

@author: Ronald Kemker
"""

import random
import tkinter as tk
from tkinter import Frame, Label, Button, Entry, colorchooser, StringVar

class ObjectClassManager(object):
    
    def __init__(self, root_app):
        '''
        This brings up a popup window that helps add/remove/rename object 
        classes.
        
        Parameters
        ----------
        root_app : AnnotationTool object
            Pass a pointer to the root_application to access "global"
            variables.
        
        Attributes
        ----------
        root_app : AnnotationTool object
            A pointer to the root_application to access "global"
            variables.
        class_manager_window : a tkinter TopLevel object
            This is the popup window for the object class manager
            
        Raises
        ------
        None
    
        Returns
        -------
        None
    
        '''

        self.root_app = root_app
        self.class_manager_window = tk.Toplevel()
        self.class_manager_window.wm_title("Object Class Manager")
        self.class_manager_window.grab_set()
        self.class_manager_window.geometry("%dx%d" % (400,400))
        self.draw_frame()


    def _choose_color(self, button_id):
        '''
        Prompts what color to assign to a given object class.
          
        Parameters
        ----------
        button_id : int 
            An integer index pointing to the color changer for a given object
            class.
    
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

        # Prompt for a new color selection
        if self.root_app.window.winfo_ismapped():
            color_code = colorchooser.askcolor(title="Choose Color")[1]
        else:
            color_code = '#EEEEEE' # This is only used for testing
        
        # If this is one of the top default colors, make it available again
        if self.root_app.colorspace[button_id] in self.root_app.top_colors:
            self.root_app.top_colors_free.insert(0, self.root_app.colorspace[button_id])
            self.root_app.top_colors_used.remove(self.root_app.colorspace[button_id])
        
        # Change the color of the corresponding object class
        self.root_app.colorspace[button_id] = color_code
        
        # Redraw the class manager
        self.class_manager_frame.destroy()
        self.draw_frame()   
        
        # Change was made, need to save project
        self.root_app.saved = False
        
        # Redraw the workspace
        self.root_app._draw_workspace()
        
    def draw_frame(self):
        '''
        Populates the object class manager frame
          
        Parameters
        ----------
        None
    
        Attributes
        ----------
        class_manager_frame : tkinter Frame object
            This has the frame that contains the entire Object Class Manager
            window.
        new_class_var : string (Default: None)
            This is the variable the current empty text box places its text 
        new_class_entry : tkinter Entry object
            This is the Entry widget where new class names are entered
            
        Raises
        ------
        None
    
        Returns
        -------
        None
            
        '''
        
        # The base Frame
        self.class_manager_frame = Frame(self.class_manager_window,
                                         height=400,
                                         width=400)
        self.class_manager_frame.pack()
        
        # Blank Space at the top of the Frame
        top_label = Label(self.class_manager_frame, 
                          text="",)
        top_label.grid(row=0, column=0, columnspan=3)
        
        # Add a new row for each object class in the project
        for i, c in enumerate(self.root_app.class_list):
            
            # The text label
            class_label = Label(self.class_manager_frame, 
                                text="%d. %s" % ((i+1), c))
            class_label.grid(row=i+1, column=0, sticky='w', pady=1)
            
            # Change color button
            color_button = Button(self.class_manager_frame, 
                                  width=1, 
                                  height=1,
                                  bg=self.root_app.colorspace[i],
                                  command=lambda i=i: self._choose_color(i))
            color_button.grid(row=i+1, column=1, pady=1)

            # Prompt to rename the object class
            rename_button = Button(self.class_manager_frame, 
                                   text="Rename", 
                                   command=lambda i=i: self._rename_class_window(i))
            rename_button.grid(row=i+1, column=2, pady=1)
            
            # Prompt to remove the object class
            remove_button = Button(self.class_manager_frame, 
                                   text="Delete", 
                                   command=lambda i=i: self._check_before_remove(i))
            remove_button.grid(row=i+1, column=3, pady=1)
            
            # Show the number of annotations for each class exist
            instances = self.root_app.class_count[i]
            instance_label = Label(self.class_manager_frame, 
                                   text=' %d labeled instances.' % instances)
            instance_label.grid(row=i+1, column=4)
        
        # Entry box for new class
        self.new_class_var = StringVar()
        self.new_class_entry = Entry(self.class_manager_frame,
                      textvariable=self.new_class_var)
        self.new_class_entry.grid(row=len(self.root_app.class_list)+1, 
                                  column=0)
        
        # Button that adds new class
        add_button = Button(self.class_manager_frame, 
                               text="Add Class", 
                               command=self._add_class_action)
        add_button.grid(row=len(self.root_app.class_list)+1, column=2)
                    
        # Button that closes the object class manager
        close_button = Button(self.class_manager_frame, 
                              text="Close",
                              command=self.class_manager_window.destroy)
        close_button.grid(row=len(self.root_app.class_list)+2, 
                          column=0, 
                          columnspan=4)

    def _rename_class_window(self, button_id):
        '''
        Displays a popup window that prompts to rename a single object class
          
        Parameters
        ----------
        button_id : int
            This points to the object class that is being renamed

        Attributes
        ----------
        rename_entry : tkinter Entry object
            This is the text box that is used to rename an object class
        rename_class_prompt : tkinter Toplevel object
            This is the window that contains the class rename prompt
            
        Raises
        ------
        None
    
        Returns
        -------
        None
            
        '''      
        
        # This is the popup window
        self.rename_class_prompt = tk.Toplevel()
        self.rename_class_prompt.wm_title("Rename Class")
        self.rename_class_prompt.geometry("%dx%d" % (400,200))
        self.rename_class_prompt.grab_set()

        # Grab the current class name
        current_class = self.root_app.class_list[button_id]

        # Draw the frame that will contain the rename class prompt
        rename_class_frame = Frame(self.rename_class_prompt,
                                         height=400,
                                         width=400)
        rename_class_frame.pack()
        
        # Label prompt
        label = Label(rename_class_frame, 
                      text='Rename \"%s\" Class to:' % current_class)
        label.grid(row=0, column=0, columnspan=2)
        
        # Entry box that the user will use to rename the object class
        self.rename_class_var = StringVar()
        self.rename_entry = Entry(rename_class_frame, 
                      textvariable=self.rename_class_var)
        self.rename_entry.grid(row=1, column=0, columnspan=2)
        
        # Button used to rename the object class
        i = button_id
        rename_button = Button(rename_class_frame, 
                            text="Ok", 
                            command=lambda i=i: self._rename_class_action(i))
        rename_button.grid(row=2, column=0)
                    
        # Button to close the prompt without renaming
        close_button = Button(rename_class_frame, 
                              text="Cancel",
                              command=self.rename_class_prompt.destroy)
        close_button.grid(row=2, column=1)        

    def _rename_class_action(self, button_id):
        '''
        Renames the object class when the "ok" button is pressed
          
        Parameters
        ----------
        button_id : int
            This points to the object class that is being renamed
            
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
        
        # Old and new object class names
        new_class = self.rename_entry.get()
        
        # Don't rename object class with an empty string
        if new_class == '':
            # print('Field was empty.  Please provide a new class name.')
            pass
        else:
            # Rename class in project
            self.root_app.class_list[button_id] = new_class  
            # Delete rename class prompt
            self.rename_class_prompt.destroy()
            # Redraw class manager with new class name
            self.class_manager_frame.destroy()
            self.draw_frame()
            # Change was made, need to save project
            self.root_app.saved = False
            # Redraw the workspace
            self.root_app._draw_workspace()            

                            
    def _add_class_action(self):
        '''
        Add the object class (in the entry box) when the "Add Class" button is
        pressed.
          
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
        None
            
        '''   
        
        # Grab the new class label from the object class manager entry box
        new_class = self.new_class_entry.get()
        
        # If no class is entered, do nothing
        if new_class == "":
            # print("Provide new class name.")
            pass
        # If class provided is already in project, do nothing
        elif new_class in self.root_app.class_list:
            # print("Class already exists.")
            pass
        else:
            
            # If one of the top default colors is available, assign the first
            # one to the new object class, else assign a random color
            if len(self.root_app.top_colors_free) > 0:
                col = self.root_app.top_colors_free.pop(0)
                self.root_app.top_colors_used.append(col)
            else:
                col = "#%06x" % random.randint(0, 0xFFFFFF)
                
            # Save object class color
            self.root_app.colorspace.append(col)
            # Add the new object class to the project
            self.root_app.class_list.append(new_class)
            # Initialize the class counter at zero
            self.root_app.class_count.append(0)
        
            # Redraw the object class manager
            self.class_manager_frame.destroy()
            self.draw_frame()
            
            # Change was made, need to save project
            self.root_app.saved = False
            
            # Redraw the workspace
            self.root_app._draw_workspace()
    
    def _check_before_remove(self, button_id):
        '''
        Displays a prompt to confirm if the user wants to delete the object 
        class from the project since there is no current capability to undo.
          
        Parameters
        ----------
        button_id : int
            This points to the object class that is being remove
            
        Attributes
        ----------
        popup_window : tkinter Toplevel object
            This is the actual window that contains the prompt
            
        Raises
        ------
        None
    
        Returns
        -------
        None
            
        '''   
        
        # Create a popup window
        self.popup_window = tk.Toplevel()
        self.popup_window.geometry("300x100") 
        self.popup_window.wm_title("Remove Class?")
        self.popup_window.grab_set()
        
        # Create the new window background frame
        bkgd_frame = Frame(self.popup_window)
        bkgd_frame.place(x=0, y=0, width=300, height=100)
        
        # Add Label for the remove class prompt
        prompt_txt = "Delete Class?  You cannot undo this action."
        prompt = Label(bkgd_frame, text=prompt_txt)
        prompt.place(x=10, y=0, width=280, height=30)
        
        # Add the button that confirms the user wants to delete the object 
        # class
        i=button_id
        yes_button = Button(bkgd_frame, 
                            text="Remove", 
                            command=lambda i=i: self._remove_class(i))
        yes_button.place(x=90, y=30, height=30, width=50)

        # Add the button that confirms the user does not want to delete the  
        # object class        
        cancel_button = Button(bkgd_frame, text="Cancel", 
                               command=self.popup_window.destroy)
        cancel_button.place(x=160, y=30, height=30, width=50)

    def _remove_class(self, button_id):
        '''
        Removes the object class assigned to button_id index
          
        Parameters
        ----------
        button_id : int
            This points to the object class that is being removed
            
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
        
        # This is the color that will be no longer used
        color = self.root_app.colorspace[button_id]
        
        # If this is one of the top default colors, then make it available for
        # reuse
        if color in self.root_app.top_colors:
            self.root_app.top_colors_free.insert(0, color)
            self.root_app.top_colors_used.remove(color)            
        
        # Remove the object class from the project
        self.root_app.colorspace.pop(button_id)
        self.root_app.class_count.pop(button_id)
        self.root_app.class_list.pop(button_id)

        # Remove all annotations in the project containing that object class
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
        
        # Redraw object class manager
        self.class_manager_frame.destroy()
        self.draw_frame() 
        
        # Change was made, need to save project
        self.root_app.saved = False
        
        # Redraw the workspace
        self.root_app._draw_workspace()
        if hasattr(self, 'popup_window'):
            self.popup_window.destroy()                
