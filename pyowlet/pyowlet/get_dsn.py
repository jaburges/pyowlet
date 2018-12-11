"""Class for retrieving Devices (DSN)"""

import json
import time
import logging
import re

import requests

def get_dsn(self, auth_token):
    dsnurl = 'https://ads-field.aylanetworks.com/apiv1/devices.json'
    auth_header = {'content-type': 'application/json', 'accept': 'application/json', 'Authorization': 'auth_token'}
    response = requests.get(dsnurl, headers=auth_header)
    #data = auth_header(url)
    json_data = data.json()
    # FIXME: this is just returning the first device in the list
    # dsn = json_data[0]['device']['dsn']
    return json_data[0]['device']['dsn']




""" From POSTMAN
import requests

url = "https://ads-field.aylanetworks.com/apiv1/devices.json"

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': "{auth_token}",
    'cache-control': "no-cache",
    'Postman-Token': "d1be6e91-3267-4e2e-8fb0-804b52dab2de"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)
"""