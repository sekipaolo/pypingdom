import requests
from requests.auth import HTTPBasicAuth
from exception import ApiError
from maintenance import Maintenance
from check import Check

BASE_URL = 'https://api.pingdom.com/api'


class Client(object):

    def __init__(self, username, password, apikey, email, api_version='2.0'):
        self.username = username
        self.password = password
        self.apikey = apikey
        self.email = email
        self.init_api(api_version)
        self._checks = None

    def init_api(self, version):
        self.base_url = BASE_URL + "/" + version + "/"
        self.auth = HTTPBasicAuth(self.username, self.password)
        self.headers = {'App-Key': self.apikey}
        if self.email:
            self.headers['Account-Email'] = self.email

    def send(self, method, resource, resource_id="", data={}, params={}):
        try:
            response = requests.request(method, self.base_url + resource + "/" + resource_id, auth=self.auth, headers=self.headers, data=data)
        except requests.exceptions.RequestException, e:
            raise ApiError(e)
        if response.status_code != 200:
            raise Exception(response.text)
        else:
            return response.json()

    def create_maintenance(self, description, start, stop, check_names):
        m = Maintenance(self.username, self.password)
        ids = []
        for name in check_names:
            check = Check(self, name)
            if not check._id:
                raise("Check Not Found: " + name)
            ids.append(check._id)
        m.create(description, start, stop, ids)
