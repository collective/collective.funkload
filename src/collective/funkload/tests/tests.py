import os
import unittest
from zope.testing import doctest
from zope.testing.testrunner import tests

from collective import funkload

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)

def setUp(test):
    tests.setUp(test)
    this_directory = os.path.split(__file__)[0]
    directory_with_tests = os.path.join(this_directory, 'src')
    test.globs['defaults'] = ['--path', directory_with_tests,
                              '--tests-pattern', '^sampletests$']

def tearDown(test):
    tests.tearDown(test)

def test_suite():
    return doctest.DocFileSuite(
        'README.txt',
        package=funkload,
        setUp=setUp, tearDown=tearDown,
        optionflags=optionflags)

additional_tests = test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
