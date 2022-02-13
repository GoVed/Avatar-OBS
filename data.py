# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 16:29:52 2022

@author: vedhs
"""

#Imports
import numpy as np
from PIL import Image
from os import walk

#The points which are used for the data
points=['Left Eyebrow Left','Left Eyebrow Center','Left Eyebrow Right','Right Eyebrow Left','Right Eyebrow Center','Right Eyebrow Right','Left Eye Left','Left Eye Top','Left Eye Pupil','Left Eye Bottom','Left Eye Right','Right Eye Left','Right Eye Top','Right Eye Pupil','Right Eye Bottom','Right Eye Right','Nose Top','Nose Tip','Mouth Left Tip','Upper Lip Left Center','Upper Lip Center','Upper Lip Right Center','Mouth Right Tip','Lower Lip Left Center','Lower Lip Center','Lower Lip Right Center','Chin']


#data class which makes the raw format of the data
class data:
    img=None
    location=np.zeros((len(points),2),dtype=np.uint32)
    
    def save(self,path='Data/raw/'):
        #getting new id
        gid=0
                
        filenames=next(walk(path), (None, None, []))[2]
        if len(filenames)>0:
            filename=filenames[-1]        
            gid=int(filename[0:filename.index('.')])+1
            
        
        #Save with id
        im = Image.fromarray(self.img)
        im.save(path+str(gid)+".jpeg")
        np.save(path+str(gid)+".npy",self.location)
        
    
    
#Main class to test    
if __name__ == '__main__':
    d = data()
    print(d.location)
    