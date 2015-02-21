# -*- coding: utf-8 -*-
"""Tracking Processing

Usage:
  tracking_processing.py <df> [--roi=<rf>] [--plot]
  tracking_processing.py (-h| --help)
    
Options
  -h --help   Show this screen
  --roi=<rf>  file with start and stop times for roi
  --plot      Produces plots of the processed data
"""

import timeseries as ts
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter,lfilter,freqz
from docopt import docopt


def remap_stupid_quats(data):
    qy = data.pop('qy')
    data['qy'] = data.pop('qw')
    data['qw'] = data.pop('qz')
    data['qz'] = qy
    return data
    
def gen_planar_theta(data):
    data['theta'] = 2*np.arctan2(data['qw'],data['qz'])
    return data
   
if __name__=="__main__":
    arguments = docopt(__doc__)
    print(arguments)    
    headers, num_headers = ts.check_headers(arguments['<df>'])
    roi = np.genfromtxt(arguments['--roi'], delimiter=',',skip_header=1)
    all_data =  np.genfromtxt(arguments['<df>'],delimiter=',',skip_header=num_headers)
    data = ts.mrx_to_dict(all_data,headers[0])
    
    data = ts.remap_to_time(data)
    data = ts.zero_time(data)
    data = ts.extract_time_series(data,roi)
    
    data = remap_stupid_quats(data)
    data = gen_planar_theta(data)
    
    #remap quaternions from this particular data set
    if arguments['--plot']:
        plt.figure(1)
        plt.plot(data['time'],data['qw'])
        
        
        plt.figure(2)
        plt.plot(data['time'],data['theta'])
        
        
        plt.figure(3)
        plt.plot(data['time'],data['x'])
        plt.show()
        
    ts.timeseries_to_csv(data,'processed.csv') 
    
    