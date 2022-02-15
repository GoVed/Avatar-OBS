# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 17:54:17 2022

@author: vedhs
"""


import cv2
import numpy as np
import data
import training


model_path='Data/models/model'
models=[]
i=0
for name in data.region_name:
    print(model_path+name+'.h5')
    temp=training.genModel(len(data.train_region[i])*2)
    temp.load_weights(model_path+name+'.h5')
    models.append(temp)
    i+=1
                  
def raw_predict(img):
    o=np.zeros((len(data.points),2))
    i=0
    for region in data.train_region:
        
        pred=models[i].predict(img)        
        pred=np.reshape(pred,(pred.shape[1]//2,2))
        o[region,:]=pred
        i+=1
    return o
    

def image(path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    img=cv2.imread(path)
    faces = face_cascade.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 4)
    o=None
    if len(faces)>0:
        f=faces[0]
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)[f[1]:f[1]+f[3],f[0]:f[0]+f[2],:]
        img = cv2.resize(img, (128,128), interpolation = cv2.INTER_AREA)
        o=raw_predict(np.array([img]))
        t=data.data()
        t.img=img
        
        o[o[:,0]>=128,0]=127
        o[o[:,1]>=128,1]=127
        t.location=np.array(o,dtype=np.int32)
        print(o)
        t.show()
        
        
        o/=[127/(f[3]-1),127/(f[2]-1)]
        o=np.add(o,[f[1],f[0]])        
        
    return o

def image_all(path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    img=cv2.imread(path)
    faces = face_cascade.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 4)
    o=None
    if len(faces)>0:
        f=faces[0]
        img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)[f[1]:f[1]+f[3],f[0]:f[0]+f[2],:]
        img = cv2.resize(img, (128,128), interpolation = cv2.INTER_AREA)
        model=training.genModel(27)
        model.load_weights('Data/models/modelAll.h5')
        o=model.predict(img)
        t=data.data()
        t.img=img
        
        o[o[:,0]>=128,0]=127
        o[o[:,1]>=128,1]=127
        t.location=np.array(o,dtype=np.int32)
        print(o)
        t.show()
        
        
        o/=[127/(f[3]-1),127/(f[2]-1)]
        o=np.add(o,[f[1],f[0]])        
        
    return o
pred=image_all('Data/raw/0.jpeg')
t=data.data()
t.img=cv2.cvtColor(cv2.imread('Data/raw/0.jpeg'), cv2.COLOR_BGR2RGB)
t.location=np.array(pred,dtype=np.int32)
t.show()