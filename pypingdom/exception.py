
try:
    from urllib2 import HTTPError
except:
    from urllib.error import HTTPError

try:
    import json
except:
    import simplejson as json


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
