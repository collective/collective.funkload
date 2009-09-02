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

The build-diffs console script is intended to make building HTML and
differential HTML report directories from existing bench result XML
files convenient.  It automatically builds HTML report directories
based on the bench result XML files specified or on all those present
in the directory if none are specified.  The bench result XML files
can also be selected relative to the current date.  The script can
also build differential HTML report directories for the specified
result XML files against other specified result XML files or against
all the result XML files for the same test.  This makes generating MxN
grids of differential HTML report directories quick and simple.
Finally, it generates a simple HTML index to the HTML report
directories and differentials generated.

For example, when investigating the relative performance merits of
several different configurations, start with an empty directory and
run fl-run-bench for each configuration.  Then run simply
"build-diffs" and the result XML files for each configuration will be
compared against the result XML files for every other configuration
for each test.

On the other hand, for generating continuous integration (such as with
buildbot) benchmarking where developers want to monitor benchmarks
compared to the last change, last week, last month and last year, the
result XML files and HTML report directories would be selected
relative to the current date.

The build-diffs script also only generates HTML report directories and
differentials if they haven't already been generated.

Both "-x" or "--x-axis" and "-y" or "--y-axis" options may be given
multiple times to select multiple result XML files or HTML report
directories.  Differential HTML report directories will be generated
for each result XML file or HTML report directory selected with the
"-x" or "--x-axis" options will be

Start with a directory with a number of benchmark result XML files.

    >>> import os
    >>> from collective.funkload.tests import tests
    >>> tests.setUpReports(reports_dir)
    >>> sorted(os.listdir(reports_dir), reverse=True)
    ['foo-bench-20081211T071242.xml',
     'foo-bench-20081211T071241.xml',
     'foo-bench-20081210T071243.xml',
     'foo-bench-20081210T071241.xml',
     'foo-bench-20081209T071242.xml',
     'foo-bench-20081205T071242.xml',
     'foo-bench-20081204T071242.xml',
     'foo-bench-20081203T071242.xml',
     'foo-bench-20081111T071242.xml',
     'foo-bench-20071211T071242.xml',
     'baz-bench-20081211T071243.xml',
     'baz-bench-20081211T071242.xml',
     'bar-bench-20081211T071242.xml']
 
Compare the most recent result XML files against HTML report
directories relative to the current date for one day ago, one week
ago, one month ago and 1 year ago.

    >>> from collective.funkload import diff
    >>> args='-d reports_dir -x latest -y 1 -y 7 -y 30 -y 365'
    >>> options, _ = diff.parser.parse_args(args=args.split())
    >>> diff.run(options)
    Creating html report ...done: 
    file://.../reports/test_foo-20081211T071242/index.html
    Creating html report ...done: 
    file://.../reports/test_foo-20081211T071241/index.html
    Creating html report ...done: 
    file://.../reports/test_foo-20081210T071243/index.html
    Creating html report ...done: 
    file://.../reports/test_foo-20081204T071242/index.html
    Creating html report ...done: 
    file://.../reports/test_foo-20081111T071242/index.html
    Creating html report ...done: 
    file://.../reports/test_foo-20071211T071242/index.html
    Creating html report ...done: 
    file://.../reports/test_baz-20081211T071243/index.html
    Creating html report ...done: 
    file://.../reports/test_baz-20081211T071242/index.html
    Creating html report ...done: 
    file://.../reports/test_bar-20081211T071242/index.html
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
    Creating report index ...done:
    file://.../reports/index.html

