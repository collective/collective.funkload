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

reports = [
    dict(name='bar', stamp='20081211T071242',
         time='2008-12-11T07:12:42.000000',
         test='test_bar', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='baz', stamp='20081211T071243',
         time='2008-12-11T07:12:43.000000',
         test='test_baz', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='baz', stamp='20081211T071242',
         time='2008-12-11T07:12:42.000000',
         test='test_baz', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='foo', stamp='20081211T071242',
         time='2008-12-11T07:12:42.000000',
         test='test_foo', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='foo', stamp='20081211T071241',
         time='2008-12-11T07:12:41.000000',
         test='test_foo', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='foo', stamp='20081210T071243',
         time='2008-12-10T07:12:43.000000',
         test='test_foo', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='foo', stamp='20081210T071241',
         time='2008-12-10T07:12:41.000000',
         test='test_foo', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='foo', stamp='20081209T071242',
         time='2008-12-09T07:12:42.000000',
         test='test_foo', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='foo', stamp='20081205T071242',
         time='2008-12-05T07:12:42.000000',
         test='test_foo', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='foo', stamp='20081204T071242',
         time='2008-12-04T07:12:42.000000',
         test='test_foo', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='foo', stamp='20081203T071242',
         time='2008-12-03T07:12:42.000000',
         test='test_foo', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='foo', stamp='20081111T071242',
         time='2008-11-11T07:12:42.000000',
         test='test_foo', class_='FooTestCase',
         module='foo.sampletests'),
    dict(name='foo', stamp='20071211T071242',
         time='2007-12-11T07:12:42.000000',
         test='test_foo', class_='FooTestCase',
         module='foo.sampletests')]

bench_tmpl = open(
    os.path.join(os.path.dirname(__file__), 'bench.xml')).read()

def setUpReports(reports_dir):
    if os.path.isdir(reports_dir):
        shutil.rmtree(reports_dir)
    os.mkdir(reports_dir)
    for report in reports:
        report['path'] = os.path.join(
            reports_dir, '%(name)s-bench-%(stamp)s.xml' % report)
        open(report['path'], 'w').write(
            bench_tmpl % report)

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
