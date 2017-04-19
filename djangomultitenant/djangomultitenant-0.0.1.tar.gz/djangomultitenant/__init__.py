from threading import local


thread_local_data = local()


class Middleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_code = request.META.get('HTTP_TENANT_CODE', 'unknown')
        setattr(thread_local_data, 'tenant_code', str(tenant_code).lower())
        response = self.get_response(request)
        return response


class Router(object):

    @staticmethod
    def _select_db():
        return getattr(thread_local_data, 'tenant_code', 'unknown')

    def db_for_read(self, model, **hints):
        return self._select_db()

    def db_for_write(self, model, **hints):
        return self._select_db()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
