import sys

from zope.testing.testrunner import runner

from funkload import BenchRunner

class Runner(runner.Runner):
    
    def register_tests(self, tests):
        """Wrap each found test in the Funkload bench runner."""
        return super(Runner, self).register_tests(
            BenchRunner.BenchRunner(test) for test in tests)

def run(defaults=None, args=None):
    runner = Runner(defaults, args)
    runner.run()
    if runner.failed and runner.options.exitwithstatus:
        sys.exit(1)
    return runner.failed
    
