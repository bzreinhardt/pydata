# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 10:43:40 2015

@author: ben
"""

import timeseries as ts
import numpy as np
import matplotlib.pyplot as plt

if __name__=="__main__":

    A = np.array([[769.464978558294,0,635.224289485861],[0,768.751988580164,491.728901817741],[0,0,1]])
   
    data_file = '/home/ben/experiment-analysis/spin_test2_2014_Aug_28/PoseLog.csv'
    time_file = '/home/ben/experiment-analysis/spin_test2_2014_Aug_28/timestamps.txt'
    roi_file =  '/home/ben/experiment-analysis/spin_test2_2014_Aug_28/good_data.csv'
    test_file = 'test_write.csv'
    
    headers, num_headers = ts.check_headers(data_file)
    timestamps = np.genfromtxt(time_file)
    roi = np.genfromtxt(roi_file,delimiter=',',skip_header=1)    
    
    all_data = np.genfromtxt(data_file,delimiter=',',skip_header=num_headers)
    data_dict = ts.mrx_to_dict(all_data,headers[0])
    data_dict = ts.remap_to_time(data_dict)
    
    
    
    data_dict = ts.zero_time(data_dict)
    plt.figure(1)
    plt.plot(data_dict['x'],data_dict['y'])
    
    
    data_dict = ts.extract_time_series(data_dict,roi)
      
    plt.figure(3)
    plt.plot(data_dict['x'],data_dict['y'])
    
    #Convert Y data

    data_dict = ts.transform_data(data_dict,['y'],np.atleast_2d(-1),np.atleast_2d(1))
    
    plt.figure(4)
    plt.plot(data_dict['x'],data_dict['y'])
    
    ts.timeseries_to_csv(data_dict,test_file) 
    headers, num_headers = ts.check_headers(test_file)
    new_data = np.genfromtxt(test_file,delimiter=',',skip_header=1)
    new_data_dict = ts.mrx_to_dict(new_data,headers[0]) #note this is still in pixel coordiantes
    
    plt.figure(5)
    plt.plot(new_data_dict['x'],new_data_dict['y'])
    
    plt.figure(6)
    plt.plot(new_data_dict['time'],new_data_dict['qz'])
    
    new_data_dict['qz'] *= -1 
    new_data_dict['qz'] = ts.remove_sign_outliers(new_data_dict['qz'],region = 1,threshold=0.1)
    plt.figure(7)
    plt.plot(new_data_dict['time'],new_data_dict['qz'])
    
    