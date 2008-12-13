##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""A few built-in recipes

$Id: __init__.py 90185 2008-08-25 11:17:33Z icemac $
"""

# Copied from zc.recipe.testrunner

import os
import pkg_resources
import zc.buildout.easy_install

class TestRunner:

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        options['script'] = os.path.join(buildout['buildout']['bin-directory'],
                                         options.get('script', self.name),
                                         )
        if not options.get('working-directory', ''):
            options['location'] = os.path.join(
                buildout['buildout']['parts-directory'], name)
        self.egg = zc.recipe.egg.Egg(buildout, name, options)

    def install(self):
        options = self.options
        dest = []
        eggs, ws = self.egg.working_set(('collective.funkload', ))

        test_paths = [ws.find(pkg_resources.Requirement.parse(spec)).location
                      for spec in eggs]

        defaults = options.get('defaults', '').strip()
        if defaults:
            defaults = '(%s) + ' % defaults

        wd = options.get('working-directory', '')
        if not wd:
            wd = options['location']
            if os.path.exists(wd):
                assert os.path.isdir(wd)
            else:
                os.mkdir(wd)
            dest.append(wd)
        wd = os.path.abspath(wd)
        initialization = initialization_template % wd

        env_section = options.get('environment', '').strip()
        if env_section:
            env = self.buildout[env_section]
            for key, value in env.items():
                initialization += env_template % (key, value)

        initialization_section = options.get('initialization', '').strip()
        if initialization_section:
            initialization += initialization_section

        dest.extend(zc.buildout.easy_install.scripts(
            [(options['script'], 'collective.funkload.bench', 'run')],
            ws, options['executable'],
            self.buildout['buildout']['bin-directory'],
            extra_paths=self.egg.extra_paths,
            arguments = defaults + (arg_template % dict(
                TESTPATH=repr(test_paths)[1:-1].replace(
                               ', ', ",\n  '--test-path', "),
                )),
            initialization = initialization,
            ))

        return dest

    update = install

arg_template = """[
  '--test-path', %(TESTPATH)s,
  ]"""

initialization_template = """import os
sys.argv[0] = os.path.abspath(sys.argv[0])
os.chdir(%r)
"""

env_template = """os.environ['%s'] = %r
"""
