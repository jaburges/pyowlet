#!/usr/bin/env python

import time

import requests
import logging
__author__ = 'fgorodishter'

# configure logging
logging.basicConfig()
logger = logging.getLogger('owlet')
logger.setLevel(logging.DEBUG)


class Owlet(object):

    def __init__(self, email, password):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        self.properties = [
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

        self._auth_token = None
        self._expire_time = 0

        self.email = email
        self.password = password

    def _login(self):
        '''Generate a new auth token.'''
        login_url = 'https://user-field.aylanetworks.com/users/sign_in.json'
        login_payload = {
          "user": {
            "email": self.email,
            "password": self.password,
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
        self._auth_token = json_data['access_token']

        # update our auth expiration time
        self._expire_time = time.time() + json_data['expires_in']

        logger.debug('Auth Token: %s expires at %s', self._auth_token, self._expire_time)

    def get_auth_token(self):
        '''
        Get the auth token.

        If the current token has not expired, return that.
        Otherwise login and get a new token and return that token.
        '''

        # if the auth token doesnt exist or has expired, login to get a new one
        if (self._auth_token is None) or (self._expire_time <= time.time()):
            logger.debug('Auth Token expired, need to get a new one')
            self._login()

        return self._auth_token

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

    def get_dsn(self):
        url = 'https://ads-field.aylanetworks.com/apiv1/devices.json'
        data = self._auth_request(url)
        json_data = data.json()
        # FIXME: this is just returning the first device in the list
        return json_data[0]['device']['dsn']

    def get_data(self):
        '''
        Generator that returns a dict of o2 and hr.

        Example:
        {
            'HEART_RATE': 151,
            'OXYGEN_LEVEL': 100,
            'data_updated_at': u'2017-11-12T19:10:08Z',
        }
        '''

        # get the dsn for the device
        dsn = self.get_dsn()

        # create the properties url with our dsn
        properties_url = 'https://ads-field.aylanetworks.com/apiv1/dsns/{}/properties'.format(dsn)

        last_time = {p: 0 for p in self.properties}

        delay = 1

        while True:
            time.sleep(delay)

            output = {}
            for measure in self.properties:
                url = properties_url + '/' + measure
                response = self._auth_request(url)
                data = response.json()['property']
                if data['data_updated_at'] == last_time[measure]:
                    # increase the delay so we don't hammer their api
                    # keep doubling the delay each time the measurements don't update
                    # up to a maximum of 5 minutes
                    delay = min(delay * 2, 300)
                    logger.debug(
                        'No update for %s since %s. Increasing delay to %s seconds',
                        measure,
                        last_time[measure],
                        delay
                    )
                    continue

                # reset the delay to 1 second
                delay = 1

                # save the data_updated_at time so we don't keep printing duplicate data
                last_time[measure] = data['data_updated_at']

                logger.info(
                    "%s = %s @ %s",
                    measure,
                    data['value'],
                    data['data_updated_at']
                )

                # set the output value for this measure
                output[measure] = data['value']
                # update the updated at value
                output['data_updated_at'] = data['data_updated_at']

            # log to es
            # requests.post(
            #    'http://ES_ADDRESS:9200/owlet/measure/' + output['data_updated_at'],
            #    verify=False,
            #    json=output,
            #    headers=self.headers
            # )

            if output:
                yield output


if __name__ == "__main__":
    import sys

    # get credentials from the commandline
    # python owlet_status.py email password
    email = sys.argv[1]
    password = sys.argv[2]

    o = Owlet(
        email=email,
        password=password
    )
    for data in o.get_data():
        print(data)
