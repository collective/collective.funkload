import sys
import os
import optparse
import unittest
import datetime
from thread import error as ThreadError

from zope.testing.testrunner import runner
from zope.testing.testrunner import options

from funkload import BenchRunner
from funkload import FunkLoadTestCase
from funkload import utils

from collective.funkload import loop

USAGE = """\
A FunkLoad unittest use a configuration file named [class].conf, this
configuration is overriden by the command line options.  See
http://funkload.nuxeo.org/ for more information."""

bench = optparse.OptionGroup(options.parser, 'Benchmark', USAGE)
bench.add_option("--url", type="string", dest="main_url",
                  help="Base URL to bench.")
bench.add_option("--cycles", type="string", dest="bench_cycles",
                  help="Cycles to bench, this is a list of number of "
                  "virtual concurrent users, "
                  "to run a bench with 3 cycles with 5, 10 and 20 "
                  "users use: -c 2:10:20")
bench.add_option("--duration", type="string", dest="bench_duration",
                  help="Duration of a cycle in seconds.")
bench.add_option("--sleep-time-min", type="string",
                  dest="bench_sleep_time_min",
                  help="Minimum sleep time between request.")
bench.add_option("-M", "--sleep-time-max", type="string",
                  dest="bench_sleep_time_max",
                  help="Maximum sleep time between request.")
bench.add_option("--startup-delay", type="string",
                  dest="bench_startup_delay",
                  help="Startup delay between thread.")
bench.add_option("-l", "--label", type="string",
                  help="Add a label to this bench run "
                  "for easier identification (it will be appended to the directory name "
                  "for reports generated from it).")
bench.add_option("", "--accept-invalid-links", action="store_true",
                  help="Do not fail if css/image links are "
                  "not reachable.")
bench.add_option("", "--simple-fetch", action="store_true",
                  help="Don't load additional links like css "
                  "or images when fetching an html page.")
options.parser.add_option_group(bench)

in_bench_mode = False

class FLBenchRunner(BenchRunner.BenchRunner, unittest.TestCase):

    __str__ = BenchRunner.BenchRunner.__repr__
                        
    def __init__(self, test, options):
        self.threads = []
        self.module_name = test.__class__.__module__
        self.class_name = test.__class__.__name__
        self.method_name = test.meta_method_name
        self.options = options
        self.color = not options.no_color

        test.in_bench_mode = True
        test.options = options

        self.config_path = test._config_path
        self.result_path = test.result_path
        self.class_title = test.conf_get('main', 'title')
        self.class_description = test.conf_get('main', 'description')
        self.test_id = self.method_name
        self.test_description = test.conf_get(self.method_name, 'description',
                                              'No test description')
        self.test_url = test.conf_get('main', 'url')
        self.cycles = map(int, test.conf_getList('bench', 'cycles'))
        self.duration = test.conf_getInt('bench', 'duration')
        self.startup_delay = test.conf_getFloat('bench', 'startup_delay')
        self.cycle_time = test.conf_getFloat('bench', 'cycle_time')
        self.sleep_time = test.conf_getFloat('bench', 'sleep_time')
        self.sleep_time_min = test.conf_getFloat('bench', 'sleep_time_min')
        self.sleep_time_max = test.conf_getFloat('bench', 'sleep_time_max')

        # setup monitoring
        monitor_hosts = []                  # list of (host, port, descr)
        for host in test.conf_get('monitor', 'hosts', '', quiet=True).split():
            host = host.strip()
            monitor_hosts.append((host, test.conf_getInt(host, 'port'),
                                  test.conf_get(host, 'description', '')))
        self.monitor_hosts = monitor_hosts
        # keep the test to use the result logger for monitoring
        # and call setUp/tearDown Cycle
        self.test = test

    def run(self, *args, **kw):
        """Translate from TestCase to BenchRunner"""
        return BenchRunner.BenchRunner.run(self)

    def startThreads(self, cycle, number_of_threads):
        """Starting threads."""
        BenchRunner.trace(
            "* Current time: %s\n" % datetime.datetime.now().isoformat())
        BenchRunner.trace("* Starting threads: ")
        threads = []
        i = 0
        utils.set_running_flag(True)
        utils.set_recording_flag(False)
        for thread_id in range(number_of_threads):
            i += 1
            thread = loop.LoopTestRunner(
                self.test, self.options, cycle, number_of_threads,
                thread_id, self.sleep_time)
            BenchRunner.trace(".")
            try:
                thread.start()
            except ThreadError:
                BenchRunner.trace("\nERROR: Can not create more than %i threads, try a "
                      "smaller stack size using: 'ulimit -s 2048' "
                      "for example\n" % i)
                raise
            threads.append(thread)
            BenchRunner.thread_sleep(self.startup_delay)
        BenchRunner.trace(' done.\n')
        self.threads = threads

class Runner(runner.Runner):

    def configure(self):
        result = super(Runner, self).configure()
        self.options.no_color = not self.options.color
        return result

    def register_tests(self, tests):
        """Wrap each found test in the Funkload bench runner."""
        self.convertFLTests(tests)
        return super(Runner, self).register_tests(tests)

    def convertFLTests(self, tests):
        """ Only run funkload tests here, and wrap them in a bench """
        for layer, suite in tests.iteritems():
            for test in suite._tests[:]:
                idx = suite._tests.index(test)
                suite._tests.remove(test)
                if isinstance(test, FunkLoadTestCase.FunkLoadTestCase):
                    suite._tests.insert(idx, FLBenchRunner(test, self.options))
                    

def run(defaults=None, args=None):
    runner = Runner(defaults, args)

    global in_bench_mode
    in_bench_mode = True
    runner.run()
    in_bench_mode = False
    
    if runner.failed and runner.options.exitwithstatus:
        sys.exit(1)
    return runner.failed
    
