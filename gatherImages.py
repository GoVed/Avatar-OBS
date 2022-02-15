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
      self.width, self.height = 640, 360
      
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
    
    #Counter to check which position is being set
    poscounter=0
    
    #Constructor
    def __init__(self,ip=''):
        #Making tkinter window
        self.win = tk.Tk()
        
        #Video capture
        self.cap = VideoCapture(ip)
        
        #Init for UI elements to show on tk window
        self.UIe = {}
        
        self.px,self.py=0,0

    #To capture live from camera and show on the UI 
    def show_frame(self):
        
        #Check if image needs to be updated
        if self.update_image:
            
            #Read image from camera
            frame = self.cap.read()
            
            
            #Flip the image
            frame = cv2.flip(frame, 1)
            
            #Color format change
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            #Save latest image
            self.np_img = np.array(cv2image)
            
            #Generating image object to show
            img = Image.fromarray(cv2image)        
            imgtk = ImageTk.PhotoImage(image=img)
            
            #Setting image to the UI element
            self.UIe['lmain'].imgtk = imgtk
            self.UIe['lmain'].configure(image=imgtk)
        else:
            tempimg = np.copy(self.np_img)
            
            for i in range(0,self.poscounter):                
                tempimg[self.tempdata.location[i,0],self.tempdata.location[i,1],:]=[255,0,0]
                               
                
            #Generating image object to show
            img = Image.fromarray(tempimg)        
            imgtk = ImageTk.PhotoImage(image=img)
            
            #Setting image to the UI element
            self.UIe['lmain'].imgtk = imgtk
            self.UIe['lmain'].configure(image=imgtk)
        
        #Show the mouse coordinates on the status
        self.statusstr = 'X:'+str(self.px)+'\tY:'+str(self.py)+'\t'
        
        #Show what's being set
        if self.update_image:
            self.statusstr += 'Pause the frame to start setting the position'
        else:        
            self.statusstr += 'Setting:'+data.points[self.poscounter]
        
        
        #Update the status variable
        self.status.set(self.statusstr)
        
        #Update next frame on UI at 30FPS
        self.UIe['lmain'].after(1000//30, self.show_frame)
           
    #To stop live video and track mouse pointer for click positions
    def start_gathering(self):
        
        #Invert update image flag
        self.update_image = not self.update_image
        
        #Check the update image state
        if self.update_image:
            #Update the button text
            self.UIe['start_button'].configure(text = "Pause frame and set posittions to save")            
        else:            
            #Update the button text
            self.UIe['start_button'].configure(text = "Discard frame and continue live video")
            #Create new data object
            self.tempdata=data.data()
            self.tempdata.img=self.np_img
     
    #On mouse move
    def motion(self,event):
        #set mouse x and y; -2 because of window position
        self.px, self.py = event.x-2, event.y-2
     
    #On mouse click
    def mouse_clicked(self,event): 
        
        #If frame is paused
        if not self.update_image:
            
            #Set the position and increase the counter
            self.tempdata.location[self.poscounter,1]=self.px
            self.tempdata.location[self.poscounter,0]=self.py
            self.poscounter+=1
            
            #Check if every position is counter
            if self.poscounter >= len(data.points):
                self.tempdata.save()
                self.reset_data()
        
    #On reset
    def reset_data(self,event=None):         
        self.poscounter=0
        self.update_image = True
        del self.tempdata
        self.UIe['start_button'].configure(text = "Pause frame and set positions to save")
        
    #On reset
    def undo(self,event=None):         
        self.poscounter=max(0,self.poscounter-1)
        
        
            
        
    #Main run for tk UI
    def run(self):
        
        #UI for showing image
        self.win.bind('<Escape>', lambda e: self.win.quit())
        self.UIe['lmain'] = tk.Label(self.win)
        self.UIe['lmain'].pack()
        
        
        #UI button to show start button
        self.UIe['start_button'] = tk.Button(self.win,text = "Pause frame and set posittions to save",command = self.start_gathering)
        self.UIe['start_button'].pack()
        
        #Label to show status
        self.status = tk.StringVar()
        self.UIe['status'] = tk.Label(self.win,textvariable= self.status)
        self.UIe['status'].pack()
        self.status.set("Pause the frame to start positioning")
        
        self.show_frame()
        self.win.bind('<Motion>', self.motion)
        self.win.bind("<Button-1>", self.mouse_clicked)
        self.win.bind("<Button-3>", self.undo)
        self.win.mainloop()
        self.close()
        
    #Custom destructor method
    def close(self):
        
        #Release camera device
        self.cap.release()
        

if __name__ == '__main__':
    tool = interactive_tool('http://192.168.137.183:16500/video')
    tool.run()
