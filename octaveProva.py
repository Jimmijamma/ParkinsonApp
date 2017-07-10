'''
Created on 05 lug 2017

@author: jimmijamma
'''

#from oct2py import octave
import matlab.engine
import os
from numpy import array
from numpy import random as rnd


if __name__ == '__main__':
    '''
    octave.addpath('/Users/jimmijamma/Documents/MATLAB/fastdfa')
    os.environ["OCTAVE_EXECUTABLE"] = "/path/to/your/octave/executable"
    x=[3,2,1,5]
    alpha, intervals, flucts = octave.fastdfa(x)
    '''
    x=rnd.rand(3000).tolist()
    print x
    
    eng = matlab.engine.start_matlab()
    ret = eng.fastdfa(x,nargout=3)
    alpha=ret[0]
    intervals = [item for sublist in ret[1] for item in sublist]
    flucts = [item for sublist in ret[2] for item in sublist]
    
    print alpha
    print intervals
    print flucts
 