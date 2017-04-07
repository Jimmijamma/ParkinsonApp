'''
Created on 07 apr 2017

@author: jimmijamma
'''

from praat import praatUtil as praat
from numpy import mean,log2,log,exp

def logz(x):
    if (x > 0):
        y = log(x)
    else:
        y = 0
    return y


def ppe_main(filePath):

    readProgress = 0.01
    acFreqMin = 60
    voicingThreshold = 0.45
    veryAccurate = False
    fMax = 2000
    octaveJumpCost = 0.35
    silenceThreshold = 0.03
    octaveCost = 0.01
    voicedUnvoicedCost = 0.14
    verbose = False
    
    tmpFile = praat.calculateF0(filePath,readProgress,acFreqMin,voicingThreshold,veryAccurate,fMax,octaveJumpCost,silenceThreshold,octaveCost,voicedUnvoicedCost,verbose)
    offsets, f0_list = praat.readPitchTier(tmpFile)
    f0_list=list(f0_list)
    f0_list = [x for x in f0_list if x is not None]
    mean_f0 = mean(f0_list)
    r=[]
    for f0 in f0_list:
        r.append(12*log2(1.0*f0/mean_f0))   
    s = sum(r)
    p_r = []
    for element in r:
        p_r.append(1.0*element/s)
  
    N = len(p_r)
    
    PPE = 0
    for j in range (0,N-1):
        PPE = PPE - p_r[j] * logz(p_r[j])

    PPE = 1.0*PPE/log(N)

    PPE=1/(1+exp(-PPE))
    return PPE