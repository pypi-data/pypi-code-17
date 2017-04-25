from django.contrib.auth.models import AnonymousUser

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()


def get_current_user():
    return getattr(_thread_locals, 'emtex_user', AnonymousUser())


def set_current_user(user_email):
    setattr(_thread_locals, 'emtex_user', user_email)


class GetCurrentUserMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            set_current_user(
                user_email=request.user.email
            )

