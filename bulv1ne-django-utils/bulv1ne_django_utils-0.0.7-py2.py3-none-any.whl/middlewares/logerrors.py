from utils.logging import logger


class LogErrors(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        log = logger.name(__name__)
        try:
            log.debug('Before request')
            response = self.get_response(request)
            headers = {k: v for k, v in request.META.items() if k.startswith('HTTP')}
            log.fields(**headers).debug('Headers')
            log.fields(url=request.build_absolute_uri(), content_type=request.content_type).info('Content type URL')
            log.fields(**request.POST).debug('After request')
        except Exception as e:
            log.exception(e)
            raise e
        return response
