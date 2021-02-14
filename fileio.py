# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 13:25:14 2021

@author: Ronald Kemker
"""

import struct

def int_to_bytearray(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def bytearray_to_int(x):
    return int.from_bytes(x, 'big')

def bytearray_to_float(x):
    return float(struct.unpack("f", x)[0])

def float_to_bytearray(x):
    return struct.pack('f', x)

def string_to_bytearray(x):
    return str.encode(x)

def bytearray_to_string(x):
    return x.decode()    

class ROI(object):
    
    def __init__(self):
        '''
        A single Region of Interest (ROI).  A ROI with two points is a bounding
        box that has all edges parallel to the X-Y axes.  A ROI with three or
        more points is a multi-sided polygon.
                
        Parameters
        ----------
        None
    
        Attributes
        ----------
        points : list
            These are the coordinates for a single ROI.
            
        Raises
        ------
        None
    
        Returns
        -------
        None
        '''  
        
        self.points = []
    
    def push(self, x, y):
        '''
        Add a list that contains the [x,y] pair into the list of ROI
        coordinates.
        
        Parameters
        ----------
        x : FLOAT32
            x-coordinate
        y : FLOAT32
            y-cooridnate

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
        self.points.append([x, y])
    
    def size(self):
        '''
        Returns the number of cooridnate pairs in a ROI
        
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
        size : INT
            Number of coordinate pairs in the ROI
    
        '''   
        return len(self.points)
    
    def getBox(self):
        '''
        Helper function to assist with the InteractiveBox object.  
        TODO: Integrate InteractiveBox with this Annotation object

        Parameters
        ----------
        None
        
        Attributes
        ----------
        None        
        
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
        hex_list : list
            Contains a list of bytearrays that describes the entire ROI object

        '''

        # Separate different elements
        newline_byte = string_to_bytearray('\n')

        hex_list = [self.size().to_bytes(2, 'big'), newline_byte]
        
        for point in self.points:
            hex_list += [float_to_bytearray(point[0]), newline_byte]
            hex_list += [float_to_bytearray(point[1]), newline_byte]
        
        return hex_list

class Annotation(object):
    
    def __init__(self):
        '''
        The Annotation object contains all of the relevant information for a
        single annotation.
        
        Parameters
        ----------
        None

        Attributes
        ----------
        roi : list
            Empty list that will contain ROI objects
            
        label : list
            Empty list that will contain integers that correspond to object
            classes
            
        rotation : integer
            Indicates how the image needs to be rotated to be upright

        Raises
        ------
        None   
        
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
        roi : ROI object
            Contains the ROI object that describes an annotation
        label : int
            The truth label for each corresponding ROI

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
        self.roi.append(roi)
        self.label.append(label)
        
    def pop(self, index=0):
        '''
        Deletes a ROI from the annotation
        
        Parameters
        ----------
        index : INT (default=0)
            The index of the ROI to be deleted
       
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
        self.roi.pop(index)
        self.label.pop(index)

    def size(self):
        '''
       Number of ROIs in an image

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
        hex_list : list
            A list of bytearray objects that describes the annotation object
        '''
        # Separate different elements
        newline_byte = string_to_bytearray('\n')
        
        hex_list = [int_to_bytearray(self.size()), newline_byte]
        hex_list += [int_to_bytearray(self.rotation), newline_byte]

        for i, roi in enumerate(self.roi):
            hex_list += roi.to_bytes()
            hex_list += [self.label[i].to_bytes(2, 'big'), newline_byte]
        
        return hex_list
       
    
def SaveOAF(filename, annotations, file_list, class_list, colorspace, 
            current_file, version=1, testing=False):
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
    testing : BOOLEAN (Default is False)
        This is used for testing purposes only.
        
    Raises
    ------
    None           

    Returns
    -------
    hex_list : list
        The hex_list is returned for unittesting only
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
    if testing:
        return hex_list
    else:
        with open(filename, 'wb') as f:
            for h in hex_list:
                f.write(h)


def LoadOAF(filename, bytes_list=None):       
    '''
    Load .OAF file 
    
    Open Annotation Format (.oaf) File Extension.  See save OAF for format.       
    
    Parameters
    ----------
    filename : STRING
        File path/name to save the OpenAnnotation File
    bytes_list : List of bytearrays
        This is a bytearray of an entire OpenAnnotation Formatted project that
        is used only for unittesting.

    Raises
    ------
    None  

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
    if not bytes_list:
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