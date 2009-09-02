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
