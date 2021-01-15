# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 08:01:15 2021

@author: Ronald Kemker
"""

import tkinter as tk
from PIL import ImageTk, Image

class InteractiveBox(object):
    
    def __init__(self, left, top, right, bottom, color, width=5):
        
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.color = color
        
        self.close_button_size = 20
        self.width = width
                
    def draw_box(self, root_app, box_id):
        
        self.root_app = root_app
        canvas = root_app.canvas
        self.image_id = root_app.current_file
        self.box_id = box_id
        
        canvas.create_rectangle(self.left,
                                self.top,
                                self.right,
                                self.bottom,
                                outline=self.color,
                                width=self.width)
        
        close_window_img = Image.open('img/close_window.jpg')
        close_window_img = close_window_img.crop((100,100,720,720))

        sz = self.close_button_size

        photo = ImageTk.PhotoImage(close_window_img.resize((sz,sz), 
                                              Image.ANTIALIAS))        
        
        button = tk.Button(canvas, 
                        width = self.close_button_size, 
                        height = self.close_button_size,
                        image=photo, 
                        command=lambda box_id=box_id: self.delete_box(box_id),
                        relief='flat',
                        bg=None)
        button.image = photo
        
        button.place(x = self.right - self.close_button_size - 2*self.width,
                     y = self.top+self.width)

    def delete_box(self, box_id):
        self.root_app.annotations[self.image_id].bbox.pop(box_id)
        self.root_app.annotations[self.image_id].label.pop(box_id)
        self.root_app._draw_workspace()        
        
if __name__ == "__main__":
    
    window = tk.Tk()
    window.geometry("200x200") 
        
    canvas = tk.Canvas(window, width = 198, height=198)
    canvas.pack()
    
    left = 10
    right= 110
    top = 10
    bottom = 120
    color = 'Blue'
    
    box = InteractiveBox(left, top, right, bottom, color)
    box.draw_box(canvas)
    
    window.mainloop()
