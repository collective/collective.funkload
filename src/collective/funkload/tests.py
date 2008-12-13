import unittest
from zope.testing import doctest

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)

def test_suite():
    return doctest.DocFileSuite(
        'README.txt',
        optionflags=optionflags)

additional_tests = test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
