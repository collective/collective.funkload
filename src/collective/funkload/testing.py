"""collective.funkload.testing"""

import os
import shutil

from collective.funkload import report

reports = [
    dict(name='read', stamp='20081211T071242',
         time='2008-12-11T07:12:42.000000',
         test='test_read', class_='FooTestCase',
         module='foo.sampletests', label='python-2.4'),
    dict(name='read', stamp='20081211T071241',
         time='2008-12-11T07:12:41.000000',
         test='test_read', class_='FooTestCase',
         module='foo.sampletests', label='python-2.6'),
    dict(name='read', stamp='20081210T071243',
         time='2008-12-10T07:12:43.000000',
         test='test_read', class_='FooTestCase',
         module='foo.sampletests', label='python-2.4'),
    dict(name='read', stamp='20081210T071241',
         time='2008-12-10T07:12:41.000000',
         test='test_read', class_='FooTestCase',
         module='foo.sampletests', label='python-2.5'),
    dict(name='add', stamp='20081211T071243',
         time='2008-12-11T07:12:43.000000',
         test='test_add', class_='FooTestCase',
         module='foo.sampletests', label='python-2.4'),
    dict(name='add', stamp='20081211T071242',
         time='2008-12-11T07:12:42.000000',
         test='test_add', class_='FooTestCase',
         module='foo.sampletests', label='python-2.6'),
    dict(name='write', stamp='20081211T071242',
         time='2008-12-11T07:12:42.000000',
         test='test_write', class_='FooTestCase',
         module='foo.sampletests', label='')]

bench_tmpl = open(os.path.join(
    os.path.dirname(__file__), 'tests', 'bench.xml')).read()

def setUpReports(reports_dir):
    if os.path.isdir(reports_dir):
        shutil.rmtree(reports_dir)
    os.mkdir(reports_dir)
    for report_d in reports:
        report_d['path'] = os.path.join(
            reports_dir, '%(name)s-bench-%(stamp)s.xml' % report_d)
        open(report_d['path'], 'w').write(
            bench_tmpl % report_d)
        open(os.path.join(
            reports_dir, '%(name)s-bench-%(stamp)s.log' % report_d),
            'w').write('')

def listReports(reports_dir):
    return sorted(
        (label, sorted(
            (test, sorted(times[0].iteritems(), reverse=True))
            for test, times in tests.iteritems()))
        for label, tests in
        report.results_by_label(reports_dir).iteritems())
