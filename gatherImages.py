# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 16:28:38 2022

@author: vedhs
"""

#Imports
import tkinter as tk
import numpy as np
import data
import cv2
from PIL import Image, ImageTk
import queue, threading

# bufferless VideoCapture
class VideoCapture:

    def __init__(self, ip):
      #Setting width and height for the camera
      self.width, self.height = 1280, 720
      
      #Setting the device
      if ip!='':
          self.cap = cv2.VideoCapture(ip)            
      else:
          self.cap = cv2.VideoCapture(0)
      self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
      self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)      
      
      self.q = queue.Queue()
      t = threading.Thread(target=self._reader)
      t.daemon = True
      t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()   # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)
    
    def read(self):
        return self.q.get()
    
    def release(self):
        self.cap.release()

#Interactive tool to gather data easily using GUI
class interactive_tool:

    #To save image
    np_img = None
    
    #Flag to update image
    update_image=True
    
    #Constructor
    def __init__(self,ip=''):
        #Making tkinter window
        self.win = tk.Tk()
        
        #Video capture
        self.cap = VideoCapture(ip)
        
        #Init for UI elements to show on tk window
        self.UIe = {}

    #To capture live from camera and show on the UI 
    def show_frame(self):
        
        #Check if image needs to be updated
        if self.update_image:
            
            #Read image from camera
            frame = self.cap.read()
            
            
            #Flip the image
            frame = cv2.flip(frame, 1)
            
            #Color format change
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            
            #Save latest image
            self.np_img = np.array(cv2image)
            
            #Generating image object to show
            img = Image.fromarray(cv2image)        
            imgtk = ImageTk.PhotoImage(image=img)
            
            #Setting image to the UI element
            self.UIe['lmain'].imgtk = imgtk
            self.UIe['lmain'].configure(image=imgtk)
            
        self.UIe['lmain'].after(1000//30, self.show_frame)
    
    #To stop live video and track mouse pointer for click positions
    def start_gathering(self):
        self.update_image = not self.update_image
        if self.update_image:
            self.UIe['start_button'].configure(text = "Pause frame and set posittions to save")
        else:            
            self.UIe['start_button'].configure(text = "Discard frame and continue live video")
        
    
    #Main run for tk UI
    def run(self):
        
        #UI for showing image
        self.win.bind('<Escape>', lambda e: self.win.quit())
        self.UIe['lmain'] = tk.Label(self.win)
        self.UIe['lmain'].pack()
        
        
        #UI button to show start button
        self.UIe['start_button'] = tk.Button(self.win,text = "Pause frame and set posittions to save",command = self.start_gathering)
        self.UIe['start_button'].pack()
        
        
        self.show_frame()
        
        self.win.mainloop()
        self.close()
        
    #Custom destructor method
    def close(self):
        
        #Release camera device
        self.cap.release()
        

if __name__ == '__main__':
    tool = interactive_tool('http://192.168.137.183:16500/video')
    tool.run()
