#!/usr/sbin/env python
# -*- coding: utf-8 -*-
import yaml
import datetime

from six.moves import input

import pypingdom


with open('private_test_data.yml', 'r') as stream:
    auth = yaml.safe_load(stream)

client = pypingdom.Client(username=auth['username'],
                          password=auth['password'],
                          apikey=auth['apikey'],
                          email=auth['email'])

check_definition = {
    'name': 'Ansible integration test',
    'paused': True,
    # 'alert_policy': '',
    'type': 'http',
    'host': 'www.google.com',
    'url': '/',
    'requestheaders': {
        'XCustom': 'my header value'
    },
    'tags': ['pypingdom-test', 'custom-tag'],
    'encryption': False
}


def clean():
    global client, check_definition
    checks = client.get_checks(filters={'tags': ['pypingdom-test']})
    for check in checks:
        print('deleting check %s' % check.name)  # noqa: T001
        client.delete_check(check)
    checks = client.get_checks(filters={'tags': ['pypingdom-test']})
    print(checks)  # noqa: T001
    assert checks == []  # noqa: S101


def create_check():
    global client, check_definition
    c = client.create_check(check_definition)
    print('created %s' % c.name)  # noqa: T001
    check = client.get_check(check_definition['name'])
    assert check is not None  # noqa: S101


def update_check():
    global client, check_definition
    check = client.get_check(check_definition['name'])
    print('updating check %s' % check.name)  # noqa: T001
    newcheck = client.update_check(check, {'requestheaders': {'XCustom': 'new header value'}})
    assert newcheck.requestheaders['XCustom'] == 'new header value'  # noqa: S101


def delete_check():
    global client, check_definition
    check = client.get_check(check_definition['name'])
    print('deleting check %s' % check.name)  # noqa: T001
    client.delete_check(check)
    check = client.get_check(check_definition['name'])
    assert check is None  # noqa: S101


def create_maintenance():
    global client, check_definition
    check = client.get_check(check_definition['name'])
    start = datetime.datetime.now() + datetime.timedelta(days=2)
    stop = start + datetime.timedelta(minutes=20)
    print('creating maintenance for check %s' % check.name)
    window = client.create_maintenance({
        'checks': [check],
        'name': 'pypyngdom test maintenance',
        'start': start,
        'stop': stop
    })
    return window


def delete_maintenance(mid):
    check = client.get_check(check_definition['name'])
    for m in client.get_maintenances(filters={'checks': [check]}):
        print('deleting maintenance %s' % m.name)  # noqa: T001
        client.delete_maintenance(m)


create_check()
input('Continue?')
update_check()
input('Continue?')
create_maintenance()
input('Continue?')
delete_maintenance()
input('Continue?')
delete_check()
