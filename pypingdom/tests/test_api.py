"""Tests for the api class."""

import os
import unittest

import requests_mock

from pypingdom.api import Api


def fake_checks():
    """Return json data for mocking."""
    resource_file = os.path.normpath('pypingdom/tests/resources/api/2.0/checks')
    return open(resource_file, mode='r').read()


class ApiTestCase(unittest.TestCase):
    """Test cases for the api methods."""

    @requests_mock.Mocker()
    def test_request(self, m):
        """Test a simple request."""
        api = Api(username="testuser", password="testpass", apikey="mocked")
        m.request('get', api.base_url + "checks", text=fake_checks())
        res = api.send('get', "checks", params={"include_tags": True})
        self.assertTrue("checks" in res)
