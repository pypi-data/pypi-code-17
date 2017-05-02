from .aggregates import *

try:
    # Django 1.7+
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    # Django < 1.7
    from django.db.models.loading import get_model
