'''
Created on 20 mar 2017

@author: jimmijamma
'''
import netifaces as ni
from flask import Flask
from flask import request
import json
import os
from urllib import URLopener
from threading import Thread
import processSignal as ps
from parkinson_neural_network import neuralnet_main
from firebase import firebase
#import pyrebase
import requests
from datetime import datetime
from numpy import mean



from scipy.io import wavfile
import matplotlib.pyplot as plt


app = Flask(__name__)

def receiveRequest(data):
    print data
    j = json.loads(data)
    audio_url = j["audio_url"]
    codicePaziente = j["codicePaziente"]
    codiceMedico= j["codicemed"]
    codiceTest = 'ssss'
    dataTest = '12231'
    print codiceMedico
    tmp_directory = os.getcwd() +"/temp"
    if not os.path.exists(tmp_directory):
        os.makedirs(tmp_directory)
        
    filePath = tmp_directory + "/" + codicePaziente + "_" + codiceTest + "_" + dataTest + ".wav"
    
    #testfile = URLopener()
    #testfile.retrieve(audio_url, filePath)
    
    r = requests.get(audio_url, stream=True, auth=requests.auth.HTTPBasicAuth('user', 'pass'))
    with open(filePath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    
    return filePath, j

def writeResponse(row,status,jsonRequest):
    HNR=row[0]
    RPDE=row[1]
    DFA=row[2]
    PPE=row[3]
    codicePaziente = jsonRequest["codicePaziente"]
    audio_position = jsonRequest["audio_position"]
    
    now=datetime.now()
    
    year=now.year
    day=now.day
    month=now.month
    
    hour=now.hour
    minute=now.minute
    
    giorno=str(day)+'-'+str(month)+'-'+str(year)
    ora=str(hour)+':'+str(minute)
    
    '''
    now=str(datetime.now())
    now=now.replace(' ', '_').replace('.', '_').replace('-','_')
    pieces=now.split(':')
    del pieces[-1]
    now=':'.join(pieces)
    '''

    data = { "audio_position":audio_position,
        "dataTest": giorno+ora,
        "HNR":HNR,
        "RPDE":RPDE,
        "DFA":DFA,
        "PPE":PPE,
        "UPDRS":status}
    
    
    db = firebase.FirebaseApplication('https://parkinsonapp-7b987.firebaseio.com/', None)
    res_path='users/'+str(codicePaziente)+'/results/'+str(giorno)+"_"+str(ora)
    res='Data: ' + str(giorno)+"_"+str(ora)+', '+'UPDRS: '+str(status)
    result = db.put(url='https://parkinsonapp-7b987.firebaseio.com/',name=res_path,data=res)
    
    test_path='users/'+str(codicePaziente)+'/Tests/'+str(giorno)+"_"+str(ora)
    db.put(url='https://parkinsonapp-7b987.firebaseio.com/',name=test_path + '/date' ,data=giorno+'_'+ora)
    db.put(url='https://parkinsonapp-7b987.firebaseio.com/',name=test_path + '/HNR' ,data=HNR) 
    db.put(url='https://parkinsonapp-7b987.firebaseio.com/',name=test_path + '/DFA' ,data=DFA)
    db.put(url='https://parkinsonapp-7b987.firebaseio.com/',name=test_path + '/RPDE' ,data=RPDE)
    db.put(url='https://parkinsonapp-7b987.firebaseio.com/',name=test_path + '/PPE' ,data=PPE)
    db.put(url='https://parkinsonapp-7b987.firebaseio.com/',name=test_path + '/UPDRS' ,data=status)
    db.put(url='https://parkinsonapp-7b987.firebaseio.com/',name=test_path + '/audio_url' ,data=audio_position)
    
    
    #firebase = firebase.FirebaseApplication('https://parkinsonapp-7b987.firebaseio.com/', None)
    #nuovo_paziente="Paziente2"
    #result = firebase.post('/Medici/Medico1/Pazienti', nuovo_paziente, json.dumps(data))

    return data

@app.route('/', methods= ['GET', 'POST'])
def process():
    if request.method == 'POST':
        data = request.data
        filePath, jsonRequest = receiveRequest(data) 
        
        HNR,RPDE,DFA,PPE=ps.processSignal(filePath)
        row=[HNR,RPDE,DFA,PPE]
        row=[0.079633,-0.234945,-0.144857,-0.643293]
        status, probabilities = ps.machineLearningAzure(HNR, RPDE, DFA, PPE)
           
        print"Status of the patient: " + str(status)
        jsonResponse=writeResponse(row, status, jsonRequest)
        response = app.response_class(response=json.dumps(jsonResponse),status=200,mimetype='application/json')     
        return response
    else:
        return 'Upload Page'
    


if __name__ == '__main__':
    ni.ifaddresses('en0')
    ip = ni.ifaddresses('en0')[2][0]['addr']
    ip_complete="http://" + str(ip) +":5000/"
    print ip_complete

    db = firebase.FirebaseApplication('https://parkinsonapp-7b987.firebaseio.com/', None)
    server = 'Flask_server'
    data={'ip':ip_complete}
    
    result = db.put(url='https://parkinsonapp-7b987.firebaseio.com/',name='Server/ip',data=ip_complete)
    
    app.debug = True
    app.run(host='0.0.0.0', debug = True)

   