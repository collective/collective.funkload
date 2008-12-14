from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='collective.funkload',
      version=version,
      description="Miscellaneous experimentation with and extensions to Funkload",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ross Patterson',
      author_email='me@rpatterson.net',
      url='http://pypi.python.org/pypi/collective.funkload',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir = {'':'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'funkload',
          'zope.testing',
      ],
      entry_points={
          'console_scripts': [
              'fl-run-bench = collective.funkload.bench:run'],
          'zc.buildout': [
              'default = collective.funkload.recipe:TestRunner'],
          },
      test_suite='collective.funkload',
      )