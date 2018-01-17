# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .api import Api
from .gui import Gui
from .check import Check
from .maintenance import Maintenance


class Client(object):
    """Interact with API and GUI."""

    def __init__(self, username, password, apikey, email, api_version='2.0'):
        """
        Initializer.

        :param username: account main email
        :param password: account password
        :param apikey: Pingdom api key
        :param email: required for `Multi-User Authentication
                      <https://www.pingdom.com/resources/api#multi-user+authentication>`_.
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
            self.checks[item["name"]] = Check(self.api, json=item)

    def get_check(self, name=None, _id=None):
        if name:
            return self.checks.get(name, None)
        elif _id:
            for _name, check in self.checks.items():
                if check._id == _id:
                    return check
        else:
            raise Exception("Missing name or _id")

    def get_checks(self, filters=None):
        if filters is None:
            return [c for c in self.checks.values()]
        return [c for c in self.checks.values() if not len(set(filters.get("tags", [])).intersection(set([x['name']
                for x in c.tags]))) == 0]

    def create_check(self, obj):
        c = Check(self.api, obj=obj)
        data = c.to_json()
        response = self.api.send(method='post', resource='checks', data=data)
        c._id = int(response["check"]["id"])
        c.from_json(self.api.send('get', "checks", response["check"]["id"])['check'])
        self.checks[c.name] = c
        return c

    def delete_check(self, check):
        if not check._id:
            raise Exception("CheckNotFound %s" % check.name)
        self.api.send(method='delete', resource='checks', resource_id=check._id)
        self.checks.pop(check.name, None)

    def update_check(self, check, changes):
        # ensure definition is updated
        check.fetch()
        # cache current definition to detect idempotence when modify is called
        cached_definition = check.to_json()
        check.from_obj(changes)
        data = check.to_json()
        if data == cached_definition:
            return False
        del data["type"]  # type can't be changed
        self.api.send(method='put', resource='checks', resource_id=check._id, data=data)
        check.from_json(self.api.send('get', "checks", check._id)['check'])
        return check

    def get_maintenances(self, filters=None):
        if filters is None:
            filters = {}
        self.gui.login()
        url = "https://my.pingdom.com/newims/maintenance/xhr?limit=10000&page_id=1&_=1489571119019"
        response = self.gui.send("get", url)
        res = []
        for obj in response.json()['events']:
            if "checks" in filters:
                wanted_ids = [check._id for check in filters['checks']]
                got_ids = [int(x['compound_id']) for x in obj['checks']]
                if len(set(wanted_ids).intersection(set(got_ids))) == 0:
                    continue
            window = Maintenance(self, json=obj)
            if "names" in filters and window.name not in filters['names']:
                continue
            if "after" in filters and filters["after"] >= window.start:
                continue
            if "before" in filters and filters["before"] <= window.stop:
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

    def servertime(self):
        return self.api.send(method='get', resource='servertime')['servertime']

    def get_summary_outage(self, checkid, start=None, end=None, order="asc"):
        params = {}
        if start is not None:
            params['from'] = start
        if end is not None:
            params['to'] = end
        if order is not None:
            params['order'] = order
        return self.api.send('get', resource="summary.outage", resource_id=checkid, params=params)
