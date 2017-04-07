'''
Created on 20 mar 2017

@author: jimmijamma
'''

import requests
import json


post_url = "http://127.0.0.1:5000/process"

audio_url = "https://firebasestorage.googleapis.com/v0/b/parkinsonapp-7b987.appspot.com/o/Pazienti%2F1_03.wav?alt=media&token=2be99d72-5a56-4c25-9e67-665d0a4aa8e1"
audio_position = "gs://parkinsonapp-7b987.appspot.com/Pazienti/1_03.wav"
codiceMedico = "MAR.ROS"
codicePaziente = "PGNGDO75A15D205T"
codiceTest = "001"
dataTest =  "20-03-2017"


headers = {'content-type': 'application/json'}
data = { "audio_url": audio_url,
        "audio_position":audio_position,
        "codiceMedico":codiceMedico,
        "codicePaziente": codicePaziente,
        "codiceTest": codiceTest,
        "dataTest": dataTest}

response = requests.post(post_url, data=json.dumps(data), headers=headers)

jsonResponse = response.json()

audio_position=jsonResponse["audio_position"]
codicePaziente=jsonResponse["codicePaziente"]
codiceMedico=jsonResponse["codiceMedico"]
codiceTest=jsonResponse["codiceTest"]
dataTest=jsonResponse["dataTest"]
PPE=jsonResponse["PPE"]
HNR=jsonResponse["HNR"]
RPDE=jsonResponse["RPDE"]
DFA=jsonResponse["DFA"]
UPDRS=jsonResponse["UPDRS"]

print "Codice Paziente: " + str(codicePaziente)
print "Codice Medico: " + str(codiceMedico)
print "Data del test: " + str(dataTest)
print "Codice del test: " + str(codiceTest)
print "HNR: " + str(HNR)
print "RPDE: " + str(RPDE)
print "DFA: " + str(DFA)
print "PPE: " + str(PPE)
print "UPDRS: " + str(UPDRS)
print "Posizione del file: " + str(audio_position)