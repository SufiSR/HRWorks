import requests

import json

url = "https://api.hrworks.de"


def get_token():
    global headers
    payload = {
        "accessKey": "YOURACCESSKEY",
        "secretAccessKey": "YOURSECRET"
    }
    authentication_response = requests.post(url+"/v2/authentication", data=json.dumps(payload))    
    authentication_json = authentication_response.json()
    headers = {
        "Authorization": "Bearer"+" "+authentication_json["token"]
    }
    
def get_available_working_hours():
    endpoint = "/v2/persons/available-working-hours"
    payload = {
        "persons":["Scully"],
        "beginDate": "2022-01-01",
        "endDate": "2022-06-15",
        "interval": "days"
    }
    r = requests.get(url + endpoint, data=json.dumps(payload), headers=headers)
    print(r.json())
    return

get_token()
get_available_working_hours()
