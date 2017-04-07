#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 15:42:40 2017

@author: jimmijamma
Detrended Fluctuation Analysis
Python traduction of Matlab code: version 1.1 by Guan Wenye 
(https://it.mathworks.com/matlabcentral/fileexchange/19795-detrended-fluctuation-analysis)

"""

import numpy as np
from math import log, floor


def dfa_main(data):
    
    time_scales=list(np.linspace(100,1000,10)) # array of possible time scales
    
    fluctuations=[] # vector of fluctuations in different time scales
    for ts in time_scales:
        fluctuations.append(dfa_core(data, ts))
        
    # creating the log-log functions of fluctuations vs time_scale
    log_ts=[]
    for ts in time_scales:
        log_ts.append(log(ts))
    log_f=[]
    for f in fluctuations:
        log_f.append(log(f))
    aprox_f=np.polyfit(log_ts,log_f,1)
    alpha=aprox_f[0] # slope of the aproximating function of the log-log function
    
    DFA=1/(1+np.exp(-alpha))
    
    return DFA
    
    
    
def dfa_core(data, time_scale):
  
    time_scale=int(time_scale)
    n_windows=int(floor(1.0*len(data)/time_scale))
    integer_size=int(n_windows*time_scale) # resizing the signal in order to have an integer number of windows
    data=data[0:integer_size]
    mean_s=np.mean(data)
    
    integrated_data=[]
    for i in range(0,integer_size):
        integrated_data.append(np.sum(data[0:i]-mean_s))
    
    trends = []
    for j in range(1,n_windows+1):
        trends.append(np.polyfit(range(0,time_scale),data[(j-1)*time_scale:j*time_scale],1))
  
    trended_data=[]
    for k in range(1,n_windows+1):
        trended_data.extend(np.polyval(trends[k-1],range(0,time_scale)))
        
    #print len(trended_data)
    sum1=1.0*np.sum((data-trended_data)**2)/integer_size
    sum1=np.sqrt(sum1)
    
    return sum1