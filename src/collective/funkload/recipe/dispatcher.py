
import sys
import collective.funkload.bench
import zope.testing.testrunner

class FunkloadWrapper(object):
    
    def __init__(self,url,buildout_dir):
        self._url = url
        self._dir = buildout_dir
    
    def _usage(self):
        """ Print usage """
        print "Usage"
        for method in self._getActions():
            method = getattr(self,method)
            print str(method.__name__) + ": " + str(method.__doc__)
    
    def _getActions(self):
        return [x for x in dir(self) if not x.startswith('_')]
    
    def _dispatch(self):
        self._args = sys.argv
        actions = self._getActions()
        try:
            action = self._args[1]
        except IndexError:
            action = None
        
        
        if action and action in actions:
            test_path = ['--test-path=%s' % (path) for path in sys.path if path.startswith(self._dir)]
            fl_args = [self._args[0]] + test_path + ['--url=%s' % self._url] +  self._args[2:]
            
            sys.argv = fl_args
            
            action = getattr(self,action)
            action()
        else:
            self._usage()
          
        
    def test(self):
        """ Launch a FunkLoad unit test. """
        raise NotImplementedError

    
    def bench(self):
        """ Launch a FunkLoad unit test as load test. """
        collective.funkload.bench.run(args=sys.argv)

def main(url,buildout_dir):
    wrapper = FunkloadWrapper(url,buildout_dir)
    wrapper._dispatch()

