# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 16:28:38 2022

@author: vedhs
"""

import tkinter as tk
import data
import cv2
from PIL import Image, ImageTk





def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)


def start():
    pass

win = tk.Tk()

width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


win.bind('<Escape>', lambda e: win.quit())
lmain = tk.Label(win)
lmain.pack()

start_button = tk.Button(win,text = "Start",command = start)
start_button.pack()

show_frame()

win.mainloop()
cap.release()
