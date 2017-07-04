# -*- coding: utf-8 -*-
"""Tests for the Check class."""

from __future__ import absolute_import

import json
import os
import unittest

from pypingdom import check


def mock_data(path):
    """Return json data for mocking."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    resource_file = os.path.join(dir_path, os.path.normpath('resources'), path.lstrip('/'))
    return open(resource_file, mode='r').read()


class CheckTestCase(unittest.TestCase):
    """Test cases for the Check class."""

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.checks = json.loads(mock_data('api/2.0/checks'))['checks']

    def test_check(self):
        """Test basic attributes."""
        acheck = check.Check(None, self.checks[0])
        self.assertEqual(acheck.name, self.checks[0]["name"])
        self.assertFalse("fubar" in acheck.tags)
        self.assertEqual(len(acheck.tags), len(self.checks[0]["tags"]))

    def test_check_notags(self):
        """Test that a check with no tags."""
        self.assertTrue("tags" not in self.checks[2])  # just to be sure ;-)
        acheck = check.Check(None, self.checks[2])
        self.assertTrue(isinstance(acheck.tags, list))
        self.assertEqual(len(acheck.tags), 0)
