# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 21:35:05 2022

@author: vedhs
"""

from tensorflow import keras
from os import walk
from PIL import Image
import numpy as np

def getData():
    x=[]
    y=[]
    path='Data/raw/'
    files=next(walk(path), (None, None, []))[2]
    ids=len(files)//2
    for i in range(ids):
        x.append(np.asarray(Image.open(path+str(i)+'.jpeg')))
        y.append(np.load(path+str(i)+'.npy').flatten())
        
    x=np.array(x)
    y=np.array(y)
    return x,y

def genModel(output_classes):
    model = keras.models.Sequential()
    model.add(keras.layers.Conv2D(32, (2,2), padding='same',input_shape=(360,640,3)))
    model.add(keras.layers.LeakyReLU(alpha=0.2))
    model.add(keras.layers.BatchNormalization(momentum=0.15, axis=-1))
        
    model.add(keras.layers.MaxPooling2D(pool_size=(3, 3)))
    model.add(keras.layers.Dropout(0.20))
    
    model.add(keras.layers.Conv2D(64, (2,2), padding='same'))
    model.add(keras.layers.LeakyReLU(alpha=0.2))
    model.add(keras.layers.BatchNormalization(momentum=0.15, axis=-1))
    
    model.add(keras.layers.MaxPooling2D(pool_size=(3, 3)))
    model.add(keras.layers.Dropout(0.20))
    
    model.add(keras.layers.Conv2D(128, (2,2), padding='same'))
    model.add(keras.layers.LeakyReLU(alpha=0.2))
    model.add(keras.layers.BatchNormalization(momentum=0.15, axis=-1))
    
    model.add(keras.layers.MaxPooling2D(pool_size=(3, 3)))
    model.add(keras.layers.Dropout(0.20))
    
    model.add(keras.layers.Flatten())

    model.add(keras.layers.Dense(128))
    model.add(keras.layers.Activation("relu"))
    
    model.add(keras.layers.Dense(output_classes))
    model.add(keras.layers.Activation("relu"))
    return model

x,y = getData()
model = genModel(y.shape[1])

model.compile(optimizer='nadam',loss='mean_squared_error')
model.fit(x,y,epochs=500,shuffle=True)

