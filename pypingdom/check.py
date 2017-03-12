from maintenance import Maintenance


class Check(object):

    def __init__(self, client, name, obj=False):
        self.client = client
        self.name = name
        if obj:
            self.from_json(obj)
        else:
            self.fetch()

    def __repr__(self):
        vals =["{0}: '{1}'".format(k, v) for k, v in self.__dict__.items()]
        return "pingdom.Check:\n\t{0}".format("\n\t".join(vals))

    def from_json(self, obj):
        for k, v in obj.items():
            if k == "id":
                self._id = str(obj['id'])
            elif k in ['tags', "contactids"]:
                setattr(self, k, v.split(","))
            else:
                setattr(self, k, v)

    def to_json(self):
        obj = {}
        for k, v in self.__dict__.items():
            if k in ['tags', "contactids"]:
                obj[k] = ",".join(v)
            elif k == "hostname":
                obj['host'] = v
            elif k in ["alert_policy_name", "client", "status", "_id", "lasttesttime", "lastresponsetime", "lasterrortime", "created", "type"]:
                pass
            else:
                obj[k] = v
        return obj

    def fetch(self):
        for item in self.client.send('get', "checks")['checks']:
            if item['name'] == self.name:
                self.from_json(item)

    def create(self):
        data = self.to_json()
        data['type'] = self.type
        self.client.send(method='post', resource='checks', data=data)
        self.fetch()

    def modify(self):
        self.client.send(method='put', resource='checks', resource_id=self._id, data=self.to_json())
        self.fetch()

    def unpause(self):
        self.paused = "false"
        self.modify()

    def pause(self):
        self.paused = "true"
        self.modify()

    def delete(self):
        if not self._id:
            raise "CheckNotFound"
        self.client.send(method='delete', resource='checks', resource_id=self._id)

    def create_maintenance(self, description, start, stop):
        m = Maintenance(self.client.username, self.client.password)
        m.create(description, start, stop, [self._id])