The report index renders a table with links to the HTML reports on the
X and Y axes and links to the differential reports in the table
cells.  In this case there's only one HTML report on the X axis and
four reports on the Y axis.

    >>> print open(os.path.join(reports_dir, 'index.html')).read()
    <...
    <h1>test_foo reports</h1>
    <table>
        <thead> <tr> <th></th> <th> <a
        href="test_foo-20081211T071242/index.html">test_foo-20081211T071242</a>
        </th> </tr> </thead>
        <tbody>
            <tr>
                <th> <a
                href="test_foo-20081211T071241/index.html">test_foo-20081211T071241</a>
                </th>
                <td> <a
                href="diff_foo-20081211T_071242_vs_071241/index.html">diff_foo-20081211T_071242_vs_071241</a>
                </td>
            </tr>
            <tr>
                <th> <a
                href="test_foo-20081210T071243/index.html">test_foo-20081210T071243</a>
                </th>
                <td> <a
                href="diff_foo_20081211T071242_vs_20081210T071243/index.html">diff_foo_20081211T071242_vs_20081210T071243</a>
                </td>
            </tr>
            <tr>
                <th> <a
                href="test_foo-20081204T071242/index.html">test_foo-20081204T071242</a>
                </th>
                <td> <a
                href="diff_foo_20081211T071242_vs_20081204T071242/index.html">diff_foo_20081211T071242_vs_20081204T071242</a>
                </td>
            </tr>
            <tr>
                <th> <a
                href="test_foo-20081111T071242/index.html">test_foo-20081111T071242</a>
                </th>
                <td> <a
                href="diff_foo_20081211T071242_vs_20081111T071242/index.html">diff_foo_20081211T071242_vs_20081111T071242</a>
                </td>
            </tr>
            <tr>
                <th> <a
                href="test_foo-20071211T071242/index.html">test_foo-20071211T071242</a>
                </th>
                <td> <a
                href="diff_foo_20081211T071242_vs_20071211T071242/index.html">diff_foo_20081211T071242_vs_20071211T071242</a>
                </td>
            </tr>
        </tbody>
        <tfooter> <tr> <th></th> <th> <a
        href="test_foo-20081211T071242/index.html">test_foo-20081211T071242</a>
        </th> </tr> </tfooter>
    </table>
    <h1>test_baz reports</h1>
    <table>
        <thead> <tr> <th></th> <th> <a
        href="test_baz-20081211T071243/index.html">test_baz-20081211T071243</a>
        </th> </tr> </thead>
        <tbody>
            <tr>
                <th> <a
                href="test_baz-20081211T071242/index.html">test_baz-20081211T071242</a>
                </th>
                <td> <a
                href="diff_baz-20081211T_071243_vs_071242/index.html">diff_baz-20081211T_071243_vs_071242</a>
                </td>
            </tr>
        </tbody>
        <tfooter> <tr> <th></th> <th> <a
        href="test_baz-20081211T071243/index.html">test_baz-20081211T071243</a>
        </th> </tr> </tfooter>
    </table>
    <h1>test_bar reports</h1>
    <table>
        <thead> <tr> <th></th> <th> <a
        href="test_bar-20081211T071242/index.html">test_bar-20081211T071242</a>
        </th> </tr> </thead>
        <tbody>
        </tbody>
        <tfooter> <tr> <th></th> <th> <a
        href="test_baz-20081211T071243/index.html">test_baz-20081211T071243</a>
        </th> </tr> </tfooter>
    </table>

Without any arguments, HTML report directories are generated for each
set of benchmark result XML files and differentials are generated
between each HTML report directory for the same test.  HTML report
directories and differentials are not generated if they already have
been.  All result XML files and HTML report directories are processed
sorted in reverse alphabetical order for consistent ordering by the
timestamp placing the most recent first.

    >>> tests.setUpReports(reports_dir)
    >>> args='-d reports_dir'
    >>> options, _ = diff.parser.parse_args(args=args.split())
    >>> diff.run(options)
    Creating html report ...done: 
    file://.../reports/test_foo-20081210T071241/index.html
    Creating html report ...done: 
    file://.../reports/test_foo-20081209T071242/index.html
    Creating html report ...done: 
    file://.../reports/test_foo-20081205T071242/index.html
    Creating html report ...done: 
    file://.../reports/test_foo-20081203T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071242_vs_20081210T071241/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071242_vs_20081209T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071242_vs_20081205T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071242_vs_20081203T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071241_vs_20081210T071243/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071241_vs_20081210T071241/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071241_vs_20081209T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071241_vs_20081205T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071241_vs_20081204T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071241_vs_20081203T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071241_vs_20081111T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081211T071241_vs_20071211T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071243_vs_20081210T071241/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071243_vs_20081209T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071243_vs_20081205T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071243_vs_20081204T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071243_vs_20081203T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071243_vs_20081111T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071243_vs_20071211T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071241_vs_20081209T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071241_vs_20081205T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071241_vs_20081204T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071241_vs_20081203T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071241_vs_20081111T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081210T071241_vs_20071211T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081209T071242_vs_20081205T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081209T071242_vs_20081204T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081209T071242_vs_20081203T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081209T071242_vs_20081111T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081209T071242_vs_20071211T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081205T071242_vs_20081204T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081205T071242_vs_20081203T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081205T071242_vs_20081111T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081205T071242_vs_20071211T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081204T071242_vs_20081203T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081204T071242_vs_20081111T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081204T071242_vs_20071211T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081203T071242_vs_20081111T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081203T071242_vs_20071211T071242/index.html
    Creating diff report ...done:
    file://.../reports/diff_foo_20081111T071242_vs_20071211T071242/index.html

