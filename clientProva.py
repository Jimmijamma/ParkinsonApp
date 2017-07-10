'''
Created on 20 mar 2017

@author: jimmijamma
'''

import requests
import json


post_url = "http://127.0.0.1:5000/"


audio_url = "https://firebasestorage.googleapis.com/v0/b/parkinsonapp-7b987.appspot.com/o/audio%2FVrAXqFo56nRJVCXRuzXisyTNG4R2%2F2017_07_05_14_32_55.wav?alt=media&token=83062f74-81d9-45dd-bd3e-262f5b75ca98"
audio_position = "gs://parkinsonapp-7b987.appspot.com/audio/VrAXqFo56nRJVCXRuzXisyTNG4R2/2017_07_05_14_32_55.wav"
codiceMedico = "MAR.ROS"
codicePaziente = "CNJp4fLaRARNyZyJlUoXuH1PRqj2"
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

"""
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
print "Posizione del file: " + str(audio_position)"""