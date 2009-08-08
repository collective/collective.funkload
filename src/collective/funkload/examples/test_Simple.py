# -*- coding: iso-8859-15 -*-
"""simple FunkLoad test

$Id: $
"""
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from collective.funkload import testcase

class Simple(testcase.FLTestCase):
    """XXX

    This test use a configuration file Simple.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')

    def test_simple(self):
        server_url = self.server_url
        self.get("http://teamrubber.com/",
            description="visit Team Rubber")

    def test_complex(self):
        server_url = self.server_url
        self.get("http://plone.org/",
            description="Visit plone.org")


        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

def test_suite():
    return unittest.makeSuite(Simple)


if __name__ in ('main', '__main__'):
    unittest.main()
