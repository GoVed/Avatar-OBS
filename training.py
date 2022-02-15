# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 21:35:05 2022

@author: vedhs
"""

from tensorflow import keras
from os import walk
import numpy as np
import data
import cv2

def getData(region):
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    x=[]
    y=[]
    path='Data/raw/'
    files=next(walk(path), (None, None, []))[2]
    ids=len(files)//2
    for i in range(ids):
        img=cv2.imread(path+str(i)+'.jpeg')
        
        faces = face_cascade.detectMultiScale(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 1.1, 4)
        if len(faces)>0:
            f=faces[0]
            img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)[f[1]:f[1]+f[3],f[0]:f[0]+f[2],:]
            img = cv2.resize(img, (128,128), interpolation = cv2.INTER_AREA)
            x.append(img)
            o=np.array(np.load(path+str(i)+'.npy')[region,:],dtype=np.float32)
            o=np.subtract(o,[f[1],f[0]])
            o[o[:,0]>=f[3],0]=f[3]-1
            o[o[:,1]>=f[2],1]=f[2]-1
            o*=[127/(f[3]-1),127/(f[2]-1)]
            y.append(o.flatten())
        
    x=np.array(x)
    y=np.array(y,dtype=np.float32)
    return x,y

def genModel(output_classes):
    model = keras.models.Sequential()
    model.add(keras.layers.Conv2D(8, (2,2), padding='same', kernel_initializer='random_normal',input_shape=(128,128,3)))
    model.add(keras.layers.LeakyReLU(alpha=0.3))
    model.add(keras.layers.BatchNormalization(momentum=0.15, axis=-1))
        
    model.add(keras.layers.MaxPooling2D(pool_size=(3, 3)))
    model.add(keras.layers.Dropout(0.20))
    
    model.add(keras.layers.Conv2D(16, (2,2),kernel_initializer='random_normal', padding='same'))
    model.add(keras.layers.LeakyReLU(alpha=0.3))
    model.add(keras.layers.BatchNormalization(momentum=0.15, axis=-1))
        
    
    model.add(keras.layers.MaxPooling2D(pool_size=(3, 3)))
    model.add(keras.layers.Dropout(0.20))
    
    model.add(keras.layers.Conv2D(128, (2,2),kernel_initializer='random_normal', padding='same'))
    model.add(keras.layers.LeakyReLU(alpha=0.3))
    model.add(keras.layers.BatchNormalization(momentum=0.15, axis=-1))
    
    
    model.add(keras.layers.MaxPooling2D(pool_size=(3, 3)))
    model.add(keras.layers.Dropout(0.20))
    
    model.add(keras.layers.Flatten())

    model.add(keras.layers.Dense(128,kernel_initializer='random_normal'))
    model.add(keras.layers.LeakyReLU(alpha=0.3))
    
    model.add(keras.layers.Dense(output_classes,kernel_initializer='random_normal'))
    model.add(keras.layers.LeakyReLU(alpha=0.3))
    return model


def posloss(y_true,y_pred):
    
    l=keras.backend.square(y_true-y_pred)
    l=keras.backend.reshape(l,(-1,l.shape[1]//2,2))
    l=keras.backend.sum(l,axis=2)
    l=keras.backend.sqrt(l)
    l=keras.backend.sum(l,axis=1)
    l=keras.backend.mean(l)
    return l
    
model=None
if __name__=='__main__':
    # i=0
    # for region in data.train_region:
    #     x,y = getData(region)
    #     model = genModel(y.shape[1])
    #     model.compile(optimizer='adam',loss=posloss)
    #     model.fit(x,y,batch_size=1,epochs=500,shuffle=True,workers=6)
    #     model.save('data/models/model_new_'+data.region_name[i]+'.h5')
    #     i+=1
    
    x,y = getData(np.arange(27))
    model = genModel(y.shape[1])
    model.compile(optimizer='adam',loss=posloss)
    model.fit(x,y,batch_size=1,epochs=500,shuffle=True)
    model.save('data/models/modelAll'+'.h5')


