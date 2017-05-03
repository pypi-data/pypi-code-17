import os


DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

INSTALLED_APPS = (
    "form_renderers",
    "form_renderers.tests",
    "django.contrib.contenttypes",
    "django.contrib.sites",
)

SITE_ID = 1

SECRET_KEY = "SECRET_KEY"

FORM_RENDERERS = {"enable-bem-classes": True}
