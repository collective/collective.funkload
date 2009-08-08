# -*- coding: utf-8 -*-
from zc.recipe.egg import Scripts
import os
import stat

from script_template import SCRIPT_TEMPLATE

class TestRunner(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        self._recipes = []

        options_funkload = options.copy()
        if 'initialization' in options_funkload:
            del options_funkload['initialization']
        if 'python' in options_funkload:
            del options_funkload['python']
        options_funkload['eggs'] = 'funkload\ncollective.funkload'
        self._recipes.append(Scripts(buildout,name,options_funkload))
        
        test_address = self.options.get('address')
        if not test_address:
            if 'instance' in self.buildout:
                test_address = self.buildout['instance'].get('http-address')
        if not test_address:
            raise KeyError, "You must specify an address to test"
                
        self.test_address = test_address
        self.filename = self.options.get('filename','funkload')
        python = options.get('python', buildout['buildout']['python'])
        self.executable = buildout[python]['executable']
        
                
    def install(self):
        """Installer"""
        result = []
        for recipe in self._recipes:
            result.extend(recipe.install())
        
        bin_dir = self.buildout["buildout"]["bin-directory"]
        script = SCRIPT_TEMPLATE % {'bin_directory':bin_dir,"test_address":self.test_address}
        script_path = os.path.join(bin_dir,self.filename)

        result.append(script_path)
        fd = open(script_path,'w')
        fd.write(script)
        fd.close
        os.chmod(script_path,stat.S_IRWXU)
        
        print "Generated script '%s'." % (script_path)
        
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple(result)

 #   def update(self):
 #       """Updater"""
 #       for recipe in self._recipes:
 #           recipe.update()
