"""Tests for the client class."""

from __future__ import absolute_import

import os
import unittest

import requests_mock

from pypingdom import Client
from pypingdom.check import Check


def mock_data(path):
    """Return json data for mocking."""
    resource_file = os.path.join(os.path.normpath('pypingdom/tests/resources'), path.lstrip('/'))
    return open(resource_file, mode='r').read()


class ClientTestCase(unittest.TestCase):
    """Test cases for the client methods."""

    @requests_mock.Mocker()
    def test_request(self, m):
        """Test a simple request."""
        base_url = "https://api.pingdom.com"
        fakepath = "/api/2.0/checks"
        m.request('get', base_url + fakepath, text=mock_data(fakepath))
        fakepath = "/api/2.0/servertime"
        m.request('get', base_url + fakepath, text=mock_data(fakepath))

        client = Client(username="username",
                        password="password",
                        apikey="apikey",
                        email="email")

        res = client.get_checks()
        self.assertEqual(len(res), 3)
        self.assertTrue(all(isinstance(x, Check) for x in res))
        check1 = client.get_check(name="My check 1")
        self.assertNotEqual(check1, None)
        check2 = client.get_check(name="My check 2")
        self.assertNotEqual(check1, check2)

        res = client.servertime()
        self.assertEqual(res, 1294237910)
