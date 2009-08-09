.. -*-doctest-*-

=============================================================
collective.funkload
=============================================================
Miscellaneous experimentation with and extensions to Funkload
-------------------------------------------------------------

``collective.funkload`` is a wrapper to `Funkload <http://pypi.python.org/pypi/funkload>`_, a web performance testing and reporting tool.

The scripts that Funkload installs generally require that they be
executed from the directory where the test modules live.  While this
is appropriate for generating test cases with the Funkload recorder,
it's often not the desirable behavior when recording benchmarking data
or generating reports.  Additionally, the argument handling for the
test and benchmark runners doesn't allow for specifying test modules
with dotted paths as one is often wont to do when working with
setuptools and eggs.

-------------------------
collective.funkload.bench
-------------------------

The collective.funkload package provides a wrapper around the Funkload
benchmark runner that handles dotted path arguments gracefully.
Specifically, rather than pass ``*.py`` file and TestCase.test_method
arguments, collective.funkload.bench.run() supports zope.testing
argument semantics for finding tests with "-s", "-m" and "-t".

    >>> from collective.funkload import bench
    >>> bench.run(defaults, (
    ...     'test.py -s foo -t test_foo '
    ...     '--cycles 1 --url http://bar.com').split())
    t...
    Benching FooTestCase.test_foo...
    * Server: http://bar.com...
    * Cycles: [1]...

------------------------
collective.funkload.diff
------------------------

The build-diffs console script will use "fl-build-report --diff" to
generate a differential report comparing the most recent benchmark
report against the previous report and against any available reports
from a day, a week, a month and a year ago.  When multiple reports are
available from the previous unit of time, the differential report will
be generated against the report closest to exactly that unit of time
in the past.

The diff module provides a function for parsing the date stamp from
a report filename.

    >>> from collective.funkload import diff
    >>> diff.parse_date(diff.report_re.match(
    ...     'test_foo-20081211T071242')).isoformat()
    '2008-12-11T07:12:42'

    >>> import os
    >>> sorted(os.listdir(reports_dir), reverse=True)
    ['test_foo-20081211T071242',
     'test_foo-20081211T071241',
     'test_foo-20081210T071243',
     'test_foo-20081210T071241',
     'test_foo-20081209T071242',
     'test_foo-20081205T071242',
     'test_foo-20081204T071242',
     'test_foo-20081203T071242',
     'test_foo-20081111T071242',
     'test_foo-20071211T071242',
     'test_baz-20081211T071243',
     'test_baz-20081211T071242',
     'test_bar-20081211T071242']

    >>> options, _ = diff.parser.parse_args(args=['-o', reports_dir])
    >>> diff.run(options)
    Creating diff report ...done: 
    file://.../reports/diff_foo-20081211T_071242_vs_071241/index.html
    Creating diff report ...done: 
    file://.../reports/diff_foo_20081211T071242_vs_20081210T071243/index.html
    Creating diff report ...done: 
    file://.../reports/diff_foo_20081211T071242_vs_20081204T071242/index.html
    Creating diff report ...done: 
    file://.../reports/diff_foo_20081211T071242_vs_20081111T071242/index.html
    Creating diff report ...done: 
    file://.../reports/diff_foo_20081211T071242_vs_20071211T071242/index.html
    Creating diff report ...done: 
    file://.../reports/diff_baz-20081211T_071243_vs_071242/index.html
