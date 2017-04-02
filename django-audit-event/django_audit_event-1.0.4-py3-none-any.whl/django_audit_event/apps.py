from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class Config(AppConfig):
    name = 'app_audit_event'
    label = 'django_audit_event'
    verbose_name = _("Audit Event")
    verbose_name_plural = _("Audit Events")
