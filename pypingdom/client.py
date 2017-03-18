from api import Api
from gui import Gui
from check import Check


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
            self.checks[item["name"]] = Check(self, name=item["name"], json=item)

    def get_check(self, name):
        return self.checks.get(name, None)

    def get_checks(self, filters):
        res = []
        for name, check in self.checks.items():
            if "tags" in filters and len(set(filters["tags"]).intersection(set(check.tags))) == 0:
                continue
            res.append(check)
        return res

    def create_check(self, name, obj):
        c = Check(self, name, obj=obj)
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
        if "check_names" in filters:
            filters["check_ids"] = filters.get("check_ids", []) + self.check_ids_from_names(filters["check_names"])
            del filters["check_names"]
        return self.gui.get_maintenances(filters)

    def create_maintenance(self, description, start, stop, check_names):
        self.gui.create_maintenance(description, start, stop, self.check_ids_from_names(check_names))

    def delete_maintenance(self, _id):
        self.gui.delete_maintenance(_id)

    def check_ids_from_names(self, names):
        ids = []
        for name in names:
            check = self.get_check(name)
            if check is None:
                raise("Check Not Found: " + name)
            ids.append(str(check._id))
        return ids