The report index now includes all the reports on both axes for a
complete NxN grid.

    >>> print open(os.path.join(reports_dir, 'index.html')).read()
    <...
    <h1>test_foo reports</h1>
    <table>
        <thead> <tr>
            <th> <a
            href="test_foo-20081211T071242/index.html">test_foo-20081211T071242</a>
            </th>
            <th> <a
            href="test_foo-20081211T071241/index.html">test_foo-20081211T071241</a>
            </th>
            <th> <a
            href="test_foo-20081210T071243/index.html">test_foo-20081210T071243</a>
            </th>
            <th> <a
            href="test_foo-20081210T071241/index.html">test_foo-20081210T071241</a>
            </th>
            <th> <a
            href="test_foo-20081209T071242/index.html">test_foo-20081209T071242</a>
            </th>
            <th> <a
            href="test_foo-20081205T071242/index.html">test_foo-20081205T071242</a>
            </th>
            <th> <a
            href="test_foo-20081204T071242/index.html">test_foo-20081204T071242</a>
            </th>
            <th> <a
            href="test_foo-20081203T071242/index.html">test_foo-20081203T071242</a>
            </th>
            <th> <a
            href="test_foo-20081111T071242/index.html">test_foo-20081111T071242</a>
            </th>
            <th> <a
            href="test_foo-20071211T071242/index.html">test_foo-20071211T071242</a>
            </th>
        </tr> </thead>
        <tbody>
    test_foo-20081211T071242/index.html
    diff_foo-20081211T_071242_vs_071241/index.html
    diff_foo_20081211T071242_vs_20081210T071243/index.html
    diff_foo_20081211T071242_vs_20081210T071241/index.html
    diff_foo_20081211T071242_vs_20081209T071242/index.html
    diff_foo_20081211T071242_vs_20081205T071242/index.html
    diff_foo_20081211T071242_vs_20081204T071242/index.html
    diff_foo_20081211T071242_vs_20081203T071242/index.html
    diff_foo_20081211T071242_vs_20081111T071242/index.html
    diff_foo_20081211T071242_vs_20071211T071242/index.html
    test_foo-20081211T071241/index.html
    diff_foo-20081211T_071242_vs_071241/index.html
    diff_foo_20081211T071241_vs_20081210T071243/index.html
    diff_foo_20081211T071241_vs_20081210T071241/index.html
    diff_foo_20081211T071241_vs_20081209T071242/index.html
    diff_foo_20081211T071241_vs_20081205T071242/index.html
    diff_foo_20081211T071241_vs_20081204T071242/index.html
    diff_foo_20081211T071241_vs_20081203T071242/index.html
    diff_foo_20081211T071241_vs_20081111T071242/index.html
    diff_foo_20081211T071241_vs_20071211T071242/index.html
    test_foo-20081210T071243/index.html
    diff_foo-20081211T_071242_vs_071241/index.html
    diff_foo_20081211T071241_vs_20081210T071243/index.html
    diff_foo_20081210T071243_vs_20081210T071241/index.html
    diff_foo_20081210T071243_vs_20081209T071242/index.html
    diff_foo_20081210T071243_vs_20081205T071242/index.html
    diff_foo_20081210T071243_vs_20081204T071242/index.html
    diff_foo_20081210T071243_vs_20081203T071242/index.html
    diff_foo_20081210T071243_vs_20081111T071242/index.html
    diff_foo_20081210T071243_vs_20071211T071242/index.html
    test_foo-20081210T071241/index.html
    diff_foo-20081211T_071242_vs_071241/index.html
    diff_foo_20081211T071241_vs_20081210T071243/index.html
    diff_foo_20081210T071243_vs_20081210T071241/index.html
    diff_foo_20081210T071241_vs_20081209T071242/index.html
    diff_foo_20081210T071241_vs_20081205T071242/index.html
    diff_foo_20081210T071241_vs_20081204T071242/index.html
    diff_foo_20081210T071241_vs_20081203T071242/index.html
    diff_foo_20081210T071241_vs_20081111T071242/index.html
    diff_foo_20081210T071241_vs_20071211T071242/index.html
    test_foo-20081209T071242/index.html
    diff_foo-20081211T_071242_vs_071241/index.html
    diff_foo_20081211T071241_vs_20081210T071243/index.html
    diff_foo_20081210T071243_vs_20081210T071241/index.html
    diff_foo_20081210T071241_vs_20081209T071242/index.html
    diff_foo_20081209T071242_vs_20081205T071242/index.html
    diff_foo_20081209T071242_vs_20081204T071242/index.html
    diff_foo_20081209T071242_vs_20081203T071242/index.html
    diff_foo_20081209T071242_vs_20081111T071242/index.html
    diff_foo_20081209T071242_vs_20071211T071242/index.html
    test_foo-20081205T071242/index.html
    diff_foo-20081211T_071242_vs_071241/index.html
    diff_foo_20081211T071241_vs_20081210T071243/index.html
    diff_foo_20081210T071243_vs_20081210T071241/index.html
    diff_foo_20081210T071241_vs_20081209T071242/index.html
    diff_foo_20081209T071242_vs_20081205T071242/index.html
    diff_foo_20081205T071242_vs_20081204T071242/index.html
    diff_foo_20081205T071242_vs_20081203T071242/index.html
    diff_foo_20081205T071242_vs_20081111T071242/index.html
    diff_foo_20081205T071242_vs_20071211T071242/index.html
    test_foo-20081204T071242/index.html
    diff_foo-20081211T_071242_vs_071241/index.html
    diff_foo_20081211T071241_vs_20081210T071243/index.html
    diff_foo_20081210T071243_vs_20081210T071241/index.html
    diff_foo_20081210T071241_vs_20081209T071242/index.html
    diff_foo_20081209T071242_vs_20081205T071242/index.html
    diff_foo_20081205T071242_vs_20081204T071242/index.html
    diff_foo_20081204T071242_vs_20081203T071242/index.html
    diff_foo_20081204T071242_vs_20081111T071242/index.html
    diff_foo_20081204T071242_vs_20071211T071242/index.html
    test_foo-20081203T071242/index.html
    diff_foo-20081211T_071242_vs_071241/index.html
    diff_foo_20081211T071241_vs_20081210T071243/index.html
    diff_foo_20081210T071243_vs_20081210T071241/index.html
    diff_foo_20081210T071241_vs_20081209T071242/index.html
    diff_foo_20081209T071242_vs_20081205T071242/index.html
    diff_foo_20081205T071242_vs_20081204T071242/index.html
    diff_foo_20081204T071242_vs_20081203T071242/index.html
    diff_foo_20081203T071242_vs_20081111T071242/index.html
    diff_foo_20081203T071242_vs_20071211T071242/index.html
    test_foo-20081111T071242/index.html
    diff_foo-20081211T_071242_vs_071241/index.html
    diff_foo_20081211T071241_vs_20081210T071243/index.html
    diff_foo_20081210T071243_vs_20081210T071241/index.html
    diff_foo_20081210T071241_vs_20081209T071242/index.html
    diff_foo_20081209T071242_vs_20081205T071242/index.html
    diff_foo_20081205T071242_vs_20081204T071242/index.html
    diff_foo_20081204T071242_vs_20081203T071242/index.html
    diff_foo_20081203T071242_vs_20081111T071242/index.html
    diff_foo_20081111T071242_vs_20071211T071242/index.html
        </tbody>
        <tfooter> <tr>
            <th> <a
            href="test_foo-20081211T071242/index.html">test_foo-20081211T071242</a>
            </th>
            <th> <a
            href="test_foo-20081211T071241/index.html">test_foo-20081211T071241</a>
            </th>
            <th> <a
            href="test_foo-20081210T071243/index.html">test_foo-20081210T071243</a>
            </th>
            <th> <a
            href="test_foo-20081210T071241/index.html">test_foo-20081210T071241</a>
            </th>
            <th> <a
            href="test_foo-20081209T071242/index.html">test_foo-20081209T071242</a>
            </th>
            <th> <a
            href="test_foo-20081205T071242/index.html">test_foo-20081205T071242</a>
            </th>
            <th> <a
            href="test_foo-20081204T071242/index.html">test_foo-20081204T071242</a>
            </th>
            <th> <a
            href="test_foo-20081203T071242/index.html">test_foo-20081203T071242</a>
            </th>
            <th> <a
            href="test_foo-20081111T071242/index.html">test_foo-20081111T071242</a>
            </th>
            <th> <a
            href="test_foo-20071211T071242/index.html">test_foo-20071211T071242</a>
            </th>
        </tr> </tfooter>
    <h1>test_baz reports</h1>
    <table>
    test_baz-20081211T071243/index.html
    diff_baz-20081211T_071243_vs_071242/index.html
    test_baz-20081211T071242/index.html
    diff_baz-20081211T_071243_vs_071242/index.html
    </table>
    <h1>test_bar reports</h1>
    <table>
    test_bar-20081211T071242/index.html
    </table>

The diff module provides a function for parsing the date stamp from a
HTML report directory name.

    >>> diff.parse_date(diff.report_re.match(
    ...     'test_foo-20081211T071242')).isoformat()
    '2008-12-11T07:12:42'
