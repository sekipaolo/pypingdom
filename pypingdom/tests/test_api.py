# -*- coding: utf-8 -*-
"""Tests for the api class."""

from __future__ import absolute_import

import os
import unittest

import requests_mock

from pypingdom.api import Api


def mock_data(path):
    """Return json data for mocking."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    resource_file = os.path.join(dir_path, os.path.normpath('resources'), path.lstrip('/'))
    return open(resource_file, mode='r').read()


class ApiTestCase(unittest.TestCase):
    """Test cases for the api methods."""

    @requests_mock.Mocker()
    def test_request(self, m):
        """Test a simple request."""
        api = Api(username='testuser', password='testpass', apikey='mocked')  # noqa: S106
        m.request('get', api.base_url + 'checks', text=mock_data('/api/2.0/checks'))
        res = api.send('get', 'checks', params={'include_tags': True})
        self.assertTrue('checks' in res)
