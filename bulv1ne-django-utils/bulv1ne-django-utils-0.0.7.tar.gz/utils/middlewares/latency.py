import time

from utils.logging import logger


class LatencyMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log = logger.name(__name__)
        start_time = time.time()
        try:
            return self.get_response(request)
        finally:
            ms = int((time.time() - start_time) * 1000)
            log.fields(url=request.build_absolute_uri()).info('Latency {}ms'.format(ms))
