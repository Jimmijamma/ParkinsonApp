'''
Created on 09 lug 2017

@author: jimmijamma
'''
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile



def truncate_silence(data):
    is_silence=[]
    threshold=0.01
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
    noise=data[:ii*n]
    print ii
    
    return trunc_data,noise




if __name__ == '__main__':
    
    
    fs, y = wavfile.read('CNJp4fLaRARNyZyJlUoXuH1PRqj2_ssss_12231.wav') # reading the audio file
    
    if len(y.shape)>1:
        y=np.mean(y,1) # converting from stereo to mono
        


    n_samples=len(y)
    
    # discarding the second half of the signal, if specified
    y=y[1:int(np.floor(n_samples/2))]
    
    plt.plot(y)
    #plt.show()
    plt.savefig('before_processing')
    plt.close()


    # normalizing the signal
    y_min = min(y)
    y_max = max(y)
    
    y=y-np.mean(y)
    #y=(y-min(y))/(max(y)-min(y))
    y_norm=[]
    for sample in y:
        y_norm.append(2.0*(sample-y_min)/(y_max-y_min)-1)
        
        
    y_norm=y_norm-np.mean(y_norm)

    
    y_norm,noise=truncate_silence(y_norm)



    
    sp_n = np.fft.fft(noise)
    freq_n = np.fft.fftfreq(len(noise))
    plt.plot(freq_n, sp_n.real)
    plt.xlim(0,0.1)
    plt.savefig('fft_noise')
    plt.close()
    
    sp = np.fft.fft(y_norm, n=len(noise))
    freq = np.fft.fftfreq(len(noise))
    plt.plot(freq, sp.real)
    plt.xlim(0,0.2)
    plt.savefig('fft_signal')
    plt.close()
    
    signal=np.array(sp.real)
    noise=np.array(sp_n.real)
    clean=signal-noise
    freq_c = np.fft.fftfreq(len(clean))
    plt.plot(freq_c, clean)
    plt.xlim(0,0.2)
    plt.savefig('fft_clean')
    plt.close()
    
    print clean[:20]
    print sp.real[:20]
    print sp_n.real[:20]
    