'''
Created on 06 apr 2017

@author: jimmijamma
'''
from signalProcessing import RPDE
from scipy.io import wavfile
from scipy.signal import decimate
from numpy import mean
from math import floor

def pre_processing(filePath):
    
    fs, y = wavfile.read(filePath) # reading the audio file
    
    y=mean(y,1) # converting from stereo to mono
    
    n_samples=len(y)
    
    # discarding the second half of the signal, if specified
    y=y[1:int(floor(n_samples/2))]

    # normalizing the signal
    y=(y-min(y))/(max(y)-min(y))
    m_y=mean(abs(y))
    y=y-m_y
    
    downsampling_factor = 5
    y=decimate(y, downsampling_factor)
    fs = int(1.0 * fs / downsampling_factor)
    
    return y
    
def processSignal(filePath):
    
    print "Pre-processing the signal ..."
    mono_data = pre_processing(filePath)
    
    print "Computing RPDE ..."
    rpde = RPDE.RPDE_main(mono_data)
    print "RPDE: " + str(rpde)