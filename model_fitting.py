# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 13:56:04 2015

@author: ben
"""
import numpy as np
from transformations import quaternion_matrix

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
                              
             
                              
def com_from_point(state,point):
    """finds the state of the center of mass from the state of a rigidly attached point
   
    
    :param state: measured state of the point
    :type state: numpy array 6x1 (euler) or 7x1 (quat)
    :param point: point position in body frame
    :type point: numpy array 3x1
    :returns: state of center of mass
    :returns: numpy array 6x1 (euler) or 7x1 (quat)
    """
    if np.size(state) is 6:
        raise NotImplementedError("com_from_point not implemented for euler angle states")
    if np.size(state) is 13:
        # xbody = Qxworld        
        Q = quaternion_matrix(state[3:7])
        print(Q) 
        x_com = state[0:3] - np.dot(Q,point)
        v_com = state[7:10] - np.cross(state[10:13],point)
        state_com = np.hstack((x_com,state[3:7],v_com,state[10:13]))
        return state_com
    
            
            
            
        
            
        
        
        
    
    