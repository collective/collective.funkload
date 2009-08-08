Supported options
=================



Example usage
=============

.. Note to recipe author!
   ----------------------
   zc.buildout provides a nice testing environment which makes it
   relatively easy to write doctests that both demonstrate the use of
   the recipe and test it.
   You can find examples of recipe doctests from the PyPI, e.g.
   
     http://pypi.python.org/pypi/zc.recipe.egg

   The PyPI page for zc.buildout contains documentation about the test
   environment.

     http://pypi.python.org/pypi/zc.buildout#testing-support

   Below is a skeleton doctest that you can start with when building
   your own tests.

Test with a url defined

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = test1
    ... index = http://pypi.python.org/simple
    ... [test1]
    ... recipe = collective.recipe.funkload
    ... address = 127.0.0.1:8080 
    ... """)


Running the buildout gives us::

    >>> print 'start\n', system(buildout) 
    start
    ...
    Generated script '/sample-buildout/bin/fl-credential-ctl'.
    Generated script '/sample-buildout/bin/fl-run-test'.
    Generated script '/sample-buildout/bin/fl-record'.
    Generated script '/sample-buildout/bin/fl-run-bench'.
    Generated script '/sample-buildout/bin/fl-monitor-ctl'.
    Generated script '/sample-buildout/bin/fl-install-demo'.
    Generated script '/sample-buildout/bin/fl-build-report'.
    Generated script '/sample-buildout/bin/funkload'.
    
Test that the script contains our url

    >>> import os
    >>> script = os.path.join(sample_buildout,'bin','funkload')
    >>> print open(script,'r').read()
    #!...TEST_URL = "127.0.0.1:8080"...
    


Test without a url defined (it will automatically be taken from a section called instance)

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = test1
    ... index = http://pypi.python.org/simple
    ... [test1]
    ... recipe = collective.recipe.funkload
    ... [instance]
    ... http-address = 192.168.1.100:8080
    ... """)

Running the buildout gives us:

    >>> print 'start\n', system(buildout) 
    start
    ...
    Generated script '/sample-buildout/bin/fl-credential-ctl'.
    Generated script '/sample-buildout/bin/fl-run-test'.
    Generated script '/sample-buildout/bin/fl-record'.
    Generated script '/sample-buildout/bin/fl-run-bench'.
    Generated script '/sample-buildout/bin/fl-monitor-ctl'.
    Generated script '/sample-buildout/bin/fl-install-demo'.
    Generated script '/sample-buildout/bin/fl-build-report'.
    Generated script '/sample-buildout/bin/funkload'.

Test that the script contains our url

    >>> import os
    >>> script = os.path.join(sample_buildout,'bin','funkload')
    >>> print open(script,'r').read()
    #!...TEST_URL = "192.168.1.100:8080"...



Test without a url defined (it will automatically be taken from a section called instance)

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = test1
    ... index = http://pypi.python.org/simple
    ... [test1]
    ... recipe = collective.recipe.funkload
    ... """)

Running the buildout gives us:

    >>> print 'start', system(buildout) 
    start...
    
    ...You must specify an address to test...

