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
from parkinson_neural_network import neuralnet_main

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
    
    return filePath, j

def writeResponse(row,status,jsonRequest):
    HNR=row[0]
    RPDE=row[1]
    DFA=row[2]
    PPE=row[3]
    codicePaziente = jsonRequest["codicePaziente"]
    audio_position = jsonRequest["audio_position"]
    codiceMedico = jsonRequest["codiceMedico"]
    codiceTest = jsonRequest["codiceTest"]
    dataTest = jsonRequest["dataTest"]
    
    data = { "audio_position":audio_position,
        "codicePaziente": codicePaziente,
        "codiceMedico":codiceMedico,
        "codiceTest": codiceTest,
        "dataTest": dataTest,
        "HNR":HNR,
        "RPDE":RPDE,
        "DFA":DFA,
        "PPE":PPE,
        "UPDRS":status}
    
    return data

@app.route('/process', methods= ['GET', 'POST'])
def process():
    if request.method == 'POST':
        data = request.data
        filePath, jsonRequest = receiveRequest(data) 
        
        #HNR,RPDE,DFA,PPE=ps.processSignal(filePath)
        #row=[HNR,RPDE,DFA,PPE]
        row=[0.079633,-0.234945,-0.144857,-0.643293]
        status=neuralnet_main(row)
           
        print"Status of the patient: " + str(status)
        jsonResponse=writeResponse(row, status, jsonRequest)
        response = app.response_class(response=json.dumps(jsonResponse),status=200,mimetype='application/json')     
        return response
    else:
        return 'Upload Page'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', debug = True)