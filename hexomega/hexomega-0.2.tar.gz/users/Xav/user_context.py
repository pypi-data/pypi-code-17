from django.http import HttpResponseForbidden


def url_context(function):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if request.user.username not in request.get_full_path():
            return HttpResponseForbidden()
        else:
            return function(request, *args, **kwargs)
    return wrapper
