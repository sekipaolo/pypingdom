class Check(object):

    SKIP_ON_PRINT = ["cached_definition", "_id", "api"]
    SKIP_ON_JSON = [
        "api", "alert_policy_name", "cached_definition", "created", "lastresponsetime",
        "lasttesttime", "_id", "id", "status"
    ]

    def __init__(self, api, name, json=False, obj=False):
        self.api = api
        self.name = name
        if json:
            self.from_json(json)
        elif obj:
            self.from_obj(obj)
        else:
            raise "Missing check definition: use json or obj parameter"

    def __repr__(self):
        attr = ["{0}: {1} ".format(k, v) for k, v in self.__dict__.items() if k not in self.SKIP_ON_PRINT]
        return "\npingdom.Check <%s> \n  %s" % (self._id, "\n  ".join(attr))

    def to_json(self):
        obj = {}
        for k, v in self.__dict__.items():
            if k in self.SKIP_ON_JSON:
                pass
            elif k == "tags":
                obj["tags"] = ",".join(v)
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
                self.name = v.lower()
            elif k == "hostname":
                self.host = v
            elif k == "id":
                self._id = v
            elif k == "status":
                if v == "paused":
                    self.paused = True
                else:
                    self.paused = False
            elif k == "type" and type(k) is dict:
                self.type = v.keys()[0]
                for x, y in v[self.type].items():
                    setattr(self, x, y)
            else:
                setattr(self, k, v)

    def from_obj(self, obj):
        for k, v in obj.items():
            setattr(self, k, v)

    def fetch(self):
        res = self.api.send('get', "checks", self._id)['check']
        self.from_json(res)
