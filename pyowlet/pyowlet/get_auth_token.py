"""Class for retrieving Auth Token"""

import json
import time
import logging
import re

import requests
from pyowlet import login


def get_auth_token(self, auth_token, expire_time):
    '''
    Get the auth token. If the current token has not expired, return that.
    Otherwise login and get a new token and return that token.
    '''

    # if the auth token doesnt exist or has expired, login to get a new one
    if (auth_token is None) or (expire_time <= time.time()):
        logger.debug('Auth Token expired, need to get a new one')
        login.login()
			
    auth_header = {'content-type': 'application/json', 'accept': 'application/json', 'Authorization': 'auth_token'}
	return auth_token
