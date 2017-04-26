from django.conf import settings

def get_settings(string="OVP_TESTIMONIALS"):
  return getattr(settings, string, {})
