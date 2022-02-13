# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 16:29:52 2022

@author: vedhs
"""

#Imports
import numpy as np


#The points which are used for the data
points=['Left Eyebrow Left','Left Eyebrow Center','Left Eyebrow Right','Right Eyebrow Left','Right Eyebrow Center','Right Eyebrow Right','Left Eye Left','Left Eye Top','Left Eye Pupil','Left Eye Bottom','Left Eye Right','Right Eye Left','Right Eye Top','Right Eye Pupil','Right Eye Bottom','Right Eye Right','Nose Top','Nose Tip','Mouth Left Tip','Mouth Left Center','Mouth Center','Mouth Right Center','Mouth Right Tip','Chin']


#data class which makes the raw format of the data
class data:
    img=None
    location=np.zeros((len(points)))
    
    
#Main class to test    
if __name__ == '__main__':
    d = data()
    print(d.location.shape)
    