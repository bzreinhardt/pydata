# -*- coding: utf-8 -*-
import scipy
import numpy as np
import matplotlib.pyplot as plt
import csv

'''
Functions for dealing with timeseries data
'''

'''Utility'''
def is_number(s):
    """Check if a string is a number"""
    try: 
        float(s)
        return True
    except ValueError:
        return False
'''IO '''
def check_headers(filename ):
    """Reports the headers for filename.
    
    :param filename: path for the file 
    :type filename: str
    :returns: array of str -- the headers
    :returns: int -- number of header lines
    
        
    """
    with open(filename,'r') as data_file:
        i = 0
        headers = []
        reader = csv.reader(data_file,delimiter=',')
        for row in reader:
            if is_number(row[0]) or len(row) == 0:
                break
            else:
                i += 1
                headers.append(row)
        return headers, i
        
def gen_header(data_dict):
    keys = data_dict.keys()
    header = ','.join(keys)
    return header
    
def timeseries_to_csv(data_dict,filename, fmt='%.5e'):
    ''' Saves data_dict to filename as a column csv'''
    no_time_keys = filter(lambda s: s is not "time", data_dict.keys())
    keys = ['time']
    keys.extend(no_time_keys)
    new_header = ','.join(keys)
    mrx = data_to_mrx(data_dict,keys).T
    np.savetxt(filename,mrx, delimiter =',',header=new_header,fmt=fmt)
    
        

'''Conversions'''
def mrx_to_dict(data,keys,data_dict={}):
    """
    Converts a matrix of data and a list of keys to a data dictionary
    """
    dim = -1    
    for i in range(0,2):
        if np.size(data,i) is len(keys):
            dim = i
    if dim is -1:
        raise TypeError("Different number of columns and data keys") 
    for i in range(0,len(keys)):
        if dim is 0:
            data_dict[str(keys[i])] = data[i,:].T
        else:
            data_dict[str(keys[i])] = data[:,i]
    return data_dict
    
     
def transform_mrx(X,A,B=0):
    """
    Transforms a set of 3 coordinates by a matrix
    """
    if B is 0:
        B = np.zeros(np.shape(X))
    X = np.atleast_2d(X)
    A = np.atleast_2d(A)
    B = np.atleast_2d(B)
    d = np.size(A,1)
    if np.size(X,0) is not d and np.size(X,1) is d:
        X = np.transpose(X)
    elif np.size(X,0) is not d and np.size(X,1) is not d:
        raise TypeError("wrong dimensions")
    y = np.dot(A,X)+B
    return y
    
            
def data_to_mrx(data_dict,keys):   
    mrx = np.array([])    
    for key in keys:
        print(key)
        if len(mrx) is 0:
            if np.size(np.atleast_2d(data_dict[key]),1) is 1:
                mrx = data_dict[key].T
            else:
                mrx = data_dict[key]
        
        else:
            if np.size(np.atleast_2d(data_dict[key]),1) is 1:
                mrx = np.vstack((mrx,data_dict[key].T))
            else:
                mrx = np.vstack((mrx,data_dict[key]))    
    return mrx
    

    
def transform_data(data_dict,keys,A,B=0):
    '''
    Performs an affine transform AX+B where X is located in keys of data_dict
    '''
    X = data_to_mrx(data_dict,keys)
    mrx = transform_mrx(X,A,B)
    data_dict = mrx_to_dict(mrx,keys,data_dict)
    return data_dict
    
def extract_time_series(data_dict,interval):
    '''get data associated with a single time interval'''
    
    t = data_dict['time']
   
    
    for key in data_dict.keys():
    
        data_dict[key] = data_dict[key][np.logical_and(t > interval[0], t < interval[1])]
    return data_dict
    
def remove_sign_outliers(data,region=1,scale=1,threshold = 0.05, method=-1):
    '''
    removes the outliers from a timeseries
    '''
    
    for i in range(region,len(data)-region):
        #only check when things aren't very close to zero
        if np.abs(data[i]) > threshold*scale:
            if np.sign(np.mean(np.sign(data[i-region:i]))) != np.sign(data[i]) \
            and np.sign(np.mean(np.sign(data[i-region:i]))) != np.sign(data[i+region]):
                if method is -1:
                    data[i] *= -1
    return data
            
            
    
def remap_to_time(data_dict):
    '''
    Makes sure the time in timeseries data has the right identifier
    '''
    eq_keys = ['t','timeseries','timestamp','# time'] #this should be a regexp
    for key in eq_keys:
        if key in data_dict:
            time = data_dict.pop(key)
            data_dict['time'] = time
    return data_dict
    
def zero_time(data_dict):
     t_0 = data_dict['time'][0]
     data_dict['time'] = data_dict['time']-t_0
     return data_dict
        
class TestFunctions:
    filename = '/home/ben/experiment-analysis/spin_test2_2014_Aug_28/PoseLog.csv'
    def test_check_headers(self):
        header_lines,i = check_headers(self.filename)
        print(header_lines)
    def test_get_data_dict(self):
        get_data_dict(self.filename)
       # print(reader.keys())
    def test_genfromtxt(self):
        data = np.genfromtxt(self.filename, delimiter=',',skip_header=1)
        print(np.size(data,2))

if __name__=='__main__':
    A = np.array([[769.464978558294,0,635.224289485861],[0,768.751988580164,491.728901817741],[0,0,1]])
    data_file = '/home/ben/experiment-analysis/spin_test2_2014_Aug_28/PoseLog.csv'
    time_file = '/home/ben/experiment-analysis/spin_test2_2014_Aug_28/timestamps.txt'
    roi_file =  '/home/ben/experiment-analysis/spin_test2_2014_Aug_28/good_data.csv'
    test_file = 'test_write.csv'
    
    headers, num_headers = check_headers(data_file)
    timestamps = np.genfromtxt(time_file)
    roi = np.genfromtxt(roi_file,delimiter=',',skip_header=1)    
    
    all_data = np.genfromtxt(data_file,delimiter=',',skip_header=num_headers)
    data_dict = mrx_to_dict(all_data,headers[0])
    data_dict = remap_to_time(data_dict)
    
    
    
    data_dict = zero_time(data_dict)
    plt.figure(1)
    plt.plot(data_dict['x'],data_dict['y'])
    
    data_dict = transform_data(data_dict,['x','y','z'],A)
    plt.figure(2)
    plt.plot(data_dict['x'],data_dict['y'])
    
    data_dict = extract_time_series(data_dict,roi)
  
    plt.figure(3)
    plt.plot(data_dict['x'],data_dict['y'])
    
    timeseries_to_csv(data_dict,test_file) 
    headers, num_headers = check_headers(test_file)
    new_data = np.genfromtxt(test_file,delimiter=',',skip_header=1)
    new_data_dict = mrx_to_dict(new_data,headers[0])
    
    plt.figure(4)
    plt.plot(new_data_dict['x'],new_data_dict['y'])
    
   
    
    
       
    

    
    
    
        
        
     
    