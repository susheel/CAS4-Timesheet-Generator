from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/client_secret.json
SCOPES = 'default'
SCOPE_URL = 'https://www.googleapis.com/auth/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Python API Client'


class GClient:
    name = 'Google Python API Client'
    scopes = SCOPES
    client_secret_file = 'client_secret.json'
    credentials = None
    service = None

    def __init__(self, name=None, scopes=None, client_secret_file=None):
        if name:
            self.name = name
        if scopes:
            self.scopes = scopes
        if client_secret_file:
            self.client_secret_file = client_secret_file

    def _get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, self.scopes + '.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file,
                                                  SCOPE_URL + self.scopes)
            flow.user_agent = self.name
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        self.credentials = credentials

    def get_service(self, service_type, version='v3'):
        if self.service is None:
            self._get_credentials()
        http = self.credentials.authorize(httplib2.Http())
        self.service = discovery.build(service_type, version, http=http)
        return self.service


if __name__ == '__main__':
    c = GClient()
    service = c.get_service('calendar')
    print(service)
