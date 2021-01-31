# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 21:25:58 2021

@author: Ronald Kemker
"""

# External Dependencies
import glob, exif, pickle, csv
from PIL import Image
from plum._exceptions import UnpackError
import tkinter as tk
from tkinter import Frame, Label, Menu, Button, Canvas, Entry
from tkinter.filedialog import askopenfilename, asksaveasfilename, \
    askdirectory

from help import HelpMenu
from project_wizard import ProjectWizard

class AppMenu(object):
   
    def __init__(self, root_app):
        '''
        This is the menu bar at the top of the application.
        
        Parameters
        ----------
        root_app : Pass a pointer to the root_application to access parent
                   variables.
        
        Returns
        -------
        None.
    
        '''           
        
        self.root_app = root_app

    def _draw_menu(self):
        '''
        This builds the file menu.
        

        Returns
        -------
        None.

        '''
        
        # Add Menu to application window
        menu = Menu(self.root_app.window)
        self.root_app.window.config(menu=menu)
        
        
        # "File" Menu for Creating/Managing Projects
        fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New Blank Project", 
                             command=self._new)
        fileMenu.add_command(label="New Project Wizard", 
                             command=self._new_project_wizard)
        fileMenu.add_command(label="Open Project", 
                             command=self._open)
        
        # If a project is open, allow that project to be saved/closed
        if self.root_app.project_open:
            fileMenu.add_command(label="Save Project", command=self._save)
            fileMenu.add_command(label="Close Project", command=self._close)
        
        # If a project is open, allow files and entire directories to be added
        fileMenu.add_separator()
        if self.root_app.project_open:
            fileMenu.add_command(label="Import File", 
                                 command=self._import_file)
            fileMenu.add_command(label="Import Directory", 
                                 command=self._import_files_in_directory) 
            
            # Export the project to a CSV file
            fileMenu.add_command(label="Export Project to CSV", 
                                  command=self._csv_exporter)
            fileMenu.add_separator()
        
        # Quit the entire application
        fileMenu.add_command(label="Quit", command=self._quit)
        
        
        # Tools to be accessed when a project is open
        #    Class Manager : Opens new window that allows classes to be added,
        #                  removed, or changed.
        #    Reset Image : Delete all annotations currently in the image
        if self.root_app.project_open:
            toolMenu = Menu(menu)
            menu.add_cascade(label="Tools", menu=toolMenu)
            toolMenu.add_command(label="Class Manager", 
                            command=self.root_app._draw_object_class_manager)
            
            if len(self.root_app.annotations):
                toolMenu.add_command(label="Reset Image", 
                                     command=self.root_app._reset_image)
                
                toolMenu.add_command(label='Select Image #',
                                     command=self.select_image)
                
                
                
        # This is the Help Menu        
        helpMenu = Menu(menu)
        # Create a popup that Displays tutorial documentation for the user
        menu.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="OpenAnnotation Documentation", 
                             command=HelpMenu(self)._draw_menu)
        # Create a popup with basic information about the program
        helpMenu.add_command(label="About OpenAnnotation", 
                             command=self.draw_about_box)

    def select_image(self):
        '''
        Displays a prompt to select which image in the project to skip ahead 
        (or behind) to

        Returns
        -------
        None.

        '''
        
        # Build Prompt Window
        self.prompt = tk.Toplevel()
        self.prompt.wm_title("Select Image")
        self.prompt.geometry("%dx%d" % (400,200))
        
        
        # Build Frame Inside Window
        prompt_frame = Frame(self.prompt,
                                         height=200,
                                         width=400)
        prompt_frame.pack()
        
        # Prompt label
        label = Label(prompt_frame, 
                      text="Move to Image #")
        label.place(x=0, y=25, width=400, height=25)
        
        # The entry box
        prompt_var = None
        self.prompt_entry = Entry(prompt_frame, 
                      textvariable=prompt_var)
        self.prompt_entry.place(x=100, y=75, width=200, height=25)
        
        # Ok/Cancel Buttons
        ok_button = Button(prompt_frame, 
                            text="Ok",
                            height=25,
                            width=50,
                            command=self.select_image_action)
        ok_button.place(x=145, y=125, width=50, height=25)
                    
        cancel_button = Button(prompt_frame, 
                              text="Cancel",
                              command=self.prompt.destroy)
        cancel_button.place(x=205, y=125, width=50, height=25)
        

    def select_image_action(self):
        '''
        Retrieves a value from select_image Entry and sets the current_file to
        that value

        Returns
        -------
        None.

        '''
        
        # Pull the value from the entry box
        entry_val = int(self.prompt_entry.get())-1
        
        # If a valid number is entered
        if entry_val >= 0 and entry_val < len(self.root_app.annotations): 
            # Set the current file
            self.root_app.current_file = entry_val
             
            # Refresh GUI
            self.root_app._load_image_from_file() 
            self.root_app._draw_workspace()
            # Destroy Prompt
            self.prompt.destroy()
        else:
            print('Project Image Index Out of Bounds')

    def file_to_annotation(self, file):
        '''
        Creates an Annotation object based on the image.
        
        Parameters
        ----------
        file : STRING
            Path and Filename of Image to be annotated.

        Returns
        -------
        None.

        '''
        
        self.root_app.annotations.append(Annotation(file))
        
        # EXIF data is not present in all images (e.g., png files).  If there
        # is EXIF data, use it to figure out how the image needs to be rotated.
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
        # This is the error when no EXIF data is found.
        except UnpackError:
            pass

    def _import_file(self):
        '''
        This is the command that imports an image file into the project.

        Returns
        -------
        None.

        '''
        
        # Prompot for an image file to be imported
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
            self.file_to_annotation(file)
            
            # If this is the first image being loaded, then add it to canvas
            if not hasattr(self, 'img'):
                self.root_app._load_image_from_file()  
    
            # Refresh GUI
            self.root_app._draw_workspace()
            
            # The project needs to be saved
            self.root_app.saved = False       
                
    def _import_files_in_directory(self):
        '''
        This imports an entire directory of images into the project.        

        Returns
        -------
        None.

        '''
        
        # Prompt for a directory to search for imagery
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
            self.file_to_annotation(file)

        # Add all of the image files to the existing list of files in the 
        # project
        self.root_app.file_list += tmp_file_list
        
        # If this is the first image being loaded, then add it to canvas
        if not hasattr(self, 'img'):
            self.root_app._load_image_from_file()  
            
        # Refresh GUI
        self.root_app._draw_workspace()
        
        # The project needs to be saved
        self.root_app.saved = False    
    
    def _new(self):
        '''
        Create an empty project.        

        Returns
        -------
        None.

        '''
        
        # This it he list of filenames in the project
        self.root_app.file_list = []
        
        # The project is open, so other menu items will be made available.
        self.root_app.project_open = True
 
        # This is a list of Annotation objects that correspond to each 
        # filename
        self.root_app.annotations = [] 
        
        # Refresh GUI (which should be empty)
        self.root_app._draw_workspace()
        
        # Empty project doesn't need to be saved
        self.root_app.saved = True
  
    def _open(self):
        '''
        Open a saved project into the application.

        Returns
        -------
        None.

        '''
        
        # Prompt for what project should be opened
        file_name = askopenfilename(filetypes=(("PKL files","*.pkl"),),
                                                initialdir = "/",
                                                title = "Select file")
        
        # If no project is selected, there is no project to open
        if not file_name:
            return
        
        # Load the project and update the project variables with where it was
        # last saved
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

        # Already saved project doesn't need to be saved again
        self.root_app.saved = True
        
        # The project is open, so other menu items will be made available.
        self.root_app.project_open = True

        # Load the image from the last save point
        self.root_app._load_image_from_file()  
        
        # Refresh the GUI
        self.root_app._draw_workspace()
        
    def _save(self):
        '''
        Command that saves the project.  Currently puts all of the relevant
        information into a pickle file.

        Returns
        -------
        None.

        '''
 
        # Prompt where the files will be saved to
        file_name = asksaveasfilename(filetypes=(("PKL files","*.pkl"),),
                                                initialdir = "/",
                                                title = "Select file")    

        # If no filename is specified, then exit the save command
        if not file_name:
            return
    
        # Dictionary that will be pickled
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
        
        # Save the .pkl file
        with open(file_name, "wb") as f:
            pickle.dump(save_dict, f)
            
        # The file has now been saved
        self.root_app.saved = True

    def _close(self):
        '''
        Draws the prompt when the close options is clicked in the menu.  
        
        Returns
        -------
        None.

        '''        
        
        # If not saved, then prompt to save, close w/o saving, or cancel
        if not self.root_app.saved:
            
            # Popup window
            self.popup_window = tk.Toplevel()
            self.popup_window.geometry("300x100") 
            self.popup_window.wm_title("Save Work?")
            
            
            # Background to draw on
            bkgd_frame = Frame(self.popup_window, width=300, height=100)
            bkgd_frame.pack()
            
            # Label displaying the prompt
            prompt_txt = "Close without saving?"
            prompt = Label(bkgd_frame, text=prompt_txt)
            prompt.grid(row=0, column=0, columnspan=3, sticky='nsew')
            
            # The three button options
            yes_button = Button(bkgd_frame, text="Save", 
                                command=self._save_close_command)
            yes_button.grid(row=1, column=0)
            no_button = Button(bkgd_frame, text="Close", 
                               command=self._close_command)
            no_button.grid(row=1, column=1)           
            cancel_button = Button(bkgd_frame, text="Cancel", 
                                   command=self.popup_window.destroy)
            cancel_button.grid(row=1, column=2)            
        # Already saved, so just close the project
        else:
            self._close_command()

        # Get rid of the extra menu options that pertain to projects
        self.root_app.project_open = False


    def _save_close_command(self):
        '''
        Save and then close the project.

        Returns
        -------
        None.

        '''
        
        self._save()
        self._close_command()
        
    def _close_command(self):  
        '''
        Close the project.
        
        Returns
        -------
        None.

        '''        

        # Get rid of the prompt 
        if hasattr(self, 'popup_window'):
            self.popup_window.destroy()
            
        # Reset the app to default settings
        self.root_app.background.destroy()
        self.root_app.__init__()
        
        # Refresh the menu
        self._draw_menu()
                   
        # Redraw Background
        self.root_app.background = Frame(self.root_app.window,
                                width=self.root_app.window_width,
                                height=self.root_app.window_height)
        self.root_app.background.pack()
                
        # Create Load Screen Buttons
        self.root_app.new_button = Button(self.root_app.background, text="New Blank Project", 
                            width = 20,
                            height=3, 
                            command=self._new)
        self.root_app.new_button.grid(row=0, column=0, sticky='n', pady=2 )

        self.root_app.new_wiz_button = Button(self.root_app.background, 
                                     text="New Project Wizard", 
                                     width = 20,
                                     height=3, 
                                     command=self._new_project_wizard)
        self.root_app.new_wiz_button.grid(row=1, column=0, sticky='n', pady=2 )

        self.root_app.load_button = Button(self.root_app.background, text="Load Project", 
                            width=20,
                            height=3, 
                            command=self._open)
        self.root_app.load_button.grid(row=2, column=0, sticky='n', pady=2)

        self.root_app.quit_button = Button(self.root_app.background, text="Quit", 
                            width=20, 
                            height=3, 
                            command=self._quit)
        self.root_app.quit_button.grid(row=3, column=0, sticky='n', pady=2)

    def _quit(self):
        '''
        Quit the application.
        
        Returns
        -------
        None.

        '''    
        
        # If the project is not saved, prompt if it should be saved
        if not self.root_app.saved:
            
            # Popup window to prompt if the project should be saved
            popup_window = tk.Toplevel()
            popup_window.geometry("300x100") 
            popup_window.wm_title("Save Work?")
            
            # Background of the popup window
            bkgd_frame = Frame(popup_window, width=300, height=100)
            bkgd_frame.pack()
            
            # Label that displays the prompt
            prompt_txt = "Quit without saving?"
            prompt = Label(bkgd_frame, text=prompt_txt)
            prompt.grid(row=0, column=0, columnspan=3, sticky='nsew')
            
            # Buttons to save and quit, just quit, and cancel the "quit" 
            # command
            yes_button = Button(bkgd_frame, text="Save", command=self._save)
            yes_button.grid(row=1, column=0)
            no_button = Button(bkgd_frame, text="Quit", 
                               command=self.root_app.window.destroy)
            no_button.grid(row=1, column=1)           
            cancel_button = Button(bkgd_frame, text="Cancel", 
                                   command=popup_window.destroy)
            cancel_button.grid(row=1, column=2)            
        
        # The project is already saved, so just quit the entire app
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
    
        # Prompt where the csv file should be saved
        file_name = asksaveasfilename(filetypes=(("CSV files","*.csv"),),
                                                initialdir = "/",
                                                title = "Select file")
        
        # If no filename was given, don't export the project to CSV
        if not file_name:  
            return
        
        # Add .csv to the end of the filename when saving
        else:
            file_name = file_name + '.csv'
        
        # Save every box as a new line to the csv file
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

    def draw_about_box(self):
        '''
        Creates a popup Window that displays basic information about 
        OpenAnnotation

        Returns
        -------
        None.

        '''
        
        # Open a popup window
        self.about_window = tk.Toplevel()
        self.about_window.title("About Open Annotation")  # to define the title
        self.about_window.geometry("400x200")
        
        # Draw the canvas for the text
        canvas = Canvas(self.about_window, 
                        bg='white',
                        width=400, 
                        height=200)
        
        # Read a file that contains the information for the about window
        f = open('data/about.txt', 'r')
        lines = f.readlines()
        f.close()
        
        # Draw that information onto the popup window
        for i, line in enumerate(lines):
            canvas.create_text(200, (i+1)*11 , 
                               font=('Arial', 10),
                               text=line)
        canvas.pack()            

    def _new_project_wizard(self):
        self._new()
        ProjectWizard(self)
      
class Annotation(object):
    
    def __init__(self, filename):
        '''
        The Annotation object contains all of the relevant information for a
        single annotation.
        
        Parameters
        ----------
        filename : STRING
            Contains the path and filename of the image that will be annotated
        
        Returns
        -------
        None.
    
        '''  
        self.filename = filename
        self.bbox = []
        self.label = []
        self.rotation = -1
    
    def add_label(self, top, left, bottom, right, label):
        '''
        The Annotation object contains all of the relevant information for a
        single annotation.
        
        Parameters
        ----------
        top : NUMERIC
            Top-most y-coordinate (y0) for the bounding box
        left : NUMERIC
            Left-most x-coordinate (x0) for the bounding box
        bottom : NUMERIC
            Bottom-most y-coordinate (y1) for the bounding box
        right : NUMERIC
            Right-most x-coordinate (x1) for the bounding box
        label : STRING
            The truth label for the corresponding bounding box
        Returns
        -------
        None.
    
        '''              
        self.bbox.append([top, left, bottom, right, label])
        self.label.append(label)
        