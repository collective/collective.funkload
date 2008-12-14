import unittest

from collective.funkload import testcase

class FooTestCase(testcase.FunkLoadTestCase):

    def test_foo(self):
        pass

def test_suite():
    return unittest.makeSuite(FooTestCase)

if __name__ in ('main', '__main__'):
    unittest.main(defaultTest='test_suite')
