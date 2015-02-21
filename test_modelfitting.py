# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 19:00:42 2015

@author: ben
"""
import numpy as np
import model_fitting as mf

if __name__=="__main__":
    point = np.array([1,0,0])
    q = np.array([np.cos(np.pi/8),0,0,np.sin(np.pi/8)])
    state = np.hstack((np.zeros(3),q,np.zeros(6)))
    print(mf.com_from_point(state,point))