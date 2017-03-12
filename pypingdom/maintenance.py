import requests
import time


class Maintenance():

    def __init__(self, email, password):
        login_url = 'https://my.pingdom.com/'
        # LOGIN
        self.client = requests.session()
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
        response = self.client.post(login_url, data={"email": email, "password": password}, headers=self.headers)
        if response.status_code != 200:
            print("Unable to login")
            print(response.text)
            return None

    def create(self, description, start, stop, checks):
        maintenance_url = "https://my.pingdom.com/ims/data/maintenance"
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
        response = self.client.post(maintenance_url, data=data, headers=self.headers)
        if response.status_code != 200:
            print(response.text)
            return False
        else:
            return True
