import logging
import os
import sys


TRACE_LEVEL_NUM = 5
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")


def log_trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws)


logging.Logger.trace = log_trace

log = logging.getLogger()
log.setLevel(os.environ.get('LOG_LEVEL') or logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s',
                              datefmt='%a, %d %b %Y %H:%M:%S')
handler.setFormatter(formatter)
log.addHandler(handler)
