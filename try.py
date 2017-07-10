'''
Created on 29 giu 2017

@author: jimmijamma
'''


import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json 

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

