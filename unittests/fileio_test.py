# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 16:25:00 2021

@author: Ronald Kemker
"""

import unittest
from fileio import int_to_bytearray, bytearray_to_int, float_to_bytearray,\
                   bytearray_to_float, string_to_bytearray,\
                   bytearray_to_string, ROI, Annotation, LoadOAF, SaveOAF


class TestFileIO(unittest.TestCase):
    
    def test_int_bytearray_conversion(self):
                
        for i in range(2**16):
            bytes_i = int_to_bytearray(i)
            int_i = bytearray_to_int(bytes_i)
            self.assertEqual(i, int_i)
        
        
    def test_float_bytearray_conversion(self):
        
        for i in range(2**16):
            bytes_i = float_to_bytearray(float(i))
            float_i = bytearray_to_float(bytes_i)
            self.assertEqual(float(i), float_i)
    
    def test_string_bytearray_conversion(self):
        
        test_string = 'C:/Documents/filename0.jpg'
        byte_i = string_to_bytearray(test_string)
        string_i = bytearray_to_string(byte_i)
        self.assertEqual(test_string, string_i)
    
    def test_ROI(self):
        roi = ROI()
        self.assertTrue(hasattr(roi, 'points'))
        self.assertEqual(roi.size(), 0)        
        roi.push(10, 11)
        self.assertEqual(roi.size(), 1)
        roi.push(100, 101)
        self.assertEqual(roi.size(), 2)
        left, top, right, bottom = roi.getBox()
        self.assertEqual(left, 10)
        self.assertEqual(top, 11)
        self.assertEqual(right, 100)
        self.assertEqual(bottom, 101)
        roi.push(50, 51)
        self.assertEqual(roi.size(), 3)
        self.assertRaises(ValueError, roi.getBox)
        bytes_arr = roi.to_bytes()
        self.assertListEqual(bytes_arr, [b'\x00\x03', b'\n', b'\x00\x00 A', 
                                         b'\n', b'\x00\x000A', b'\n', 
                                         b'\x00\x00\xc8B', b'\n', 
                                         b'\x00\x00\xcaB', b'\n',
                                         b'\x00\x00HB', b'\n', b'\x00\x00LB', 
                                         b'\n'])    
        
    def test_Annotation(self):

        a = Annotation()
        self.assertTrue(hasattr(a, 'roi'))
        self.assertEqual(len(a.roi), 0)
        self.assertTrue(hasattr(a, 'label'))
        self.assertEqual(len(a.label), 0)
        self.assertTrue(hasattr(a, 'rotation'))
        
        a.rotation = 3
        self.assertEqual(a.rotation, 3)
        for p in range(5):
            roi = ROI()
            roi.push(0,1)
            roi.push(50.0,51.0)
            roi.push(100,101.0)
            a.push(roi, p%3)
        
        bytes_arr = a.to_bytes()        
        self.assertListEqual(bytes_arr, [b'\x05', b'\n', b'\x03', b'\n', 
                                         b'\x00\x03', b'\n', 
                                         b'\x00\x00\x00\x00', b'\n', 
                                         b'\x00\x00\x80?', b'\n', 
                                         b'\x00\x00HB', b'\n', b'\x00\x00LB', 
                                         b'\n', b'\x00\x00\xc8B', b'\n', 
                                         b'\x00\x00\xcaB', b'\n', b'\x00\x00', 
                                         b'\n', b'\x00\x03', b'\n', 
                                         b'\x00\x00\x00\x00', b'\n', 
                                         b'\x00\x00\x80?', b'\n', 
                                         b'\x00\x00HB', b'\n', b'\x00\x00LB', 
                                         b'\n', b'\x00\x00\xc8B', b'\n', 
                                         b'\x00\x00\xcaB', b'\n', b'\x00\x01', 
                                         b'\n', b'\x00\x03', b'\n', 
                                         b'\x00\x00\x00\x00', b'\n', 
                                         b'\x00\x00\x80?', b'\n', 
                                         b'\x00\x00HB', b'\n', b'\x00\x00LB', 
                                         b'\n', b'\x00\x00\xc8B', b'\n', 
                                         b'\x00\x00\xcaB', b'\n', b'\x00\x02', 
                                         b'\n', b'\x00\x03', b'\n', 
                                         b'\x00\x00\x00\x00', b'\n', 
                                         b'\x00\x00\x80?', b'\n', 
                                         b'\x00\x00HB', b'\n', b'\x00\x00LB', 
                                         b'\n', b'\x00\x00\xc8B', b'\n', 
                                         b'\x00\x00\xcaB', b'\n', b'\x00\x00', 
                                         b'\n', b'\x00\x03', b'\n', 
                                         b'\x00\x00\x00\x00', b'\n', 
                                         b'\x00\x00\x80?', b'\n', 
                                         b'\x00\x00HB', b'\n', b'\x00\x00LB', 
                                         b'\n', b'\x00\x00\xc8B', b'\n', 
                                         b'\x00\x00\xcaB', b'\n', b'\x00\x01', 
                                         b'\n'])
        
        
        for i in range(5):
            self.assertEqual(len(a.roi[0].points) , 3)
            self.assertEqual(a.label[0], i%3)
            a.pop()
            self.assertEqual(len(a.roi), 4-i)
            self.assertEqual(len(a.label), 4-i)
               
    def test_SaveOAF(self):
        annotations = []
        file_list = []
        class_list = ['winston', 'prince', 'duckie']
        colorspace = ['#0000FF', '#FF0000', '#00FF00']
        current_file = 4
        filename = 'tempfile.oaf'
        
        for i in range(5):
            a = Annotation()
            a.rotation = 3
            file_list.append('file%d.jpg' % i)
            for p in range(3):
                roi = ROI()
                roi.push(0,1)
                roi.push(50.0,51.0)
                roi.push(100,101.0)
                a.push(roi, p%3)
            annotations.append(a)
    
        byte_arr = SaveOAF(filename, annotations, file_list, class_list, 
                           colorspace, current_file, testing=True)  
        
        byte_arr_copy = []
        while len(byte_arr):
            byte_arr_copy.append(byte_arr.pop(0) + byte_arr.pop(0))
        byte_arr = byte_arr_copy
        del byte_arr_copy
        
        
        byte_truth = [b'\x01\n',b'\x04\n',b'\x05\n',b'file0.jpg\n', b'\x03\n',
                      b'\x03\n',b'\x00\x03\n', b'\x00\x00\x00\x00\n',
                     b'\x00\x00\x80?\n',b'\x00\x00HB\n',b'\x00\x00LB\n',
                     b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',b'\x00\x00\n',
                     b'\x00\x03\n',b'\x00\x00\x00\x00\n',b'\x00\x00\x80?\n',
                     b'\x00\x00HB\n',b'\x00\x00LB\n',b'\x00\x00\xc8B\n',
                     b'\x00\x00\xcaB\n',b'\x00\x01\n',b'\x00\x03\n',
                     b'\x00\x00\x00\x00\n',b'\x00\x00\x80?\n',b'\x00\x00HB\n',
                     b'\x00\x00LB\n',b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',
                     b'\x00\x02\n',b'file1.jpg\n',b'\x03\n',b'\x03\n',
                     b'\x00\x03\n', b'\x00\x00\x00\x00\n',b'\x00\x00\x80?\n',
                     b'\x00\x00HB\n', b'\x00\x00LB\n',b'\x00\x00\xc8B\n',
                     b'\x00\x00\xcaB\n',b'\x00\x00\n',b'\x00\x03\n',
                     b'\x00\x00\x00\x00\n',b'\x00\x00\x80?\n',b'\x00\x00HB\n',
                     b'\x00\x00LB\n',b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',
                     b'\x00\x01\n',b'\x00\x03\n',b'\x00\x00\x00\x00\n',
                     b'\x00\x00\x80?\n',b'\x00\x00HB\n',b'\x00\x00LB\n',
                     b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',b'\x00\x02\n',
                     b'file2.jpg\n',b'\x03\n',b'\x03\n',b'\x00\x03\n',
                     b'\x00\x00\x00\x00\n',b'\x00\x00\x80?\n',b'\x00\x00HB\n',
                     b'\x00\x00LB\n',b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',
                     b'\x00\x00\n',b'\x00\x03\n',b'\x00\x00\x00\x00\n',
                     b'\x00\x00\x80?\n',b'\x00\x00HB\n',b'\x00\x00LB\n',
                     b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',b'\x00\x01\n',
                     b'\x00\x03\n',b'\x00\x00\x00\x00\n',b'\x00\x00\x80?\n',
                     b'\x00\x00HB\n',b'\x00\x00LB\n',b'\x00\x00\xc8B\n',
                     b'\x00\x00\xcaB\n',b'\x00\x02\n',b'file3.jpg\n',
                     b'\x03\n',b'\x03\n',b'\x00\x03\n',b'\x00\x00\x00\x00\n',
                     b'\x00\x00\x80?\n',b'\x00\x00HB\n',b'\x00\x00LB\n',
                     b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',
                     b'\x00\x00\n',b'\x00\x03\n',b'\x00\x00\x00\x00\n',
                     b'\x00\x00\x80?\n',b'\x00\x00HB\n',
                     b'\x00\x00LB\n',b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',
                     b'\x00\x01\n',b'\x00\x03\n',b'\x00\x00\x00\x00\n',
                     b'\x00\x00\x80?\n',b'\x00\x00HB\n',b'\x00\x00LB\n',
                     b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',b'\x00\x02\n',
                     b'file4.jpg\n',b'\x03\n',b'\x03\n',b'\x00\x03\n',
                     b'\x00\x00\x00\x00\n',b'\x00\x00\x80?\n',b'\x00\x00HB\n',
                     b'\x00\x00LB\n',b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',
                     b'\x00\x00\n',b'\x00\x03\n',b'\x00\x00\x00\x00\n',
                     b'\x00\x00\x80?\n',b'\x00\x00HB\n',b'\x00\x00LB\n',
                     b'\x00\x00\xc8B\n',b'\x00\x00\xcaB\n',b'\x00\x01\n',
                     b'\x00\x03\n',b'\x00\x00\x00\x00\n',b'\x00\x00\x80?\n',
                     b'\x00\x00HB\n',b'\x00\x00LB\n',b'\x00\x00\xc8B\n',
                     b'\x00\x00\xcaB\n',b'\x00\x02\n',b'\x03\n',b'winston\n',
                     b'#0000FF\n',b'prince\n',b'#FF0000\n',b'duckie\n',
                     b'#00FF00\n']

            
        self.assertListEqual(byte_arr, byte_truth)
               
        annotations0, file_list0, class_list0, colorspace0, current_file0 =\
        LoadOAF(filename, byte_truth)
        
        self.assertListEqual(file_list, file_list0)
        self.assertListEqual(class_list, class_list0)
        self.assertListEqual(colorspace, colorspace0)
        self.assertEqual(current_file, current_file0)
                
    
if __name__ == '__main__':
    unittest.main()