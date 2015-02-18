# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 13:56:04 2015

@author: ben
"""
import numpy as np

class dynamicalSystem:
    
    def dynamics(t,x,u):
        raise NotImplementedError("subclasses of dynamicalSystem need to implement the dynamics function")
        
class rigidBodySystem:
    
    I = np.eye(3)
    m = 1
    point = np.array([0,0,0])
    
    def __init__(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)
            
    def dynamics(x,t,u=np.zeros(6)):
        if np.size(x) is 12:
            #do euler angle stuff
            vel = x[6:9]
            om = x[9:12]
            
        if np.size(x) is 13:
            #do quaternion stuff
            dq = 0.5*np.array[[0,-x[10],-x[11],-x[12]]\
                              [x[10],0,-x[12],x[11]]\
                              [x[11],-x[10],-x[11],-x[12]]\
                              [x[11],-x[10],-x[11],-x[12]]]
            
            
            
        
            
        
        
        
    
    