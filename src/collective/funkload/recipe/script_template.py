SCRIPT_TEMPLATE = '''#!/Library/Frameworks/Python.framework/Versions/Current/bin/python
import sys
import os

TEST_URL = "%(test_address)s"
BIN_DIRECTORY = "%(bin_directory)s"

class FunkloadWrapper(object):
    
    def _usage(self):
        """ Print usage """
        print "Usage"
        for method in self._getActions():
            method = getattr(self,method)
            print str(method.__name__) + ": " + str(method.__doc__)
    
    def _getActions(self):
        return [x for x in dir(self) if not x.startswith('_')]
    
    def _dispatch(self):
        args = sys.argv
        actions = self._getActions()
        try:
            action = args[1]
        except IndexError:
            action = None
        
        
        if action and action in actions:
            action = getattr(self,action)
            action(args)
        else:
            self._usage()
          
    
    def _runscript(self,name,args=None):
        cmdargs = ' '.join(sys.argv[2:])

        if args is None:
            args = ''

        os.system(os.path.join(BIN_DIRECTORY,name) + " " + args + " " + cmdargs)
        
    def test(self,args):
        """ Launch a FunkLoad unit test. """
        self._runscript('fl-run-test',' --url ' + TEST_URL)
    
    def bench(self,args):
        """ Launch a FunkLoad unit test as load test. """
        self._runscript('fl-run-bench')
    

if __name__ == '__main__':
    wrapper = FunkloadWrapper()
    wrapper._dispatch()
'''
