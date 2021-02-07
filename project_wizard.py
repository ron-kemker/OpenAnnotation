# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 13:31:09 2021

@author: Ronald Kemker
"""

import random, glob
import tkinter as tk
from tkinter import Frame, Label, Button, Entry, colorchooser
from tkinter.filedialog import askopenfilename, askdirectory
    
class ProjectWizard(object):
    
    def __init__(self, menu_app):
        '''
        Popup for a New Project Wizard GUI.
        
        Parameters
        ----------
        menu_app : Pass a pointer to the Menu object to access parent
                   variables.
        
        Returns
        -------
        None.
    
        '''
        # Parent Menu Object
        self.menu_app = menu_app
        
        # Parent AnnotationTool Object
        self.root_app = menu_app.root_app

        # Static Window Dimensions
        self.window_width = 1024
        self.window_height = 768
        self.left_pane_width = 300
        self.right_pane_width = self.window_width - self.left_pane_width - 1
        
        # Popup for the New Project Wizard
        self.wizard_window = tk.Toplevel()
        self.wizard_window.wm_title("Project Wizard")
        self.wizard_window.geometry("%dx%d" % (self.window_width,
                                               self.window_height))
        
        # Window Background Fram
        self.background = Frame(self.wizard_window, 
                                width = self.window_width,
                                height = self.window_height,
                                bg='black')
        self.background.pack()
        self._draw_left_pane()
        self._draw_right_pane()
        
    def _draw_left_pane(self):
        
        if hasattr(self, 'left_pane'):
            self.left_pane.destroy()
        
        # Left Pane Contains Different Buttons
        self.left_pane = Frame(self.background, 
                               width = self.left_pane_width,
                               height = self.window_height, 
                               bg=None)
        self.left_pane.place(x=0, y=0, width = self.left_pane_width, 
                             height=self.window_height)

        # Add an individual file to the project
        self.add_file_button = Button(self.left_pane,
                                      text ='Import File to Project',
                                      command = self._import_file,
                                      width=200,
                                      height=50)
        self.add_file_button.place(x=50, y=50, 
                                   width=200, height=50)

        # Add all files in a directory to the project
        self.add_dir_button = Button(self.left_pane,
                            text ='Import Files in Directory to Project',
                            command = self._import_files_in_directory,
                            width=200,
                            height=50)
        self.add_dir_button.place(x=50, y=125, 
                                   width=200, height=50)

        # Display the number of files imported
        msg = 'Project has %d files for annotation.'
        counter_label = Label(self.left_pane, 
                              width=200,
                              height=25,
                              text= msg % len(self.root_app.annotations))
        counter_label.place(x=50, y=200, width=200, height=25)

        # Build the Project
        self.build_proj_button = Button(self.left_pane,
                                      text ='Build Project',
                            command = self._build_project,
                            width=200,
                            height=50,
                            bg='Green')
        self.build_proj_button.place(x=50, y=self.window_height-200, 
                                   width=200, height=50)
        
        # Go back to the main menu
        self.cancel_button = Button(self.left_pane,
                                      text ='Main Menu',
                            command = self._cancel_project,
                            width=200,
                            height=50,
                            bg='Red')
        self.cancel_button.place(x=50, y=self.window_height-125, 
                                   width=200, height=50)


    def _draw_right_pane(self):
        '''
        Draw and update the Object Class Manager         

        Returns
        -------
        None.

        '''

        if hasattr(self, 'right_pane'):
            self.right_pane.destroy()
    
        # Draw the Right Pane to draw everything on
        self.right_pane = Frame(self.background, 
                               width = self.right_pane_width,
                               height = self.window_height, 
                               bg=None)
        self.right_pane.place(x=self.left_pane_width+1, 
                              y=0, 
                              width = self.right_pane_width, 
                              height=self.window_height)

        # Print "Object Class Manager" at the top
        title_frame = Label(self.right_pane,
                            width=self.right_pane_width,
                            height = self.window_height,
                            text = 'Object Class Manager',
                            font = ('Arial', 12, 'bold'),
                            )
        title_frame.place(x = 10,
                          y = 10,
                          height = 25,
                          width = self.right_pane_width)

        # Add all of the individual object classes
        for i, c in enumerate(self.root_app.class_list):
            
            # Create frame for a single row (organizing things)
            row_frame = Frame(self.right_pane, 
                        width=300, 
                        height=25,
                        bg=None)
            row_frame.place(x = self.right_pane_width/2-150,
                      y = (i+2)*25,
                      width = 300,
                      height=25)
            
            # Number/Name of object class
            class_label = Label(row_frame, 
                                text="%d. %s" % ((i+1), c),
                                width=175,
                                height=25,
                                justify='left',
                                font=('Arial',10))
            class_label.place(x=0, y=0, width=175, height=25)
            
            # This is the button that identifies the corresponding bounding
            # box color for each object class
            color_button = Button(row_frame, 
                                  width=25, 
                                  height=25,
                                  bg=self.root_app.colorspace[i],
                                  command=lambda i=i: self._choose_color(i))
            color_button.place(x=175, y=0, width=25, height=25)

            # Pops up a window to rename an object class
            rename_button = Button(row_frame, 
                                   text="Rename", 
                                   command=lambda i=i: self._rename_class(i))
            rename_button.place(x=200, y=0, width=50, height=25)
            
            # Button to delete an object class
            remove_button = Button(row_frame, 
                            text="Delete", 
                            command=lambda i=i: self._remove_class(i))
            remove_button.place(x=250, y=0, width=50, height=25)
            

        # Row for the "add class" entry
        row_frame = Frame(self.right_pane, 
                    width=300, 
                    height=25,
                    bg=None)
        row_frame.place(x = self.right_pane_width/2-150,
                  y = (len(self.root_app.class_list) + 2)*25,
                  width = 300,
                  height=25)                    
        self.new_class_var = None
        
        self.new_class_entry = Entry(row_frame,
                      textvariable=self.new_class_var)
        self.new_class_entry.place(x=0, y=0, width=225, height=25)
        
        # The button that adds the new object class to the project
        add_button = Button(row_frame, 
                               text="Add Class", 
                               command=self._add_class)
        add_button.place(x=225, y=0, width=75, height=25)


    def _choose_color(self, button_id):
        '''
        Choose the color of the bounding boxes for a corrsponding object class
        
        Parameters
        ----------
        button_id : INT
            Corresponding button that was pressed, so we change the right 
            color.
            
        Returns
        -------
        None.

        '''
        
        # Ask for which color to change the object class BBOXes to
        color_code = colorchooser.askcolor(title="Choose Color")
        
        # The key used for searching in the dictionaries below
        class_id = self.root_app.class_list[button_id]
        
        # If this is one of the top colors you are no longer using
        if self.root_app.colorspace[class_id] in self.root_app.top_colors:
            # Make the color available again
            self.root_app.top_colors_free.insert(0, self.root_app.colorspace[class_id])
            # It is no longer being used
            self.root_app.top_colors_used.remove(self.root_app.colorspace[class_id])
        
        # Change the color
        self.root_app.colorspace[class_id] = color_code[1]
        
        # Redraw
        self._draw_right_pane()
        self.root_app.saved = False
        self.root_app._draw_workspace()
        
    def _import_file(self):
        '''
        This is the command that imports an image file into the project.

        Returns
        -------
        None.

        '''
        
        # Prompt for an image file to be imported
        file = askopenfilename(filetypes=(("Image File", 
                                           self.root_app.file_ext),),
                                                initialdir = "/",
                                                title = "Select file")

        # If no image was selected, then exit function
        if not file:
            return
        
        # If image is not already in project, then add it
        elif file not in self.root_app.file_list:
            
            # Add this to the list of files in the project
            self.root_app.file_list.append(file)
            
            # Create an Annotation object from the image
            self.menu_app.file_to_annotation(file)
            
            # If this is the first image being loaded, then add it to canvas
            if not hasattr(self, 'img'):
                self.root_app._load_image_from_file()  
                
        # Redraw Left Pane
        self._draw_left_pane()
                                
    def _import_files_in_directory(self, new_dir=None):
        '''
        This imports an entire directory of images into the project.        

        Returns
        -------
        None.

        '''
        
        # Prompt for a directory to search for imagery
        if not new_dir:
            new_dir = askdirectory()
        
        # If no directory selected, exit function
        if not new_dir:
            return
        
        # Iterate throug all of the possible file extensions and them to a 
        # list
        tmp_file_list = []
        for fe in self.root_app.file_ext:
            tmp_file_list += glob.glob(new_dir + '\*%s' % fe)

        # Create an Annotation object from the image
        for file in tmp_file_list:
            self.menu_app.file_to_annotation(file)

        # Add all of the image files to the existing list of files in the 
        # project
        self.root_app.file_list += tmp_file_list
        
        # If this is the first image being loaded, then add it to canvas
        if not hasattr(self, 'img'):
            self.root_app._load_image_from_file()  
            
        # Redraw Left Pane
        self._draw_left_pane()
           
        
    def _rename_class_action(self, button_id):
        '''
        This function performs all of the object class renaming functionality
        
        Parameters
        ----------
        button_id : INT
            Corresponding button that was pressed, so we rename the right 
            objcet.
            
        Returns
        -------
        None.

        '''
                
        # New name to rename the object class to
        new_class = self.rename_entry.get()
        
        # If nothing was entered, then do nothing
        if new_class == '':
            print('Field was empty.  Please provide a new class name.')
        else:
            # Replace name in class list
            self.root_app.class_list[button_id] = new_class
                       
            # Redraw Right pane in New Project Wizard
            self.rename_class_prompt.destroy()
            self._draw_right_pane()
                           
    def _rename_class(self, button_id):
        '''
        Popup windows prompts to rename a corresponding object class
        
        Parameters
        ----------
        button_id : INT
            Corresponding button that was pressed, so we change the right 
            color.
            
        Returns
        -------
        None.

        '''
        
        # Popup window for renaming object class
        self.rename_class_prompt = tk.Toplevel()
        self.rename_class_prompt.wm_title("Rename Class")
        self.rename_class_prompt.geometry("%dx%d" % (400,200))
        
        # Current object class name
        current_class = self.root_app.class_list[button_id]

        # Background frame for popup window
        self.rename_class_frame = Frame(self.rename_class_prompt,
                                         height=400,
                                         width=400)
        self.rename_class_frame.pack()
        
        # Label prompt in popup
        label = Label(self.rename_class_frame, 
                      text='Rename \"%s\" Class to:' % current_class)
        label.grid(row=0, column=0, columnspan=2)
        
        # Space to write the new object class into
        self.new_class_name_var = None
        self.rename_entry = Entry(self.rename_class_frame, 
                      textvariable=self.new_class_name_var)
        self.rename_entry.grid(row=1, column=0, columnspan=2)
        
        # Rename and Cancel buttons
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
        '''
        Functionailty for Adding a new object class
        
        Parameters
        ----------
        None
            
        Returns
        -------
        None.

        '''
        # Get the new object class name from entry widget                
        new_class = self.new_class_entry.get()
        
        # If nothing is entered, do nothing
        if new_class == "":
            print("Provide new class name.")
        # if class list already exists, do nothing
        elif new_class in self.root_app.class_list:
            print("Class already exists.")
        else:
            
            # See if any of the recommended colors still exist
            if len(self.root_app.top_colors_free) > 0:
                # Move next recommended color from "free" stack to "used" stack
                col = self.root_app.top_colors_free.pop(0)
                self.root_app.top_colors_used.append(col)

            else:
                # Assign a random number if no recommended colors remain
                col = "#%06x" % random.randint(0, 0xFFFFFF)
            
            # Add key/color combination to colorspace dictionary
            self.root_app.colorspace.append(col)
            
            # Add new class name to class list
            self.root_app.class_list.append(new_class)
            
            # Initialize class count to 0
            self.root_app.class_count.append(0)
            
        # Redraw right pane
        self._draw_right_pane()
            
    def _remove_class(self, button_id):
        '''
        Remove object class from list

        Parameters
        ----------
        button_id : INT
            Corresponding button that was pressed, so we remove the right 
            object class.

        Returns
        -------
        None.

        '''
        
        # # Remove the entry from the colorspace dictionary
        color = self.root_app.colorspace.pop(button_id)
        
        # If this is a recommended color, readd it back to the "free" stack
        if color in self.root_app.top_colors:
            self.root_app.top_colors_free.insert(0, color)
            self.root_app.top_colors_used.remove(color)            
        
        # Remove the entry from the class list
        self.root_app.class_list.pop(button_id)
        # self.root_app.colorspace.pop(button_id)
        self.root_app.class_count.pop(button_id)

        # Redraw the right pane
        self._draw_right_pane()

        
    def _cancel_project(self):
        '''
        Go back to default load screen

        Returns
        -------
        None.

        '''
        # Close the New Project Wizard
        self.wizard_window.destroy()
        
        # Reload the Main Menu
        self.menu_app._close_command()

    def _build_project(self):
        '''
        Build a new project


        Returns
        -------
        None.

        '''
        
        # New class has been added, so we will need to save project
        self.root_app.saved = False
        
        # Get rid of the Wizard
        self.wizard_window.destroy()
        
        # Redraw the Workspace
        self.root_app._draw_workspace()