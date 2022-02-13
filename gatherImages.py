# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 16:28:38 2022

@author: vedhs
"""

import tkinter as tk
import data
import cv2
from PIL import Image, ImageTk


class interactive_tool:
    
    win = None
    width = None
    height = None
    cap = None
    lmain = None
    
    def __init__(self):
        self.win = tk.Tk()
        
        self.width, self.height = 800, 600
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    def show_frame(self):
        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_frame)
    
    
    def start():
        pass
    
    def run(self):
        self.win.bind('<Escape>', lambda e: self.win.quit())
        self.lmain = tk.Label(self.win)
        self.lmain.pack()
        
        start_button = tk.Button(self.win,text = "Start",command = self.start)
        start_button.pack()
        
        self.show_frame()
        
        self.win.mainloop()
        self.close()
        
    def close(self):
        self.cap.release()
        
if __name__ == '__main__':
    tool = interactive_tool()
    tool.run()
