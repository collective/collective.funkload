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

reports = ['bar-bench-20081211T071242.xml',
           'baz-bench-20081211T071243.xml',
           'baz-bench-20081211T071242.xml',
           'foo-bench-20081211T071242.xml',
           'foo-bench-20081211T071241.xml',
           'foo-bench-20081210T071243.xml',
           'foo-bench-20081210T071241.xml',
           'foo-bench-20081209T071242.xml',
           'foo-bench-20081205T071242.xml',
           'foo-bench-20081204T071242.xml',
           'foo-bench-20081203T071242.xml',
           'foo-bench-20081111T071242.xml',
           'foo-bench-20071211T071242.xml']

def setUpReports(reports_dir):
    if os.path.isdir(reports_dir):
        shutil.rmtree(reports_dir)
    os.mkdir(reports_dir)
    for report in reports:
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), 'bench.xml'),
            os.path.join(reports_dir, report))

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
        package=funkload,
        setUp=setUp, tearDown=tearDown,
        optionflags=optionflags)

additional_tests = test_suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
