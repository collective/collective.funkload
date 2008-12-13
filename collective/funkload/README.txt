.. -*-doctest-*-

=============================================================
collective.funkload
=============================================================
Miscellaneous experimentation with and extensions to Funkload
-------------------------------------------------------------

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
Specifically, rather than pass *.py file and TestCase.test_method
arguments, collective.funkload.bench.run() supports zope.testing
argument semantics for finding tests with "-s", "-m" and "-t".

    >>> from collective.funkload import bench
    >>> bench.run(
    ...     ['-s', 'foo.tests.test_foo', '-t', 'test_foo'])
    =...
    Benching Foo.test_foo...
