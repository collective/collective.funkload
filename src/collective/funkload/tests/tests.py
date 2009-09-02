import os
import unittest
import tempfile
import shutil

from zope.testing import doctest
from zope.testing.testrunner import tests

from collective import funkload

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)

def setUp(test):
    tests.setUp(test)

    test.globs['tmp_dir'] = tempfile.mkdtemp()

    this_directory = os.path.split(__file__)[0]
    directory_with_tests = os.path.join(this_directory, 'src')
    test.globs['defaults'] = ['--path', directory_with_tests,
                              '--tests-pattern', '^sampletests$']
    test.globs['reports_dir'] = os.path.join(
        os.path.join(test.globs['tmp_dir'], 'reports'))

def tearDown(test):
    shutil.rmtree(test.globs['tmp_dir'])
    tests.tearDown(test)

def test_suite():
    return doctest.DocFileSuite(
        'README.txt',
        'labels.txt',
        package=funkload,
        setUp=setUp, tearDown=tearDown,
        optionflags=optionflags)

additional_tests = test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
