from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern

def any_permission_required(*args):
    """
    A decorator which checks user has any of the given permissions.
    permission required can not be used in its place as that takes only a
    single permission.
    """
    def test_func(user):
        for perm in args:
            print perm
            if user.has_perm(perm):
                return True
        return False
    return user_passes_test(test_func)

def decorator_on_urlpatterns(decorator_func):
    """
    Applies the passed decorator on all the views
    in the urlpatterns, recursively.

    e.g.
    decorator_on_urlpatterns(permission_required('user.is_helpdesk'))(include('states.urls')))
    """
    def decorator(urlpatterns):
        def apply_permissions(patterns):
            for u in patterns:
                if isinstance(u, RegexURLResolver):
                    apply_permissions(u.url_patterns)
                elif isinstance(u, RegexURLPattern):
                    u._callback = decorator_func(u.callback)

        apply_permissions(urlpatterns)
        return urlpatterns
    return decorator

def permission_required_on_urlpatterns(*args, **kwargs):
    """
    Same API as django.contrib.auth.decorators.permission_required
    But to be applied on urlpatterns instead of view

    e.g.
    permission_required_on_urlpatterns('user.is_helpdesk')(include('states.urls')))
    """
    return decorator_on_urlpatterns(permission_required(*args, **kwargs))
