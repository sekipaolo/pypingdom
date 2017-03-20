import requests
from requests.auth import HTTPBasicAuth
import json


class ApiError(Exception):

    def __init__(self, http_response):
        content = json.loads(http_response.content)
        self.status_code = http_response.status_code
        self.status_desc = content['error']['statusdesc']
        self.error_message = content['error']['errormessage']
        super(ApiError, self).__init__(self.__str__())

    def __repr__(self):
        return 'pingdom.ApiError: HTTP `%s - %s` returned with message, "%s"' % \
               (self.status_code, self.status_desc, self.error_message)

    def __str__(self):
        return self.__repr__()


class Api(object):

    def __init__(self, username, password, apikey, email=False, version="2.0"):
        self.base_url = "https://api.pingdom.com/api/" + version + "/"
        self.auth = HTTPBasicAuth(username, password)
        self.headers = {'App-Key': apikey}
        if email:
            self.headers['Account-Email'] = email

    def send(self, method, resource, resource_id="", data={}, params={}):
        response = requests.request(method, self.base_url + resource + "/" + str(resource_id), auth=self.auth, headers=self.headers, data=data, params=params)
        if response.status_code != 200:
            raise ApiError(response)
        else:
            return response.json()
