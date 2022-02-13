# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 16:29:52 2022

@author: vedhs
"""
import numpy as np

points=['Left Eyebrow Left','Left Eyebrow Center','Left Eyebrow Right','Right Eyebrow Left','Right Eyebrow Center','Right Eyebrow Right','Left Eye Left','Left Eye Top','Left Eye Pupil','Left Eye Bottom','Left Eye Right','Right Eye Left','Right Eye Top','Right Eye Pupil','Right Eye Bottom','Right Eye Right','Nose Top','Nose Tip','Mouth Left Tip','Mouth Left Center','Mouth Center','Mouth Right Center','Mouth Right Tip','Chin']

class data:
    img=None
    location=np.zeros((len(points)))
    
if __name__ == '__main__':
    d = data()
    print(d.location.shape)
    