# -*- coding: utf-8 -*-
from zc.recipe.egg import Scripts
import os

class TestRunner(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        self.test_url = self.options.get('url')
        if not self.test_url:
            raise KeyError, "You must specify an url to test"

        default_location = os.path.join(self.buildout['buildout'].get('directory'),'var','funkload')
        self.location = self.options.get('location',default_location)


        options_funkload = {'eggs':'funkload\ncollective.funkload',
                            'scripts':'funkload',
                            'initialization':"import os;os.chdir('%s')" % (self.location),
                            'arguments':'url="%s",buildout_dir="%s"' % (self.test_url,self.buildout['buildout'].get('directory'))}

        if 'python' in options:
            options_funkload.update({'python':options['python']})
        
        self._recipe = Scripts(buildout,name,options_funkload)


    def install(self):
        """Installer"""
        
        if not os.path.exists(self.location):
            os.makedirs(self.location)
        
        return self._recipe.install()

