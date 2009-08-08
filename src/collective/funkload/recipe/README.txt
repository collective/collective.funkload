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
    ... recipe = collective.funkload
    ... url = 127.0.0.1:8080 
    ... """)


Running the buildout gives us::

    >>> print 'start\n', system(buildout) 
    start
    ...
    Generated script '/sample-buildout/bin/funkload'.
    
Test that the script contains our url

    >>> import os
    >>> script = os.path.join(sample_buildout,'bin','funkload')
    >>> print open(script,'r').read()
    #!...url="127.0.0.1:8080"...
    


Test without a url defined will fail.

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = test1
    ... index = http://pypi.python.org/simple
    ... [test1]
    ... recipe = collective.funkload
    ... """)

Running the buildout gives us:

    >>> print 'start\n', system(buildout) 
    start
    ...
    KeyError: 'You must specify an url to test'


