import logging
import time
import threading
from django.http import HttpResponse

logger = logging.getLogger("logger")

log_state = False


def log_view(request):
    global log_state
    if log_state is False:
        logger.info('Logging is activated')
        log_state = True
        t = threading.Thread(target=run_logger)
        t.start()
    else:
        logger.info('Logging is deactivated')
        log_state = False

    return HttpResponse('Logging started')


def run_logger():
    global log_state
    while log_state:
        time.sleep(2)