# -*- coding: utf-8 -*-
from zc.recipe.egg import Scripts

class TestRunner(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        self.test_url = self.options.get('url')
        if not self.test_url:
            raise KeyError, "You must specify an address to test"


        options_funkload = {'eggs':'funkload\ncollective.funkload',
                            'scripts':'funkload',
                            'arguments':'url="%s",buildout_dir="%s"' % (self.test_url,self.buildout['buildout'].get('directory'))}
        
        self._recipe = Scripts(buildout,name,options_funkload)
        
        
        
#        python = options.get('python', buildout['buildout']['python'])
#        self.executable = buildout[python]['executable']


    def install(self):
        """Installer"""
        return self._recipe.install()

