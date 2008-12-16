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

reports = ['test_bar-20081211T071242',
           'test_baz-20081211T071243',
           'test_baz-20081211T071242',
           'test_foo-20081211T071242',
           'test_foo-20081211T071241',
           'test_foo-20081210T071243',
           'test_foo-20081210T071241',
           'test_foo-20081209T071242',
           'test_foo-20081205T071242',
           'test_foo-20081204T071242',
           'test_foo-20081203T071242',
           'test_foo-20081111T071242',
           'test_foo-20071211T071242']

def setUpReports(test):
    test.globs['reports_dir'] = os.path.join(
        os.path.join(test.globs['tmp_dir'], 'reports'))
    os.mkdir(test.globs['reports_dir'])
    for report in reports:
        report_dir = os.path.join(test.globs['reports_dir'], report)
        os.mkdir(report_dir)
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), 'index.rst'),
            os.path.join(report_dir, 'index.rst'))

def setUp(test):
    tests.setUp(test)

    test.globs['tmp_dir'] = tempfile.mkdtemp()

    this_directory = os.path.split(__file__)[0]
    directory_with_tests = os.path.join(this_directory, 'src')
    test.globs['defaults'] = ['--path', directory_with_tests,
                              '--tests-pattern', '^sampletests$']

    setUpReports(test)

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
