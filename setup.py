from setuptools import setup, find_packages
import os

version = '0.3'

setup(name='collective.funkload',
      version=version,
      description="Zope and Plone focussed extensions to funkload",
      long_description=open(os.path.join(
          "src", "collective", "funkload", "README.txt")).read() +
          "\n" + open(os.path.join(
          "src", "collective", "funkload", "labels.txt")).read() +
          "\n" + open(os.path.join("docs", "HISTORY.txt")).read(),
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
          'zope.testing>=3.6', # testrunner refactored
          'zope.pagetemplate',
      ],
      entry_points={
          'console_scripts': [
              'fl-run-bench = collective.funkload.bench:run',
              'fl-build-label-reports = collective.funkload.label:main',
              'fl-list = collective.funkload.report:main'],
          'zc.buildout': [
              'default = collective.funkload.recipe:TestRunner'],
          },
      test_suite='collective.funkload',
      )
