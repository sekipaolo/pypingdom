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
        # GET /checks (get_checks) returns 'verify_certificate' regardless
        if check.type == 'http':
            # The http-type API will only accept a parameter called 'encryption' though.
            data['encryption'] = changes['encryption'] if 'encryption' in changes else data['verify_certificate']
        del data['verify_certificate']  # 'verify_certificate' is not a valid parameter
        del data["type"]  # type can't be changed
        self.api.send(method='put', resource='checks', resource_id=check._id, data=data)
        check.from_json(self.api.send('get', "checks", check._id)['check'])
        return check

    def get_maintenances(self, filters=None):
        """Return a list of mainenance windows."""
        if filters is None:
            filters = {}
        res = []
        for mw in (Maintenance(self, json=x) for x in self.api.send('get', 'maintenance')['maintenance']):
            if "checks" in filters:
                wanted_ids = [check._id for check in filters['checks']]
                got_ids = [x._id for x in mw.checks]
                if len(set(wanted_ids).intersection(set(got_ids))) == 0:
                    continue
            if "names" in filters and mw.description not in filters['names']:
                continue
            if "after" in filters and filters["after"] >= mw.start:
                continue
            if "before" in filters and filters["before"] <= mw.stop:
                continue
            res.append(mw)
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

    def get_summary_average(self, checkid, start=None, end=None, probes=None, include_uptime=None, by_country=None,
                            by_probe=None):
        params = {}
        if start is not None:
            params['from'] = start
        if end is not None:
            params['to'] = end
        if probes is not None:
            params['probes'] = probes
        if include_uptime is not None:
            params['includeuptime'] = include_uptime
        if by_country is not None:
            params['bycountry'] = by_country
        if by_probe is not None:
            params['byprobe'] = by_probe
        return self.api.send('get', resource="summary.average", resource_id=checkid, params=params)

    def get_summary_outage(self, checkid, start=None, end=None, order="asc"):
        params = {}
        if start is not None:
            params['from'] = start
        if end is not None:
            params['to'] = end
        if order is not None:
            params['order'] = order
        return self.api.send('get', resource="summary.outage", resource_id=checkid, params=params)
