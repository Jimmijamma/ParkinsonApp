'''
Created on 20 mar 2017

@author: jimmijamma
'''

from flask import Flask
from flask import request
import json
import os
from urllib import URLopener
from threading import Thread
import processSignal as ps

app = Flask(__name__)

def receiveRequest(data):
    
    j = json.loads(data)
    audio_url = j["audio_url"]
    codicePaziente = j["codicePaziente"]
    codiceTest = j["codiceTest"]
    dataTest = j["dataTest"]
    
    tmp_directory = os.getcwd() +"/temp"
    if not os.path.exists(tmp_directory):
        os.makedirs(tmp_directory)
        
    filePath = tmp_directory + "/" + codicePaziente + "_" + codiceTest + "_" + dataTest + ".wav"
    
    testfile = URLopener()
    testfile.retrieve(audio_url, filePath)
    
    return filePath
    

@app.route('/process', methods= ['GET', 'POST'])
def process():
    if request.method == 'POST':
        data = request.data
        filePath = receiveRequest(data) 
        
        process_thread=Thread(target=ps.processSignal(), args=[filePath])
        process_thread.start()
        
        return '200'
    else:
        return 'Upload Page'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', debug = True)