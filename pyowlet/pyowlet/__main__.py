import json
import logging
import time
import sys

from pyowlet import login
from pyowlet import get_auth_token
from pyowlet import get_dsn

def login_to_owlet(args):
    """Logs into Owlet unnoficial API
    Args: 
      args: argparse arguments needed to login.
      
    Returns: Auth token needed to login to retrieve data from account
    """
    auth_token = None
    expire_time = 0

    auth_token = login.login
    if not auth_token:
        sys.exit('Could not get token from Owlet API.')

def main():
    """Main method for the Script"""
    dsn = get_dsn.get_dsn

    properties = [
        'OXYGEN_LEVEL',
        'HEART_RATE',
        'BASE_STATION_ON',
        'BATT_LEVEL',
        'MOVEMENT',
        'SOCK_OFF',
        'CHARGE_STATUS',
        'BABY_NAME',
        'SOCK_CONNECTION',	
    ]

    properties_url = 'https://ads-field.aylanetworks.com/apiv1/dsns/{}/properties'.format(dsn)

    #last_time = {p: 0 for p in self.properties}

    for measure in properties:
      measure_url = properties_url + '/' + measure
      response = requests.get(measure_url, headers=auth_header)
      data = response.json()['property']
      return data
	  