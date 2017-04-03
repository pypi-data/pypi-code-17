from django.conf import settings
import importlib

def get_settings(string="OVP_NEWS"):
  return getattr(settings, string, {})
