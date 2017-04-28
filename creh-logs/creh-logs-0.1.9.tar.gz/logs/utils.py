import sys

from django.conf import settings
from django.db.models.loading import get_model


def get_location():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    location = '%s %s' %(exc_tb.tb_frame.f_code.co_filename, exc_tb.tb_lineno)
    return location


def verify_user(user):
    if user is not None:
        user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
        user_model = get_model(user_model.split('.')[0], user_model.split('.')[1])
        if isinstance(user, user_model):
            return user
    return None


def verify_exception(exception):
    try:
        return exception.__class__.__name__
    except Exception, e:
        return 'The exception could not be identified'
