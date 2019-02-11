# -*- coding: utf-8 -*-
"""Tests for the client class."""

from __future__ import absolute_import

import os
import unittest

import requests_mock

from pypingdom import Client
from pypingdom.check import Check


def mock_data(path):
    """Return json data for mocking."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    resource_file = os.path.join(dir_path, os.path.normpath('resources'), path.lstrip('/'))
    return open(resource_file, mode='r').read()


class ClientTestCase(unittest.TestCase):
    """Test cases for the client methods."""

    @requests_mock.Mocker()
    def test_request(self, m):
        """Test a simple request."""
        base_url = 'https://api.pingdom.com'
        fakepath = '/api/2.0/checks'
        m.request('get', base_url + fakepath, text=mock_data(fakepath))
        fakepath = '/api/2.0/servertime'
        m.request('get', base_url + fakepath, text=mock_data(fakepath))
        fakepath = '/api/2.0/summary.outage/85975'
        m.request('get', base_url + fakepath, text=mock_data(fakepath))

        client = Client(username='username',  # noqa: S106
                        password='password',
                        apikey='apikey',
                        email='email')

        res = client.get_checks()
        self.assertEqual(len(res), 3)
        self.assertTrue(all(isinstance(x, Check) for x in res))
        check1 = client.get_check(name='My check 1')
        self.assertNotEqual(check1, None)
        check2 = client.get_check(name='My check 2')
        self.assertNotEqual(check1, check2)

        res = client.servertime()
        self.assertEqual(res, 1294237910)

        res = client.get_summary_outage('85975')
        self.assertTrue('summary' in res)
        self.assertTrue('states' in res['summary'])

    @requests_mock.Mocker()
    def test_get_checks(self, m):
        """Test a simple request."""
        base_url = 'https://api.pingdom.com'
        fakepath = '/api/2.0/checks'
        m.request('get', base_url + fakepath, text=mock_data(fakepath))

        client = Client(username='username',  # noqa: S106
                        password='password',
                        apikey='apikey',
                        email='email')

        res = client.get_checks()
        self.assertEqual(len(res), 3)
        self.assertTrue(all(isinstance(x, Check) for x in res))

        res = client.get_checks(filters={'tags': ['apache']})
        self.assertEqual(len(res), 1)
