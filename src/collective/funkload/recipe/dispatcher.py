
import sys
import collective.funkload.bench

class FunkloadWrapper(object):
    
    def __init__(self,url):
        self._url = url
    
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
            fl_args = [self._args[0]] + ['--url=%s' % self._url] +  self._args[2:]
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
        collective.funkload.bench.run()

def main(url):
    wrapper = FunkloadWrapper(url)
    wrapper._dispatch()

