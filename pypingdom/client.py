from api import Api
from gui import Gui
from check import Check
from maintenance import Maintenance


class Client(object):
    """ Interact with API and GUI """
    def __init__(self, username, password, apikey, email, api_version='2.0'):
        """
        :param username: account main email
        :param password: account password
        :param apikey: Pingdom api key
        :param email: required for `Multi-User Authentication <https://www.pingdom.com/resources/api#multi-user+authentication>`_.
        """
        self.username = username
        self.password = password
        self.apikey = apikey
        self.email = email
        self.api = Api(username, password, apikey, email, api_version)
        self.gui = Gui(username, password)
        # cache checks
        self.checks = {}
        for item in self.api.send('get', "checks", params={"include_tags": True})['checks']:
            self.checks[item["name"].lower()] = Check(self.api, name=item["name"], json=item)

    def get_check(self, name=None, _id=None):
        if name:
            return self.checks.get(name, None)
        elif _id:
            for name, check in self.checks.items():
                if check._id == _id:
                    return check
        else:
            raise "Missing name or _id"

    def get_checks(self, filters={}):
        res = []
        for name, check in self.checks.items():
            if "tags" in filters and len(set(filters["tags"]).intersection(set(check.tags))) == 0:
                continue
            res.append(check)
        return res

    def create_check(self, name, obj):
        c = Check(self.api, name, obj=obj)
        data = c.to_json()
        response = self.api.send(method='post', resource='checks', data=data)
        c._id = int(response["check"]["id"])
        c.fetch()
        self.checks[name] = c
        return c

    def delete_check(self, check):
        if not check._id:
            raise "CheckNotFound %s" + check.name
        self.api.send(method='delete', resource='checks', resource_id=check._id)
        self.checks.pop(check.name, None)

    def update_check(self, check, obj):
        # ensure definition is updated
        check.fetch()
        # cache current definition to detect idempotency when modify is called
        cached_definition = check.to_json()
        check.from_obj(obj)
        data = check.to_json()
        if data == cached_definition:
            return False
        del data["type"]  # type can't be changed
        self.api.send(method='put', resource='checks', resource_id=check._id, data=data)
        check.fetch()
        return check

    def get_maintenances(self, filters={}):
        self.gui.login()
        response = self.gui.send("get", "https://my.pingdom.com/newims/maintenance/xhr?limit=10000&page_id=1&_=1489571119019")
        res = []
        for obj in response.json()['events']:
            if "checks" in filters:
                wanted_ids = [check._id for check in filters['checks']]
                got_ids = [int(x['compound_id']) for x in obj['checks']]
                if len(set(wanted_ids).intersection(set(got_ids))) == 0:
                    continue
            window = Maintenance(self, json=obj)
            if "names" in filters and window["name"] not in filters['names']:
                continue
            if "after" in filters and filters["after"] > window.start:
                continue
            if "before" in filters and filters["before"] < window.end:
                continue
            res.append(window)
        return res

    def create_maintenance(self, obj):
        window = Maintenance(self, obj=obj)
        self.gui.login()
        response = self.gui.send("post", "https://my.pingdom.com/ims/data/maintenance", window.to_json())
        window._id = response.json()["checks_maintenance"]["id"]
        return window

    def delete_maintenance(self, window):
        self.gui.login()
        self.gui.send("delete", "https://my.pingdom.com/ims/data/maintenance", params={"id": window._id})
