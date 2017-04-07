'''
Created on 07 apr 2017

@author: jimmijamma
'''

from praat import praatUtil as praat
from numpy import mean

def hnr_main(filePath):
    
    readProgress = 0.01
    acFreqMin = 60
    voicingThreshold = 0.1
    numPeriodsPerWindow = 4.5
    tStart = None
    tEnd = None
    outputFileName = None
    
    offsets, hnrs = praat.calculateHNR(filePath,readProgress,acFreqMin,voicingThreshold,numPeriodsPerWindow,tStart,tEnd,outputFileName)
    
    hnrs=list(hnrs)
    hnrs_2=[]
    for h in hnrs:
        if h is not None:
            hnrs_2.append(h)
    HNR = mean(hnrs_2)
    
    return HNR