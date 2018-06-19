# -*- coding: utf-8 -*-
from __future__ import absolute_import


class Check(object):

    SKIP_ON_PRINT = ["cached_definition", "_id", "api"]
    SKIP_ON_JSON = [
        "api", "alert_policy_name", "cached_definition", "created", "lastresponsetime",
        "lasttesttime", "lasterrortime", "_id", "id", "status", "maintenanceids"
    ]

    def __init__(self, api, json=False, obj=False):
        self.api = api
        if json:
            self.from_json(json)
        elif obj:
            self.from_obj(obj)
        else:
            raise Exception("Missing check definition: use json or obj parameter")

    def __repr__(self):
        attr = ["{0}: {1} ".format(k, v) for k, v in self.__dict__.items() if k not in self.SKIP_ON_PRINT]
        return "\npingdom.Check <%s> \n  %s" % (self._id, "\n  ".join(attr))

    def __contains__(self, x):
        return x in self.__dict__

    def to_json(self):
        obj = {}
        for k, v in self.__dict__.items():

            if k in self.SKIP_ON_JSON:
                pass
            elif k == "tags" and len(v):
                obj["tags"] = ",".join(map(lambda x: x['name'], v))
            elif k == "requestheaders":
                i = 0
                for x, y in v.items():
                    obj["requestheader" + str(i)] = x + ":" + y
                    i = i + 1
            else:
                obj[k] = v
        return obj

    def from_json(self, obj):
        for k, v in obj.items():
            if k == "tags":
                self.tags = [x["name"] for x in v]
            if k == "name":
                self.name = v
            elif k == "hostname":
                self.host = v
            elif k == "id":
                self._id = v
            elif k == "status":
                self.paused = bool(v == "paused")
                self.status = v
            elif k == "type" and isinstance(k, dict):
                self.type = list(v.keys())[0]
                for x, y in v[self.type].items():
                    setattr(self, x, y)
            else:
                setattr(self, k, v)
        if 'tags' not in self:
            self.tags = []

    def from_obj(self, obj):
        for k, v in obj.items():
            setattr(self, k, v)
        if 'tags' not in self:
            self.tags = []

    def fetch(self):
        res = self.api.send('get', "checks", self._id)['check']
        self.from_json(res)
