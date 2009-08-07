import threading

from funkload import BenchRunner

class LoopTestRunner(BenchRunner.LoopTestRunner):

    def __init__(self, test, options, cycle, cvus, thread_id,
                 sleep_time, debug=False):
        meta_method_name = BenchRunner.mmn_encode(
            test.meta_method_name, cycle, cvus, thread_id)
        threading.Thread.__init__(
            self, target=self.run, name=meta_method_name, args=())
        # Instanciate test anew with meta_method_name to ensure correct logging
        self.test = test.__class__(meta_method_name, test.options)
        self.color = not options.no_color
        self.sleep_time = sleep_time
        self.debug = debug
        # this makes threads endings if main stop with a KeyboardInterupt
        self.setDaemon(1)
