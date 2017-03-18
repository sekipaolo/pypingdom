import requests
import time
import datetime
from maintenance import Maintenance


class PingdomGuiException(Exception):
    pass


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
            dt = "\n".join(["{0}: {1} ".format(k, v) for k, v in data.items()])
            hd = "\n".join(["{0}: {1} ".format(k, v) for k, v in self.headers.items()])
            msg = " \n  url: %s \n  method: %s \n  data: %s \n  response: %s \n  headers: %s" % (url, dt, method, response.text, hd)
            raise PingdomGuiException(msg)
        return response

    def login(self):
        data = {"email": self.__username, "password": self.__password}
        self.send('post', 'https://my.pingdom.com/', data)

    def create_maintenance(self, description, start, stop, checks):
        self.login()
        data = {
            "__csrf_magic": "",
            "id": "",
            "description": description,
            "from-date": "{0}.{1}.{2}.".format(start.year, start.month, start.day),
            "from-time": "{0}:{1}".format(start.hour, start.minute),
            "to-date": "{0}.{1}.{2}.".format(stop.year, stop.month, stop.day),
            "to-time": "{0}:{1}".format(stop.hour, stop.minute),
            "start": int(time.mktime(start.timetuple())),
            "end": int(time.mktime(stop.timetuple())),
            "checks": "[{0}]".format(",".join(checks))
        }
        self.login()
        response = self.send("post", "https://my.pingdom.com/ims/data/maintenance", data)
        return response.json()["checks_maintenance"]["id"]

    def get_maintenances(self, filters={}):
        self.login()
        response = self.send("get", "https://my.pingdom.com/newims/maintenance/xhr?limit=10000&page_id=1&_=1489571119019")
        res = []
        for m in response.json()['events']:
            window = {
                "description": m["description"],
                "start": datetime.datetime.fromtimestamp(m['start']),
                "stop": datetime.datetime.fromtimestamp(m['end']),
                "check_ids": [int(x['compound_id']) for x in m['checks']],
                "_id": int(m['id'])}
            if "check_ids" in filters:
                if len(set(filters["check_ids"]).intersection(set(window["check_ids"]))) == 0:
                    continue
            if "names" in filters and window["description"] not in filters['names']:
                continue
            if "since" in filters and filters["since"] < window["start"]:
                continue
            if "before" in filters and filters["before"] > window["stop"]:
                continue

            res.append(window)
        return res

    def delete_maintenance(self, _id):
        self.login()
        self.send("delete", "https://my.pingdom.com/ims/data/maintenance", params={"id": _id})
