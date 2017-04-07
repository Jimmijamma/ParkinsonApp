'''
Created on 06 apr 2017

@author: jimmijamma
'''
from signalProcessing import rpde,dfa,hnr,ppe
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
    
    # down-sampling the signal
    downsampling_factor = 5
    y=decimate(y, downsampling_factor)
    fs = int(1.0 * fs / downsampling_factor)
    
    return y

def normalize_results(HNR,RPDE,DFA,PPE):
    min_HNR=8.441
    max_HNR=33.047
    mean_HNR=21.886
    std_HNR=4.426
    
    min_RPDE=0.275
    max_RPDE=0.685
    mean_RPDE=0.499
    std_RPDE=0.104
    
    min_DFA=0.574
    max_DFA=0.825
    mean_DFA=0.718
    std_DFA=0.055
    
    min_PPE=0.045
    max_PPE=0.527
    mean_PPE=0.207
    std_PPE=0.09
    
    HNR=(HNR-mean_HNR)/std_HNR
    RPDE=(RPDE-mean_RPDE)/std_RPDE
    DFA=(DFA-mean_DFA)/std_DFA
    PPE=(PPE-mean_PPE)/std_PPE
    
    HNR=-1+((HNR-min_HNR)*(1+1)/(max_HNR-min_HNR))
    RPDE=-1+((RPDE-min_RPDE)*(1+1)/(max_RPDE-min_RPDE))
    DFA=-1+((DFA-min_DFA)*(1+1)/(max_DFA-min_DFA))
    PPE=-1+((PPE-min_PPE)*(1+1)/(max_PPE-min_PPE))
    
    return HNR,RPDE,DFA,PPE
    
        
def processSignal(filePath):
    
    print "Pre-processing the signal ..."
    mono_data = pre_processing(filePath)
    
    print "Computing RPDE ..."
    RPDE = rpde.rpde_main(mono_data)
    print "RPDE: " + str(RPDE)
    
    print "Computing DFA ..."
    DFA = dfa.dfa_main(mono_data)
    print "DFA: " + str(DFA)
    
    print "Computing HNR ..."
    HNR = hnr.hnr_main(filePath)
    print "HNR: " + str(HNR)
    
    print "Computing PPE ..."
    PPE = ppe.ppe_main(filePath)
    print "PPE: " + str(PPE)   
    
    HNR_n,RPDE_n,DFA_n,PPE_n = normalize_results(HNR, RPDE, DFA, PPE)
    
    print HNR_n
    print RPDE_n
    print DFA_n
    print PPE_n
    
    return HNR_n,RPDE_n,DFA_n,PPE_n
    