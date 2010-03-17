# -*- coding: utf-8 -*-
"""%(test_name)s FunkLoad test"""

import unittest
from collective.funkload import testcase

class %(class_name)s(testcase.FLTestCase):
    """XXX

    This test use a configuration file %(class_name)s.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = self.conf_get('main', 'url')
        # XXX here you can setup the credential access like this
        # credential_host = self.conf_get('credential', 'host')
        # credential_port = self.conf_getInt('credential', 'port')
        # self.login, self.password = xmlrpc_get_credential(credential_host,
        #                                                   credential_port,
        # XXX replace with a valid group
        #                                                   'members')

    def test_%(test_name)s(self):
        # The description should be set in the configuration file
        server_url = self.server_url
        # begin of test ---------------------------------------------
%(script)s

        # end of test -----------------------------------------------

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")


def test_suite():
    return unittest.makeSuite(%(class_name)s)

additional_tests = test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')