import logging
import os
import sys

LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'TRACE'

TRACE_LEVEL_NUM = 5
logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")


def log_trace(self, message, *args, **kws):
    if self.isEnabledFor(TRACE_LEVEL_NUM):
        self._log(TRACE_LEVEL_NUM, message, args, **kws)


logging.Logger.trace = log_trace
log = logging.getLogger()
log.setLevel(LOG_LEVEL)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(LOG_LEVEL)
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)8s] [%(threadName)s] --- %(message)s (%(filename)s:%(lineno)s)", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
log.addHandler(handler)
