#!/usr/sbin/env python
import yaml
import sys
import datetime
sys.path.append("../pypingdom")
import pypingdom

with open("private_test_data.yml", 'r') as stream:
    auth = yaml.load(stream)

client = pypingdom.Client(username=auth["username"],
                          password=auth["password"],
                          apikey=auth["apikey"],
                          email=auth["email"])

check_definition = {
    "name": "Ansible integration test",
    "paused": True,
    #"alert_policy": "",
    "type": "http",
    "host": "www.google.com",
    "url": "/",
    "requestheaders": {
        'XCustom': 'my header value'
    },
    "tags": ["pypingdom-test", "custom-tag"],
    "encryption": False
}


def clean():
    global client, check_definition
    checks = client.get_checks(filters={"tags": ["pypingdom-test"]})
    for check in checks:
        print("deleting check %s" % check.name)
        client.delete_check(check)
    checks = client.get_checks(filters={"tags": ["pypingdom-test"]})
    print(checks)
    assert checks == []


def create_check():
    global client, check_definition
    c = client.create_check(check_definition["name"], check_definition)
    print("created %s" % c.name)
    check = client.get_check(check_definition["name"])
    assert check is not None


def update_check():
    global client, check_definition
    check = client.get_check(check_definition["name"])
    print("updating check %s" % check.name)
    newcheck = client.update_check(check, {"requestheaders": {'XCustom': 'new header value'}})
    assert newcheck.requestheaders["XCustom"] == 'new header value'


def delete_check():
    global client, check_definition
    check = client.get_check(check_definition["name"])
    print("deleting check %s" % check.name)
    client.delete_check(check)
    check = client.get_check(check_definition["name"])
    assert check is None


def create_maintenance():
    global client, check_definition
    start = datetime.datetime.now() + datetime.timedelta(minutes=10)
    stop = start + datetime.timedelta(minutes=20)
    print("creating maintenance for check %s" % check_definition["name"])
    mid = client.create_maintenance(description="pypyngdom test maintenance",
                                    start=start,
                                    stop=stop,
                                    check_names=[check_definition["name"]])
    return mid


def delete_maintenance(mid):
    client.delete_maintenance(mid)


create_check()
raw_input("Continue?")
update_check()
raw_input("Continue?")
mid = create_maintenance()
raw_input("Continue?")
delete_maintenance(mid)
raw_input("Continue?")
delete_check()
