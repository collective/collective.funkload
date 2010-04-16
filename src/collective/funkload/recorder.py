import os
from funkload.utils import trace
from funkload import Recorder

class RecorderProgram(Recorder.RecorderProgram):
    """
    Custom version of RecorderProgram to make usage of 
    of our custom Script tpl.
    """
    def writeScript(self, script):
        """Write the FunkLoad test script."""
        from pkg_resources import resource_string
         
        tpl_name = 'data/ScriptTestCase.tpl' 
        trace('Creating script: %s.\n' % self.script_path)
        tpl = resource_string('collective.funkload', tpl_name)
        content = tpl % {'script': script, 
                         'test_name': self.test_name, 
                         'class_name': self.class_name}

        if os.path.exists(self.script_path): 
            trace("Error file %s already exists.\n" % self.script_path) 
            return 
        f = open(self.script_path, 'w') 
        f.write(content) 
        f.close()

