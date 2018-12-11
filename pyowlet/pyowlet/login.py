# Copyright (c) 2013, Jeff Terrace
# All rights reserved.

"""Contains authentication routines."""

import json
import time
import logging
import re

import requests

# configure logging
logging.basicConfig(filename='pyowlet.log',level=logging.DEBUG)
#logger = logging.getLogger('owlet')
#logger.setLevel(logging.DEBUG)

def login(email, password):
    """Logs in to the Owlet API service to get access token.

    Args:
      email: The email account tied to Owlet.
      password: The user's password.

    Returns:
      A json value with access token.
    """
    headers = {'content-type': 'application/json', 'accept': 'application/json'}
    login_url = 'https://user-field.aylanetworks.com/users/sign_in.json'
    login_payload = {
      "user": {
        "email": email,
        "password": password,
        "application": {
          "app_id": "OWL-id",
          "app_secret": "OWL-4163742"
        }
      }
    }
    logger.debug('Generating token')
    data = requests.post(
        login_url,
        json=login_payload,
        headers=self.headers
    )
    # Example response:
    # {
    #    u'access_token': u'abcdefghijklmnopqrstuvwxyz123456',
    #    u'role': u'EndUser',
    #    u'expires_in': 86400,
    #    u'refresh_token': u'123456abcdefghijklmnopqrstuvwxyz',
    #    u'role_tags': []
    # }

    json_data = data.json()

    # update our auth token
    auth_token = json_data['access_token']

    # update our auth expiration time
    expire_time = time.time() + json_data['expires_in']

    logger.debug('Auth Token: %s expires at %s', self._auth_token, self._expire_time)
	# return auth_token
	# return expire_time

def get_auth_token(self, auth_token, expire_time):
    '''
    Get the auth token. If the current token has not expired, return that.
    Otherwise login and get a new token and return that token.
    '''

    # if the auth token doesnt exist or has expired, login to get a new one
    if (auth_token is None) or (expire_time <= time.time()):
        logger.debug('Auth Token expired, need to get a new one')
        login.login()
			
    return auth_token

def _auth_request(self, url):
    '''Make a get request using the auth_token headers.'''
    auth_header = {
        'Authorization': 'auth_token ' + self.get_auth_token()
    }
    auth_header.update(self.headers)
    response = requests.get(
        url,
        headers=auth_header
    )
    return response

