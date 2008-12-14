import sys
import os
import ConfigParser

from funkload import FunkLoadTestCase

from collective.funkload import bench

class FLTestCase(FunkLoadTestCase.FunkLoadTestCase):

    def _funkload_init(self):
        """Pull the conf file based on the test case class"""
        self.in_bench_mode = bench.in_bench_mode
        
        config_directory = os.path.dirname(
            sys.modules[self.__class__.__module__].__file__)
        config_path = os.path.join(config_directory,
                                   self.__class__.__name__ + '.conf')
        config_path = os.path.abspath(config_path)
        if not os.path.exists(config_path):
            config_path = "Missing: "+ config_path
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        self._config = config
        self._config_path = config_path
        self.default_user_agent = self.conf_get(
            'main', 'user_agent', 'FunkLoad/%s' %
            FunkLoadTestCase.get_version(), quiet=True)
        if self.in_bench_mode:
            section = 'bench'
        else:
            section = 'ftest'
        ok_codes = self.conf_getList(section, 'ok_codes',
                                     [200, 301, 302, 303, 307],
                                     quiet=True)
        self.ok_codes = map(int, ok_codes)
        self.sleep_time_min = self.conf_getFloat(
            section, 'sleep_time_min', 0)
        self.sleep_time_max = self.conf_getFloat(
            section, 'sleep_time_max', 0)
        self.log_to = self.conf_get(section, 'log_to', 'console file')
        self.log_path = self.conf_get(section, 'log_path', 'funkload.log')
        self.result_path = os.path.abspath(
            self.conf_get(section, 'result_path', 'funkload.xml'))

        # init loggers
        self.logger = FunkLoadTestCase.get_default_logger(
            self.log_to, self.log_path)
        self.logger_result = FunkLoadTestCase.get_default_logger(
            log_to="xml", log_path=self.result_path, name="FunkLoadResult")

        # init webunit browser (passing a fake methodName)
        self._browser = FunkLoadTestCase.WebTestCase(methodName='log')
        self.clearContext()
