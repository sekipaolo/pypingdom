import requests
import json


class PingdomGuiException(Exception):

    def __init__(self, http_response):
        content = json.loads(http_response.content)
        self.status_code = http_response.status_code
        self.status_desc = content['error']['statusdesc']
        self.error_message = content['error']['errormessage']
        super(PingdomGuiException, self).__init__(self.__str__())

    def __repr__(self):
        return 'pingdom.PingdomGuiException: HTTP `%s - %s` returned with message, "%s"' % \
               (self.status_code, self.status_desc, self.error_message)

    def __str__(self):
        return self.__repr__()


class Gui():

    def __init__(self, username, password):
        self.session = requests.session()
        self.__username = username
        self.__password = password
        self.session = requests.session()
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://my.pingdom.com",
            "pragma": "no-cache",
            "referer": "https://my.pingdom.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

    def send(self, method, url, data={}, params={}):
        response = self.session.request(method, url, data=data, params=params, headers=self.headers)
        if response.status_code != 200:
            raise PingdomGuiException(response)
        return response

    def login(self):
        data = {"email": self.__username, "password": self.__password}
        self.send('post', 'https://my.pingdom.com/', data)
