import datetime
import time


class Maintenance(object):

    def __init__(self, client, json=False, obj=False):
        self.client = client
        self._id = False
        if json:
            self.from_json(json)
        elif obj:
            self.from_obj(obj)
        else:
            raise "Missing definition: use json or obj parameter"

    def __repr__(self):
        checks = []
        for check in self.checks:
            if check:
                checks.append(check.name)
            else:
                checks.append("<deleted check>")
        return """
        pingdom.Maintenance <{0}>
         name: {1}
         start: {2}
         end: {3}
         checks: {4}
        """.format(self._id,
                   self.name,
                   self.start,
                   self.stop,
                   ", ".join(checks))

    def to_json(self):
        check_ids = [str(check._id) for check in self.checks]
        data = {
            # "__csrf_magic": "",
            # "id": "",
            "description": self.name,
            "from-date": "{0}.{1}.{2}.".format(self.start.year, self.start.month, self.start.day),
            "from-time": "{0}:{1}".format(self.start.hour, self.start.minute),
            "to-date": "{0}.{1}.{2}.".format(self.stop.year, self.stop.month, self.stop.day),
            "to-time": "{0}:{1}".format(self.stop.hour, self.stop.minute),
            "start": int(time.mktime(self.start.timetuple())),
            "end": int(time.mktime(self.stop.timetuple())),
            "checks": "[{0}]".format(",".join(check_ids))
        }
        return data

    def from_json(self, obj):
        self._id = int(obj['id'])
        self.name = obj["description"]
        self.start = datetime.datetime.fromtimestamp(obj['start'])
        self.stop = datetime.datetime.fromtimestamp(obj['end'])
        self.checks = [self.client.get_check(_id=int(x['compound_id'])) for x in obj['checks']]

    def from_obj(self, obj):
        self.name = obj["name"]
        self.start = obj['start']
        self.stop = obj['stop']
        self.checks = obj['checks']
