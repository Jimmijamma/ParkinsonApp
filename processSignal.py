'''
Created on 06 apr 2017

@author: jimmijamma
'''
from signalProcessing import rpde,dfa,hnr,ppe
from scipy.io import wavfile
from scipy.signal import decimate
from numpy import mean
from math import floor
import urllib2
import matplotlib.pyplot as plt

import json 

import matlab.engine
import scipy.io as sio
import numpy as np

def pre_processing(filePath):
    
    fs, y = wavfile.read(filePath) # reading the audio file
    
    if len(y.shape)>1:
        y=mean(y,1) # converting from stereo to mono
        


    n_samples=len(y)
    
    plt.plot(y)
    #plt.show()
    plt.savefig('before_processing')
    plt.close()
    
    # discarding the second half of the signal, if specified
    y=y[1:int(floor(n_samples/2))]
    
    # normalizing the signal
    y_min = min(y)
    y_max = max(y)
    
    y=y-mean(y)
    #y=(y-min(y))/(max(y)-min(y))
    y_norm=[]
    for sample in y:
        y_norm.append(2.0*(sample-y_min)/(y_max-y_min)-1)
        
        
    y_norm=y_norm-mean(y_norm)

    
    y_norm=truncate_silence(y_norm)
    '''
    
    # down-sampling the signal
    downsampling_factor = 5
    y_norm=decimate(y_norm, downsampling_factor)
    fs = int(1.0 * fs / downsampling_factor)
    '''
    
    plt.plot(y_norm)
    #plt.show()
    plt.savefig('after_processing')
    plt.close()
    
    return y_norm


def truncate_silence(data):
    is_silence=[]
    threshold=0.1
    n=2000
    chunks=[]
    n_chunks=len(data)/2-1
    print len(data)


    for i in range(n_chunks):
        chunks.append(data[i*n:i*n + n])
        
    ii=0
    while max(abs(chunks[ii]))<threshold:
        ii=ii+1
    
    trunc_data=data[ii*n:]
    print ii
    
    return trunc_data
        
            
def normalize_results(HNR,RPDE,DFA,PPE):
    min_HNR=8.441
    max_HNR=37.047
    mean_HNR=21.679
    std_HNR=4.291
    
    min_RPDE=0.275
    max_RPDE=1
    mean_RPDE=0.541
    std_RPDE=0.101
    
    min_DFA=0.0
    max_DFA=0.825
    mean_DFA=0.653
    std_DFA=0.071
    
    min_PPE=0.045
    max_PPE=1
    mean_PPE=0.220
    std_PPE=0.091
    

    HNR=(HNR-min_HNR)/(max_HNR-min_HNR)
    RPDE=(RPDE-min_RPDE)/(max_RPDE-min_RPDE)
    DFA=(DFA-min_DFA)/(max_DFA-min_DFA)
    PPE=(PPE-min_PPE)/(max_PPE-min_PPE)
    

    return HNR,RPDE,DFA,PPE


        
def processSignal(filePath):

    print "Pre-processing the signal ..."
    mono_data = pre_processing(filePath)
    
    plt.plot(mono_data)
    #plt.show()
    plt.savefig('bellaxnoi')
    plt.close()
    '''
    print "Computing RPDE ..."
    RPDE = rpde.rpde_main(mono_data)
    print "RPDE: " + str(RPDE)
    RPDE=0.5
    
    print "Computing DFA ..."
    DFA = dfa.dfa_main(mono_data)
    print "DFA: " + str(DFA)
    '''
    mono_data=mono_data.tolist()
    sio.savemat('input.mat', {'input':mono_data})
    eng = matlab.engine.start_matlab()
    H_norm, alpha, rpd, intervals, flucts = eng.rpde_dfa(nargout=5)
    RPDE=H_norm
    print "RPDE: " + str(RPDE)
    DFA=1.0/(1+np.exp(-alpha))
    print "DFA: " + str(DFA)
    
    
    print "Computing HNR ..."
    HNR = hnr.hnr_main(filePath)
    print "HNR: " + str(HNR)
    
   # print "Computing PPE ..."
   # PPE = ppe.ppe_main(filePath)
    #print "PPE: " + str(PPE)   
    
    #HNR_n,RPDE_n,DFA_n,PPE_n = normalize_results(HNR, RPDE, DFA, PPE)
    #PPE_n=0.05
    PPE=0.3
    print HNR
    print RPDE
    print DFA
    print PPE
    return HNR,RPDE,DFA,PPE
    
    
    
def machineLearningAzure(HNR,RPDE,DFA, PPE):
    
    data =  {
    
            "Inputs": {
    
                    "input1":
                    {
                        "ColumnNames": ["HNR", "RPDE", "DFA", "PPE"],
                        "Values": [ [ HNR, RPDE, DFA, PPE ], [ "0", "0", "0", "0" ], ]
                    },        },
                "GlobalParameters": {
            "New column names": "",
    }
        }
    
    body = str.encode(json.dumps(data))
    
    url = 'https://ussouthcentral.services.azureml.net/workspaces/5ac2e4bc0ef54ee28baf52a4459f7e89/services/7a5c0459a1f24611a5ab317dd281ea21/execute?api-version=2.0&details=true'
    api_key = 'MddI7aOlsU02mEqoMazZA9PFCswCpXlcrBuiE8+6BsRXUx6sV1sEE2hP5HorWUlm4XciNVgF0v6uD/eD0UTVKA==' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    
    req = urllib2.Request(url, body, headers) 
    
    try:
        response = urllib2.urlopen(req)
    
        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        # req = urllib.request.Request(url, body, headers) 
        # response = urllib.request.urlopen(req)
    
        result = response.read()
        result=json.loads(result)
        score = result['Results']['output1']['value']['Values'][0][-1]
        probabilities = result['Results']['output1']['value']['Values'][0][4:-1]
        
        prob2=[]
        for p in probabilities:
            prob2.append(float(p))
        
        return score, prob2
    
    except urllib2.HTTPError, error:
        print("The request failed with status code: " + str(error.code))
    
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
    
        print(json.loads(error.read()))  
        
        return -1

