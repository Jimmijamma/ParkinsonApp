'''
Created on 20 mar 2017

@author: jimmijamma
'''

import requests
import json


post_url = "http://127.0.0.1:5000/process"

audio_url = "https://firebasestorage.googleapis.com/v0/b/parkinsonapp-7b987.appspot.com/o/Pazienti%2F1_03.wav?alt=media&token=2be99d72-5a56-4c25-9e67-665d0a4aa8e1"
codicePaziente = "ALEMORI1993MC"
codiceTest = "001"
dataTest =  "20-03-2017"


headers = {'content-type': 'application/json'}
data = { "audio_url": audio_url,
        "codicePaziente": codicePaziente,
        "codiceTest": codiceTest,
        "dataTest": dataTest}

r = requests.post(post_url, data=json.dumps(data), headers=headers)