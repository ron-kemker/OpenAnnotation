# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 13:25:14 2021

@author: Ronald Kemker
"""

import struct

def int_to_bytearray(x):
    return x.to_bytes(2, 'big')

def bytearray_to_float(x):
    return float(struct.unpack("f", x)[0])

def bytearray_to_int(x):
    return int.from_bytes(x, 'big')

def string_to_bytearray(x):
    return str.encode(x)
  
class ROI(object):
    
    def __init__(self):
        '''
        A single Region of Interest (ROI).  A ROI with two points is a bounding
        box that has all edges parallel to the X-Y axes.  A ROI with three or
        more points is a multi-sided polygon.
                
        Returns
        -------
        None.
        '''        
        self.points = []
    
    def push(self, x, y):
        '''
        The Annotation object contains all of the relevant information for a
        single annotation.
        
        Parameters
        ----------
        x : FLOAT32
            x-coordinate
        y : FLOAT32
            y-cooridnate

        Returns
        -------
        None.
    
        '''   
        self.points.append([x, y])
    
    def size(self):
        '''
        Returns the number of cooridnate pairs in a ROI
        
        Parameters
        ----------
        None

        Returns
        -------
        size : INT
            Number of coordinate pairs in the ROI
    
        '''   
        return len(self.points)
    
    def getBox(self):
        '''
        Helper function to assist with the InteractiveBox object.  
        TODO: Integrate InteractiveBox with this Annotation object

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        left : float32
            x0 value
        top : float32
            y0 value
        right : float32
            x1 value
        bottom : float32
            y1 value

        '''
        if self.size() != 2:
            raise ValueError('This is not a box.')

        top = min(self.points[0][1], self.points[1][1])
        bottom = max(self.points[0][1], self.points[1][1])
        left = min(self.points[0][0], self.points[1][0])
        right = max(self.points[0][0], self.points[1][0])
        return left, top, right, bottom
        
    def to_bytes(self):
        '''
        Convert ROI to bytearray
        
        Format:
        Number of Points in ROI (int32)
        x0 (float32)
        y0 (float32)
        x1 (float32)
        y1 (float32)
        ...
        xN (float32)
        yN (float32)
        
        Returns
        -------
        None.

        '''

        # Separate different elements
        newline_byte = string_to_bytearray('\n')

        hex_list = [self.size().to_bytes(2, 'big'), newline_byte]
        
        for point in self.points:
            hex_list += [struct.pack('f', point[0]), newline_byte]
            hex_list += [struct.pack('f', point[1]), newline_byte]
        
        return hex_list

class Annotation(object):
    
    def __init__(self):
        '''
        The Annotation object contains all of the relevant information for a
        single annotation.
                
        Returns
        -------
        None.
    
        '''  
        self.roi = []
        self.label = []
        self.rotation = -1
    
    def push(self, roi, label):
        '''
        Add a ROI to the Annotation Object
        
        Parameters
        ----------
        roi : LIST of ROI Objects
            [(x0, y0), (x1, y1), ..., (xn, yn)]
        label : LIST of INTs
            The truth label for each corresponding ROI
        Returns
        -------
        None.
    
        '''              
        self.roi.append(roi)
        self.label.append(label)
        
    def pop(self, index):
        '''
        Deletes a ROI from the annotation
        
        Parameters
        ----------
        index : INT
            The index of the ROI to be deleted
            
        Returns
        -------
        None.
    
        '''  
        self.roi.pop(index)
        self.label.pop(index)

    def size(self):
        '''
       Number of ROIs in an image
        

        Returns
        -------
        size : INT
            The number of ROIs in the Annotation object
    
        '''         
        return len(self.roi)


    def to_bytes(self):
        '''
        Converts the Annotation to a bytearray.
        
        Format
        Number of ROIs (int32)
        Rotation (int32)
        ROI 0 (see above)
        label0 (int32)
        ROI 1
        label1
        ...
        ROI N
        label N        

        Returns
        -------
        None.

        '''
        # Separate different elements
        newline_byte = string_to_bytearray('\n')
        
        hex_list = [self.size().to_bytes(2, 'big'), newline_byte]
        hex_list += [int_to_bytearray(self.rotation), newline_byte]

        for i, roi in enumerate(self.roi):
            hex_list += roi.to_bytes()
            hex_list += [self.label[i].to_bytes(2, 'big'), newline_byte]
        
        return hex_list
       
    
def SaveOAF(filename, annotations, file_list, class_list, colorspace, 
            current_file, version=1):
    '''
    Custom savefile that will be robust to additional changes, i.e., that
    is backwards compatible to older versions.
    
    Open Annotation Format (.oaf) File Extension
    
    Format:
        Version (int)
        current file (int)
        
        Number of Files
        File 1 (string)
        Annotation 1 (obj)
        Filename 2 (string)
        Annotation 2 (obj)
        ...
        Size of Filename N (int)
        Annotation N (obj)
        
        Number of Classes (int)
        Class 1 Name (string)
        Color 1 Name (string)
        Class 2 Name (string)
        Color 2 Name (string)
        ...
        Class N Name (string)
        Color N Name (string)      
    
    Parameters
    ----------
    filename : STRING
        File path/name to save the OpenAnnotation File
    annotations : LIST OF ANNOTATION OBJECTS
        This is an ordered list of Annotation Objects.
    file_list  : LIST OF STRINGS
        This is the ordered list of images in the project.
    class_list : LIST OF STRINGS
        This is a list of object classes in this project.
    colorspace : LIST OF STRINGS
        This is a list of bounding box colors for each corresponding object
        class in class_list
    current_file : INT
        This is the file in the file_list we last left off on
    version : STRING (Default is 1)
        This will add a version control to the savefile for future
        backwards compatibility purposes

    Returns
    -------
    None.

    '''

    # Separate different elements
    newline_byte = string_to_bytearray('\n')

    # Store Version Number
    hex_list = [int_to_bytearray(version), newline_byte]

    # Current File
    hex_list += [int_to_bytearray(current_file), newline_byte]       
    
    # Number of Files
    num_files = len(file_list)
    hex_list += [int_to_bytearray(num_files), newline_byte]
    
    # Add all of the filenames and Annotation objects.
    for i in range(num_files):
        
        filename_byte = string_to_bytearray(file_list[i])
        hex_list += [filename_byte, newline_byte]
        hex_list += annotations[i].to_bytes()
    
    # Add all of the classes and corresponding ROI color schemes
    num_classes = len(class_list)
    hex_list += [int_to_bytearray(num_classes), newline_byte]
    for c in range(num_classes):
        classname_byte = string_to_bytearray(class_list[c])
        hex_list += [classname_byte, newline_byte]        
        colorname_byte = string_to_bytearray(colorspace[c])
        hex_list += [colorname_byte, newline_byte] 

    # Write .OAF file
    with open(filename, 'wb') as f:
        for h in hex_list:
            f.write(h)


def LoadOAF(filename):       
    '''
    Load .OAF file 
    
    Open Annotation Format (.oaf) File Extension.  See save OAF for format.       
    
    Parameters
    ----------
    filename : STRING
        File path/name to save the OpenAnnotation File

    version : STRING (Default is 1)
        This will add a version control to the savefile for future
        backwards compatibility purposes

    Returns
    -------
    annotations : LIST OF ANNOTATION OBJECTS
        This is an ordered list of Annotation Objects.
    file_list  : LIST OF STRINGS
        This is the ordered list of images in the project.
    class_list : LIST OF STRINGS
        This is a list of object classes in this project.
    colorspace : LIST OF STRINGS
        This is a list of bounding box colors for each corresponding object
        class in class_list
    current_file : INT
        This is the file in the file_list we last left off on.

    '''
    
    # Load all data from .OAF file
    with open(filename, 'rb') as f:
        bytes_list = f.readlines()
    
    # Grab .OAF format version (this will be used later for backwards 
    # compatability)
    version = bytearray_to_int(bytes_list.pop(0).split(b'\n')[0])
    
    # Load the last file open
    current_file = bytearray_to_int(bytes_list.pop(0).split(b'\n')[0])
    
    # Load all of the filenames and Annotation objects
    num_files = bytearray_to_int(bytes_list.pop(0).split(b'\n')[0])
    file_list = []
    annotations = []
    for i in range(num_files):
        file_list.append(bytes_list.pop(0).split(b'\n')[0].decode())
    
        num_rois = bytearray_to_int(bytes_list.pop(0).split(b'\n')[0])
        rotation = bytearray_to_int(bytes_list.pop(0).split(b'\n')[0])
        annotation = Annotation()
        annotation.rotation = rotation
        for r in range(num_rois):
            roi = ROI()
            num_pts = bytearray_to_int(bytes_list.pop(0).split(b'\n')[0])
            for p in range(num_pts):
                x = bytearray_to_float(bytes_list.pop(0).split(b'\n')[0])
                y = bytearray_to_float(bytes_list.pop(0).split(b'\n')[0])
                roi.push(x, y)
            
            label = bytearray_to_int(bytes_list.pop(0).split(b'\n')[0])
            annotation.push(roi, label)
        annotations.append(annotation)
    
    # Load all of the class names and corresponding ROI color schemes
    class_list = [] 
    colorspace = []
    num_classes = bytearray_to_int(bytes_list.pop(0).split(b'\n')[0])
    for i in range(num_classes):
        class_list.append(bytes_list.pop(0).split(b'\n')[0].decode())
        colorspace.append(bytes_list.pop(0).split(b'\n')[0].decode())
    
    
    return annotations, file_list, class_list, colorspace, current_file

if __name__ == '__main__':
    
    import random
    
    annotations = []
    file_list = []
    class_list = ['winston', 'prince', 'duckie']
    colorspace = ['blue', 'green', 'red']
    current_file = 4
    filename = 'tempfile.oaf'
    
    for i in range(5):
        a = Annotation()
        a.rotation = 3
        file_list.append('file%d.jpg' % i)
        for p in range(3):
            roi = ROI()
            roi.push(0,0)
            roi.push(100.0,100.0)
            a.push(roi, random.randint(0,2))
        annotations.append(a)

    SaveOAF(filename, annotations, file_list, class_list, colorspace, 
            current_file)
    
    annotations1, file_list1, class_list1, colorspace1, current_file1 =\
        LoadOAF(filename)
            