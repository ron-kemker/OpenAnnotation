# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 13:31:09 2021

@author: Ronald Kemker
"""

import random, glob
import tkinter as tk
from tkinter import Frame, Label, Button, Entry, colorchooser, StringVar
from tkinter.filedialog import askopenfilenames, askdirectory
    
class ProjectWizard(object):
    
    def __init__(self, menu_app):
        '''
        Popup for a New Project Wizard GUI.
        
        Parameters
        ----------
        menu_app : Pass a pointer to the Menu object to access parent
                   variables.
        
        Attributes
        ----------
        root_app : AnnotationTool object
            A pointer to the root_application to access "global"
            variables.
        menu_app : AppMenu object
            Pass a pointer to the Menu object to access parent
                   variables.  
        window_width : int (default=1024)
            The width of the Project Wizard window in pixels
        window_height : int (default=768)
            The width of the Project Wizard window in pixels
        left_pane_width : int (default=300)
            The width of the left pane of the Project Wizard in pixels
        right_pane_width : int (default=723)
            The width of the right pane of the Project Wizard in pixels  
        wizard_window : tkinter TopLevel object
            The actual project wizard window
        background : tkinter Frame object
            The background of the project wizard window that everything is
            drawn on
                    
        Raises
        ------
        None
    
        Returns
        -------
        None
    
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
        self.wizard_window.grab_set()
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
        '''
        Populates the left pane frame
          
        Parameters
        ----------
        None
    
        Attributes
        ----------
        left_pane : tkinter Frame object
            This has the frame that contains the image import tools
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
        add_file_button = Button(self.left_pane,
                                      text ='Import File(s) to Project',
                                      command = self._import_file,
                                      width=200,
                                      height=50)
        add_file_button.place(x=50, y=50, 
                                   width=200, height=50)

        # Add all files in a directory to the project
        add_dir_button = Button(self.left_pane,
                            text ='Import Entire Directory to Project',
                            command = self._import_files_in_directory,
                            width=200,
                            height=50)
        add_dir_button.place(x=50, y=125, 
                                   width=200, height=50)

        # Display the number of files imported
        msg = 'Project has %d files for annotation.'
        counter_label = Label(self.left_pane, 
                              width=200,
                              height=25,
                              text= msg % len(self.root_app.annotations))
        counter_label.place(x=50, y=200, width=200, height=25)

        # Build the Project
        build_proj_button = Button(self.left_pane,
                                      text ='Build Project',
                            command = self._build_project,
                            width=200,
                            height=50,
                            bg='Green')
        build_proj_button.place(x=50, y=self.window_height-200, 
                                   width=200, height=50)
        
        # Go back to the main menu
        cancel_button = Button(self.left_pane,
                                      text ='Main Menu',
                            command = self._cancel_project,
                            width=200,
                            height=50,
                            bg='Red')
        cancel_button.place(x=50, y=self.window_height-125, 
                                   width=200, height=50)


    def _draw_right_pane(self):
        '''
        Populates the right pane frame
          
        Parameters
        ----------
        None
    
        Attributes
        ----------
        right_pane : tkinter Frame object
            This has the frame that contains the entire Object Class Manager
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
                            command=lambda i=i: self._rename_class_window(i))
            rename_button.place(x=200, y=0, width=50, height=25)
            
            # Button to delete an object class
            remove_button = Button(row_frame, 
                            text="Delete", 
                            command=lambda i=i: self._check_before_remove(i))
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
        self.new_class_var = StringVar()
        
        self.new_class_entry = Entry(row_frame,
                      textvariable=self.new_class_var)
        self.new_class_entry.place(x=0, y=0, width=225, height=25)
        
        # The button that adds the new object class to the project
        add_button = Button(row_frame, 
                               text="Add Class", 
                               command=self._add_class_action)
        add_button.place(x=225, y=0, width=75, height=25)


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
        
        # Redraw
        self._draw_right_pane()
                
        # Redraw the workspace
        self.root_app._draw_workspace()
        
    def _import_file(self, files=None, meta=None):
        '''
        This is the command that imports an image file into the project.

        Parameters
        ----------
        file : STRING (default=None)
            This is only used for testing purposes
        meta : exif.Image object (default=None)
            This is only used for testing purposes

        Attributes
        ----------
        None
            
        Raises
        ------
        None
        
        Returns
        -------
        None.

        '''
        
        # Prompt for an image file to be imported
        if self.root_app.window.winfo_ismapped():

            files = askopenfilenames(filetypes=(("Image File", 
                                               self.root_app.file_ext),),
                                                    initialdir = "/",
                                                    title = "Select file")

        # If no image was selected, then exit function
        if not files:
            return False
        
        for file in files:
            # If image is not already in project, then add it
            if file not in self.root_app.file_list:
                
                # Add this to the list of files in the project
                self.root_app.file_list.append(file)
                
                # Create an Annotation object from the image
                self.menu_app.file_to_annotation(file, meta)
            
                # If this is the first image being loaded, then add it to canvas
                if not hasattr(self, 'img') and\
                    self.root_app.window.winfo_ismapped():
                    self.root_app._load_image_from_file()  
                
        # Redraw Left Pane
        self._draw_left_pane()
        
        return True
                                
    def _import_files_in_directory(self, new_dir=None, meta=None):
        '''
        This imports an entire directory of images into the project.        

        Parameters
        ----------
        new_dir : STRING (default=None)
            This is only used for testing purposes
        meta : exif.Image object (default=None)
            This is only used for testing purposes
            
        Attributes
        ----------
        None
            
        Raises
        ------
        None
        
        Returns
        -------
        None.

        '''
        
        # Prompt for a directory to search for imagery
        if not new_dir and self.root_app.window.winfo_ismapped():
            new_dir = askdirectory()
        
        # If no directory selected, exit function
        if not new_dir:
            return False
        
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
        if not hasattr(self, 'img') and self.root_app.window.winfo_ismapped():
            self.root_app._load_image_from_file()  
            
        # Redraw Left Pane
        self._draw_left_pane()
        
        return True

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
        
        # Popup window for renaming object class
        self.rename_class_prompt = tk.Toplevel()
        self.rename_class_prompt.wm_title("Rename Class")
        self.rename_class_prompt.geometry("%dx%d" % (400,200))
        self.rename_class_prompt.grab_set()
        
        # Current object class name
        current_class = self.root_app.class_list[button_id]

        # Background frame for popup window
        rename_class_frame = Frame(self.rename_class_prompt,
                                         height=400,
                                         width=400)
        rename_class_frame.pack()
        
        # Label prompt in popup
        label = Label(rename_class_frame, 
                      text='Rename \"%s\" Class to:' % current_class)
        label.grid(row=0, column=0, columnspan=2)
        
        # Space to write the new object class into
        self.rename_class_var = StringVar()
        self.rename_entry = Entry(rename_class_frame, 
                      textvariable=self.rename_class_var)
        self.rename_entry.grid(row=1, column=0, columnspan=2)
        
        # Rename and Cancel buttons
        i = button_id
        rename_button = Button(rename_class_frame, 
                            text="Ok", 
                            command=lambda i=i: self._rename_class_action(i))
        rename_button.grid(row=2, column=0)
                    
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
                
        # New name to rename the object class to
        new_class = self.rename_entry.get()
        
        # If nothing was entered, then do nothing
        if new_class == '':
            # print('Field was empty.  Please provide a new class name.')
            pass
        else:
            # Replace name in class list
            self.root_app.class_list[button_id] = new_class
                       
            # Redraw Right pane in New Project Wizard
            self.rename_class_prompt.destroy()
            self._draw_right_pane()
                          
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
        # Get the new object class name from entry widget                
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
        
        # Remove the entry from the colorspace dictionary
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

        if hasattr(self, 'popup_window'):
            self.popup_window.destroy()  
        
    def _cancel_project(self):
        '''
        Go back to default load screen
        
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
        None.

        '''
        # Close the New Project Wizard
        self.wizard_window.destroy()
        
        # Reload the Main Menu
        self.menu_app._close_command()

    def _build_project(self):
        '''
        Build a new project

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
        None.

        '''
        # New class has been added, so we will need to save project
        self.root_app.saved = False
        
        # Get rid of the Wizard
        self.wizard_window.destroy()
        
        # Redraw the Workspace
        self.root_app._draw_workspace()